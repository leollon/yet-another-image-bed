const respJsonData = {};

function getCSRFToken() {
    return $('input[name="csrf_token"]').attr('value');
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        }
    },
    error: function (event) {
        console.log(event);
    }
});

$('#select-file').click(function () {
    $('#file').trigger('click');
});

$('#file').on("change", function () {
    let preview = $('#img-thumbnail');
    preview.attr('src', window.URL.createObjectURL(this.files[0]));
    if (this.files[0]) {
        $('#submit').css('visibility', 'visible');
    }
    $('#filename').val(this.files[0].name);
});

$('#submit').click(function () {
    let formData = new FormData($('form')[0]);
    if (formData) {
        $.ajax({
            url: '/image/',
            type: 'POST',
            cache: false,
            data: formData,
            enctype: 'multipart/form-data',
            processData: false,
            contentType: false,
            success: function (xhr) {
                $('#nav-tabs').css('visibility', 'visible');
                $('#navTabContent').css('visibility', 'visible');
                renderData(xhr);
            },
            'error': function (event) {
                console.log(event);
            }
        })
    }
});

function renderData(jsonData) {
    let imgLink = window.location.href + jsonData.data.imgName;
    let urlcode = imgLink,
        htmlcode = '<img src="' + imgLink + '" alt="' + jsonData.data.origName + '" title="' + jsonData.data.origName + '">',
        markdowncode = '![' + jsonData.data.imgName + '](' + imgLink + ')',
        mdwithlinkcode = '![' + imgLink + '](' + imgLink + ')';
    let deletecode = window.location.href + 'remove/' + jsonData.data.imgId;
    $('#urlcode').text(urlcode);
    $('#htmlcode').text(htmlcode);
    $('#markdowncode').text(markdowncode);
    $('#mdwithlinkcode').text(mdwithlinkcode);
    $('#deletecode').text(deletecode);
}

$('.del-btn').on('click', function (e) {
    let id = $(this).data('img-id');
    let confirmation = window.confirm("Remove image " + id);
    if (confirmation) {
        $.ajax({
            url: '/remove/' + id,
            type: 'GET',
            success: function () {
                $('#' + id).remove()
            }
        })
    }
})