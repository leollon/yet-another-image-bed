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