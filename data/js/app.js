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
    this.handle_initialize = function (msg) {
        console.log("Handling initialization");
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
