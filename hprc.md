Step 1: Go to the installed repo:
=================================

This is the project home

    cd /general/group/pinfo/gurudev/EGS/

Step 2: Changing the config file
================================

The config file can be found in "./example/" (Complete file path: */general/group/pinfo/gurudev/EGS/example/*). Change the parameters in the **config.txt** file.

Step 3: Generating the modified files
=====================================

From the project home,

    module load Python/2.7.10-goolf-1.7.20
    python test.py

Step 4: Accesing the modified csv files
=======================================

The modified csv files can be found in "./data/" (Complete file path: */general/group/pinfo/gurudev/EGS/data/*). The 3 files are:

1.  changes.csv
2.  data\_modified.csv
3.  data\_origin.csv
