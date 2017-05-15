# Error Generation (EGEN) for Benchmarking Record Linkage Algorithms 
[![Build Status](https://travis-ci.org/hwangtamu/EGS.svg?branch=master)](https://travis-ci.org/hwangtamu/EGS)

THIS IS WORK IN PROGRESS.
We recommend you contact us before using it (kum at tamu dot edu).

This software is used for derived data generation by introducing errors to real record database. Various types of errors can be generated based on the user-customized configuration. You can link your original data to the derived data (orignal data infused with errors as specified in the config file) to benchmark record linkage algorithms. You can also evaluate how your algorithm does as more errors are infused.

This software includes links to potential real data you can use, if you do not have access to your own real data.

The error types include typos (insertion, deletion, transposition and replace), field swap (first & last name, month and data), field missing, and human name variation (both nicknames, and common misspellings).

Currently, we only handle DOB. Next version will include handling age.

## Dependency
`python==2.7`
## Installation
```
$git clone https://github.com/hwangtamu/egen.git
$cd egen
$python setup.py install
```

## Beginner's Guide

Try the following code:
```python
>>>from egen.table import Table
>>>t = Table()
>>>t.load_config(config_path) # the config_path can be empty
>>>t.load_data(data_path) # the path of raw data
>>>t.generate() # error generation
>>>t.write() # write output files
```

## Documentation

## Bug Report
