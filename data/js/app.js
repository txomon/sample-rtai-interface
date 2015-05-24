/**
 * The API should be the following:
 *
 * * Request initialization;
 *  send({'type': 'initialize'})
 *
 *
 *
 */
var application = new function () {
    this.get_container = function () {
        var conts = document.getElementsByTagName('div');
        var container;
        for (var i = 0; i < conts.length; i++) {
            container = conts[i];
            if (container.id == 'container')
                break;
        }
        if (!container || container.id != 'container') {
            container = document.createElement('div');
            container.id = 'container';
            var body = document.getElementsByTagName('body')[0];
            body.appendChild(container);
        }
        return container;
    };

    this.get_display = function (display_id) {
        var container = this.get_container();
        var display = document.getElementById(display_id);
        if (!display) {
            var display = document.createElement("section");
            display.id = display_id;
            container.appendChild(display);
        }
        return display;
    };

    this.update_display = function (data) {
        var display = this.get_display(data['id']);
        if (!display.innerHTML)
            display.innerHTML = '<div></div>';
    };

    this.handle_initialize = function (msg) {
        console.log("Handling initialization");
        for (var i = 0; i < msg['displays'].length; i++) {
            var display = msg['displays'][i];
            this.update_display(display);
        }
    };

    this.onmessage = function (e) {
        try {
            var o = JSON.parse(e.data);
        } catch (err) {
            console.error("Data unable to parse:" + e.data);
            return;
        }
        if (o['type'] == 'error') {
            console.log('Error ocurred in backend: ' + o['message']);
        }
        else if (o['type'] == 'initialize') {
            this.handle_initialize(o['message']);
        } else {
            console.log('No idea on what to do with type ' + o['type']);
        }
    };

};

ws = new WebSocket("ws://" + location.host + '/ws');

ws.onopen = function (e) {
    console.log("Opened ws " + e);
    this.send('{"type": "initialize"}');
};

ws.onerror = function (e) {
    console.log("Error on the WS" + e);
};

ws.onclose = function (e) {
    console.log("WS closed!");
};

ws.onmessage = function (e) {
    application.onmessage(e);
};
