import { Request } from "hoxy";

var hoxy = require('hoxy');
var port = 8080;

var proxy = hoxy.createServer().listen(port, function() {
    console.log('The proxy is listening on port ' + port + '.');
});

proxy.intercept({
    phase: 'request'
}, function(request: Request) {
    console.log("data: " + request.hostname);
});