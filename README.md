# git-ledger

github repo visualization tool

## usage

run:

```bash
python3 data.py
```
This will prompt you to enter the url for the GitHub repo and will then generate a data.json file.

```bash
python -m SimpleHTTPServer 8000 .
```
You need a local server to open the html file.

Then all you have to do is open localhost in your favorit browser. For Linux that is 127.0.0.1.

Then just navigate to the `viz.html` file and visualization should be generated.

