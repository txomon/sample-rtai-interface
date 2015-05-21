
/**
 * The API should be the following:
 *
 * * Request initialization;
 *  send({'type': 'initialize'})
 *
 *
 *
 */
var ws = new WebSocket("ws://" + location.host + '/ws');

ws.onopen = function (ev) {
    console.log("Opened ws " + ev);
    if (this.readyState == 1)
        console.log('Calling is possible');
    else
        console.log('Calling is not possible');
    this.send("Here the app");
    //this.send("{'type': 'initialize'}");
};
ws.onerror = function (ev) {
    console.log("Error on the WS" + ev);
};
ws.onclose = function (ev) {
    console.log("WS closed!");
}
ws.onmessage = function (msg) {
    console.log("Received "+ msg);
}
