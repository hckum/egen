c = [
##======================================================##
## CONFIGURATION FILE TO THE ERROR GENERATION SIMULATOR ##
##======================================================##

# INPUT FILES
# Put input files in /data subfolder

"input = data/apr13.csv",

# Lookup Table

"lookup = data/lookup.txt",

# OUTPUT FILES
# Specify the file paths where the output files will be stored.
# Do not change the variable names on the left side

"original_data = data_origin.csv",
"modified_data = data_modified.csv",
"differences = changes.csv",

# USAGE:
#   rate : the overall error rate
#   rate_missing : the rate of missing error
#   rate_swap : the rate of swap error (swap between fields or months/days)
#   rate_typo : the rate of typo errors
#   rate_vari : the rate of name variation errors

"rate = 0.03",
"rate_missing = 0.2",
"rate_swap_name = 0.05",
"rate_swap_dob = 0.05",
"rate_typo = 0.6",
"rate_vari = 0.1",

# If specified, must also list name of suffix field
"rate_suffix = 0.1",
"var_suffix=name_suff_cd",


# FIELD SELECTION
# customize the input and output files here
# select some fields from the original data
# separated with comma
# name_sufx_cd

# immutable: i
# date: d
# fixed length: f
# variable length: v
# merge alphabetics and digits into one class

"fields_formats = ID:if, voter_reg_num:f, last_name:v, first_name:v, dob:d",

# PROBABILITIES OF TYPO ERRORS
# probability of insertion, deletion, transposition, substitution
# usually no need to change this part

# variable length
"v_rate_insertion = 0.4",
"v_rate_deletion = 0.3",
"v_rate_transpose = 0.15",
"v_rate_substitution = 0.15",

# fixed length
"f_rate_insertion = 0.5",
"f_rate_transpose = 0.25",
"f_rate_substitution = 0.25",

# date
"d_rate_transpose = 0.5",
"d_rate_substitution = 0.5",

################# ADVANCED,
"pins_neigh = 2"]
