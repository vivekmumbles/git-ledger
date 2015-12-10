# git-ledger

github repo visualization tool

[demo](http://vivekmumbles.github.io/git-ledger/viz.html)

## demo instructions

left click to enter folder
right click on folder/file to view contributions

when hovering metadata can be viewed in the bottom left

press `space` to view contributions for entire folder

`alt` key is shortcut for going back, the left arrow does the same thing

pressing `enter` after typing in directory is a short cut of going to that directory, the right arrow does the same thing

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

