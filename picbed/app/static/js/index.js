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
            url: '/api/v1/image/',
            type: 'POST',
            cache: false,
            data: formData,
            enctype: 'multipart/form-data',
            processData: false,
            contentType: false,
            success: function (respData) {
                $('#nav-tabs').css('visibility', 'visible');
                $('#navTabContent').css('visibility', 'visible');
                renderData(respData);
            },
            'error': function (event) {
                console.log(event);
            }
        })
    }
});

function renderData(respData) {
    let imgLink = window.location.href + respData.image.imgName;
    let urlcode = imgLink,
        htmlcode = '<img src="' + imgLink + '" alt="' + respData.image.origName + '">',
        markdowncode = '![' + respData.image.imgName + '](' + imgLink + ')',
        mdwithlinkcode = '![' + imgLink + '](' + imgLink + ')';
    let deletecode = window.location.href + 'remove/' + respData.image.imgId;
    $('#urlcode').text(urlcode);
    $('#htmlcode').text(htmlcode);
    $('#markdowncode').text(markdowncode);
    $('#mdwithlinkcode').text(mdwithlinkcode);
    $('#deletecode').text(deletecode);
}