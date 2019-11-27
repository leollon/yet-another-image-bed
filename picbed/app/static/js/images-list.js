$(
    function () {
        // render images in images listing page
        $.get("/api/v1/image/", function (data) {
            var images = data.images;
            if (images) {
                $.each(images, function (key, arr) {
                    var html = "\
                        <li class='content' id = " + arr.img_id + ">" +
                        "<img src='/" + arr.img_name + "' class='img-thumbnail'>" +
                        "<div class='operation'><button class='btn btn-danger del-btn' data-img-id=" +
                        arr.img_id + ">" +
                        "<span class='glyphicon glyphicon glyphicon-trash aria-hidden='true'></span>\
                            </button> \
                            </div> \
                        </li>"
                    $("#image-list").append(html);
                })
            } else {
                html = "<a class='btn btn-link href='/'>go to upload</a>"
                $("#image-list").append(html)
            }
        })
    }
)

$('.del-btn').on('click', function (event) {
    let id = $(this).data('img-id');
    let confirmation = window.confirm("Remove image " + id);
    if (confirmation) {
        $.ajax({
            url: '/api/v1/image/' + id,
            type: 'DELETE',
            success: function () {
                $('#' + id).remove()
            }
        })
    }
})