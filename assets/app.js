$.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};


server_logger = {
    console: $('#server-log ul'),
    log: function(msg) {
        this.console.append('<li>' + msg + '</li>');
    }
}

$('[data-action=start-server]').click(function(e) {
    e.preventDefault();
    var settings = $('#vars-form').serializeObject();
    settings.base_path = $('#curr-folder').text();
    app_server.start(JSON.stringify(settings));
});

$('[data-action=set-project-root]').click(function(e) {
    e.preventDefault();
    file_browser.select_dir();
    $('#curr-folder').text(file_browser.dirname);
});

$('[data-action=stop-server]').click(function(e) {
    e.preventDefault();
    app_server.stop();
});

$('#vars-form').submit(function(e) {
    e.preventDefault();
});