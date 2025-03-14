var timeout = 15000;

window.setTimeout(poller, timeout);

function poller() {
    window.location = "http://127.0.0.1:5000/0";
}
