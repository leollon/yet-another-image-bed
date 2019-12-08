import re
import sys
from io import BytesIO
from pathlib import Path

from flask import json

IMG_BASE_DIR = Path(__file__).parent.joinpath("images")
TOKEN_PAT = re.compile(r"X-CSRFToken\",\ \"([a-zA-Z0-9_\-\.\)]*)")


def test_index(client):
    response = client.get("/")
    assert b"Image Upload" in response.data


def test_get(client):
    rv = client.get("/api/v1/images")
    assert "application/json" == rv.headers["Content-Type"]
    assert b"images" in rv.data


def test_upload(client, app):
    csrf_token = ""
    # have no csrf_token
    post_resp_data = client.post(
        "/api/v1/images",
        headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"},
        data={"file": (BytesIO(open((IMG_BASE_DIR / "gif.gif").as_posix(), "rb").read()), "gif.gif")},
    )

    sys.stdout.write(post_resp_data.data.decode("utf-8"))
    assert post_resp_data.status_code == 400
    assert b"The CSRF token is missing." in post_resp_data.data

    resp_data = client.get("/").data.decode("utf-8")
    csrf_token = re.search(TOKEN_PAT, resp_data).group(1)

    # have no image provided.
    post_resp_data = client.post(
        "/api/v1/images", headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"}, data={}
    )

    assert post_resp_data.status_code == 400
    assert b"Missing required parameter in an uploaded file" in post_resp_data.data

    # have no image file, but have a filename
    post_resp_data = client.post(
        "/api/v1/images",
        headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"},
        data={"file": (BytesIO(b""), "filename.jpg")},
    )

    sys.stdout.write(post_resp_data.data.decode("utf-8"))
    assert post_resp_data.status_code == 200
    assert "OK" in post_resp_data.status
    assert b"imgName" in post_resp_data.data
    assert b"imgId" in post_resp_data.data

    # have no image data
    post_resp_data = client.post(
        "/api/v1/images",
        headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"},
        data={"file": (BytesIO(b"ajef"), "filename2.jpg")},
    )

    sys.stdout.write(post_resp_data.data.decode("utf-8"))
    assert post_resp_data.status_code == 200
    assert "OK" in post_resp_data.status
    assert b"imgName" in post_resp_data.data
    assert b"imgId" in post_resp_data.data

    # no supported file
    post_resp_data = client.post(
        "/api/v1/images",
        headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"},
        data={"file": (BytesIO(open((IMG_BASE_DIR / "rfc1180.pdf").as_posix(), "rb").read()), "rfc1180.pdf")},
    )

    sys.stdout.write(post_resp_data.data.decode("utf-8"))
    assert post_resp_data.status_code == 400
    assert "BAD REQUEST" in post_resp_data.status
    assert b"No supported type" in post_resp_data.data

    # image too large, larger than 5MB, png image
    post_resp_data = client.post(
        "/api/v1/images",
        headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"},
        data={"file": (BytesIO(open((IMG_BASE_DIR / "big-png.png").as_posix(), "rb").read()), "big-png.png")},
    )

    sys.stdout.write(post_resp_data.data.decode("utf-8"))
    assert post_resp_data.status_code == 413
    assert "REQUEST ENTITY TOO LARGE" in post_resp_data.status
    assert b"4013" in post_resp_data.data

    # image smaller than 5MB, jpeg image
    post_resp_data = client.post(
        "/api/v1/images",
        headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"},
        data={"file": (BytesIO(open((IMG_BASE_DIR / "photo-1.jpeg").as_posix(), "rb").read()), "photo-1.jpeg")},
    )

    sys.stdout.write(post_resp_data.data.decode("utf-8"))
    assert post_resp_data.status_code == 200
    assert b"image" in post_resp_data.data
    assert b"imgName" in post_resp_data.data
    assert b"Success" in post_resp_data.data

    # image smaller than 5MB, jpeg image, but have no filename
    post_resp_data = client.post(
        "/api/v1/images",
        headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"},
        data={"file": (BytesIO(open((IMG_BASE_DIR / "photo-1.jpeg").as_posix(), "rb").read()), "")},
    )

    sys.stdout.write(post_resp_data.data.decode("utf-8"))
    assert post_resp_data.status_code == 400
    assert b"No selected file" in post_resp_data.data

    # image smaller than 5MB, png file, but have no permission to save image file
    Path(app.config["UPLOAD_BASE_FOLDER"]).chmod(mode=0o444)
    post_resp_data = client.post(
        "/api/v1/images",
        headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"},
        data={"file": (BytesIO(open((IMG_BASE_DIR / "EFUQVf7W.png").as_posix(), "rb").read()), "EFUQVf7W.png")},
    )

    sys.stdout.write(post_resp_data.data.decode("utf-8"))
    assert post_resp_data.status_code == 502
    assert b"No permission" in post_resp_data.data

    Path(app.config["UPLOAD_BASE_FOLDER"]).chmod(mode=0o755)

    post_resp_data = client.post(
        "/api/v1/images",
        headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"},
        data={"file": (BytesIO(open((IMG_BASE_DIR / "DoS.svg").as_posix(), "rb").read()), "DoS.svg")},
    )

    sys.stdout.write(post_resp_data.data.decode("utf-8"))
    assert post_resp_data.status_code == 200
    assert b"image" in post_resp_data.data
    assert b"imgName" in post_resp_data.data
    assert b"Success" in post_resp_data.data

    # an gif image smaller than 5MB
    post_resp_data = client.post(
        "/api/v1/images",
        headers={"X-CSRFToken": csrf_token, "Content-Type": "multipart/form-data"},
        data={
            "file": (
                BytesIO(open((IMG_BASE_DIR / "lillard_goodbye.gif").as_posix(), "rb").read()),
                "lillard_goodbye.gif",
            )
        },
    )

    sys.stdout.write(post_resp_data.data.decode("utf-8"))
    assert post_resp_data.status_code == 200
    assert b"image" in post_resp_data.data
    assert b"imgName" in post_resp_data.data
    assert b"Success" in post_resp_data.data


def test_delete(client):
    csrf_token = ""
    resp_data = client.delete("/api/v1/images/123324", headers={"X-CSRFToken": csrf_token})

    sys.stdout.write(resp_data.data.decode("utf-8"))
    assert resp_data.status_code == 400
    assert b"The CSRF token is missing." in resp_data.data

    resp_data = client.get("/").data.decode("utf-8")
    csrf_token = re.search(TOKEN_PAT, resp_data).group(1)

    images = json.loads(client.get("/api/v1/images").data)["images"]
    img_id = images[0]["img_id"]

    resp_data = client.delete("/api/v1/images/" + img_id, headers={"X-CSRFToken": csrf_token})

    sys.stdout.write(resp_data.data.decode("utf-8"))
    assert resp_data.status_code == 204
    assert "NO CONTENT" in resp_data.status


def test_remove(client):
    resp_data = client.get("/remove/234134")
    assert resp_data.status_code == 404
