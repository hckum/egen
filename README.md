# Error Generation Simulator
[![Build Status](https://travis-ci.org/hwangtamu/EGS.svg?branch=master)](https://travis-ci.org/hwangtamu/EGS)

THIS IS WORK IN PROGRESS.
We recommend you contact us before using it (kum at tamu dot edu).

This software is used for derived data generation by introducing errors to real record database. Various types of errors can be generated based on the user-customized configuration. Currently, this software supports alphabetical and numeric data formats. Alphanumeric format will be supported in the future.

The error types include typos (insertion, deletion, transposition and replace), field swap (first & last name, month and data), field missing, and human name variation (both nicknames, and common misspellings).

## Dependency
`python==2.7`
## Installation
```
$git clone https://github.com/hwangtamu/EGS.git
$cd EGS
$python setup.py install
```

## Beginner's Guide

Try the following code:
```python
>>>from egs.table import Table
>>>t = Table()
>>>t.load_config(config_path) # the config_path can be empty
>>>t.load_data(data_path) # the path of raw data
>>>t.generate() # error generation
>>>t.write() # write output files
```

## Documentation

## Bug Report
