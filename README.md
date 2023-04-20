# Simple Mitm proxy add-on

For log specific request and response to json data

## How to use Mitm add-on

- download mitmproxy <https://mitmproxy.org/>
- Setup machine proxy to <http://127.0.0.1:8080>
- Install certificate from this web <http://mitm.it/>
- Write add-on python script
- Execute Mitmproxy to accept own python script
`<location>/mitmproxy.exe -s ./myscript.py`
- Test script via sending request to any website

## Useful link

- Cheatsheet - <https://www.stut-it.net/blog/2017/mitmproxy-cheatsheet.html>
- Add-on example - <https://lucaslegname.github.io/mitmproxy/2020/11/04/mitmproxy-scripts.html>
