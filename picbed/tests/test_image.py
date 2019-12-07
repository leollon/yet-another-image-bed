import re
from io import BytesIO
from pathlib import Path

IMG_BASE_DIR = Path("./images")
TOKEN_PAT = re.compile(r"X-CSRFToken\",\ \"([a-zA-Z0-9_\-\.\)]*)")


def test_index(client):
    response = client.get("/")
    assert b"Image Upload" in response.data


def test_get(client):
    rv = client.get("/api/v1/images")
    assert b"application/json" == rv.headers["Content-Type"]
    assert b"images" in rv.data


def test_upload(client, app):
    csrf_token = ""
    # have no csrf_token
    post_resp_data = client.post("/api/v1/images", content_type="multipart/form-data", data={
        "csrf_token": csrf_token,
        "file": (BytesIO(open((IMG_BASE_DIR / "gif.gif").as_posix()).read()), "gif.gif"),
    })

    assert post_resp_data.status_code == 400
    assert b"The CSRF token is missing." in post_resp_data.data

    resp_data = client.get("/").data.decode("utf-8")
    csrf_token = re.search(TOKEN_PAT, resp_data.decode("utf-8")).group(1)

    # have no image provided.
    post_resp_data = client.post("/api/v1/images", content_type="multipart/form-data", data={
        "csrf_token": csrf_token,
    })

    assert post_resp_data.status_code == 400
    assert b"BAD REQUEST" in post_resp_data.data
    assert b"Missing required parameter in an uploaded file" in post_resp_data.data

    # have no image data
    post_resp_data = client.post("/api/v1/images", content_type="multipart/form-data", data={
        "csrf_token": csrf_token,
        "file": (BytesIO(b""), "filename.jpg"),
    })

    assert post_resp_data.status_code == 400
    assert b"BAD REQUEST" in post_resp_data.data
    assert b"No supported type" in post_resp_data.data

    # no supported file
    post_resp_data = client.post("/api/v1/images", content_type="multipart/form-data", data={
        "csrf_token": csrf_token,
        "file": (BytesIO(open((IMG_BASE_DIR / "rfc1180.pdf").as_posix(), "rb").read()), "rfc1180.pdf"),
    })

    assert post_resp_data.status_code == 400
    assert b"BAD REQUEST" in post_resp_data.status_code
    assert b"No supported type" in post_resp_data.data

    # image too large, larger than 5MB, png image
    post_resp_data = client.post("/api/v1/images", content_type="multipart/form-data", data={
        "csrf_token": csrf_token,
        "file": (BytesIO(open((IMG_BASE_DIR / "big-png.png").as_posix(), "rb").read()), "big-png.png"),
    })

    assert post_resp_data.status_code == 413
    assert b"Request Entity Too Large`" in post_resp_data.status
    assert b"4013" in post_resp_data.data

    # image smaller than 5MB, jpeg image
    post_resp_data = client.post("/api/v1/images", content_type="multipart/form-data", data={
        "csrf_token": csrf_token,
        "file": (BytesIO(open((IMG_BASE_DIR / "photo-1.jpeg").as_posix(), "rb").read()), "photo-1.jpeg"),
    })

    assert post_resp_data.status_code == 200
    assert b"image" in post_resp_data.data
    assert b"imgName" in post_resp_data
    assert b"Success" in post_resp_data.data

    # image smaller than 5MB, jpeg image, but have no filename
    post_resp_data = client.post("/api/v1/images", content_type="multipart/form-data", data={
        "csrf_token": csrf_token,
        "file": (BytesIO(open((IMG_BASE_DIR / "photo-1.jpeg").as_posix(), "rb").read()), ""),
    })

    assert post_resp_data.status_code == 400
    assert b"No selected file" in post_resp_data.data

    # image smaller than 5MB, png file, but have no permission to save image file
    Path(app.config['UPLOAD_BASE_FOLDER']).chmod(mode=444)
    post_resp_data = client.post("/api/v1/images", content_type="multipart/form-data", data={
        "csrf_token": csrf_token,
        "file": (BytesIO(open((IMG_BASE_DIR / "EFUQVf7W4AAGyMi.png").as_posix(), "rb").read()), "EFUQVf7W4AAGyMi.png")
    })

    assert post_resp_data.status_code == 502
    assert b"No permission" in post_resp_data.data

    Path(app.config['UPLOAD_BASE_FOLDER']).chmod(mode=0o644)

    post_resp_data = client.post("/api/v1/images", content_type="multipart/form-data", data={
        "csrf_token": csrf_token,
        "file": (BytesIO(open((IMG_BASE_DIR / "DoS.svg").as_posix(), "rb").read()), "DoS.svg")
    })

    assert post_resp_data.status_code == 200
    assert b"image" in post_resp_data.data
    assert b"imgName" in post_resp_data
    assert b"Success" in post_resp_data.data

    # an gif image smaller than 5MB
    post_resp_data = client.post("/api/v1/images", content_type="multipart/form-data", data={
        "csrf_token": csrf_token,
        "file": (BytesIO(open((IMG_BASE_DIR / "lillard_goodbye.gif").as_posix(), "rb").read()), "lillard_goodbye.gif")
    })

    assert post_resp_data.status_code == 200
    assert b"image" in post_resp_data.data
    assert b"imgName" in post_resp_data
    assert b"Success" in post_resp_data.data


def test_delete(client):
    pass


def test_remove(client):
    rv = client.get("/remove/234134")
    assert rv.status == 404
