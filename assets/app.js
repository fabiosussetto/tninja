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


$('[data-action=start-server]').click(function(e) {
    e.preventDefault();
    app_server.start();
});

$('[data-action=stop-server]').click(function(e) {
    e.preventDefault();
    app_server.stop();
});

$('#vars-form').submit(function(e) {
    e.preventDefault();
    settings.save(JSON.stringify($(this).serializeObject()));
});