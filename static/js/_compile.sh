#!/bin/bash
browserify bootstrap.js -o bundle.js
uglifyjs bundle.js --compress --mangle -o bundle.min.js
