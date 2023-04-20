# Simple Mitm proxy add-on

For log specific request and response to json data

## How to use Mitm add-on

- Start Mitmproxy <127.0.0.1:8081>
- Setup machine proxy to <127.0.0.1:8080>
- Install certificate from this web <http://mitm.it/>
- Write add-on python script
- Execute Mitmproxy to accept own python script
`mitmproxy -s ./myscript.py`
- Test script via sending request to any website
