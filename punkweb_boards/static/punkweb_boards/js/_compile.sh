#!/bin/bash
browserify bootstrap.js -o lib/punkweb-boards.js
uglifyjs lib/punkweb-boards.js --compress --mangle -o lib/punkweb-boards.min.js
