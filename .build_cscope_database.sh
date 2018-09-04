#!/bin/bash

# Create a list of all the files to be included in the database
CSCOPE_FILES=cscope.files
find ./ -name *.py > $CSCOPE_FILES

# Generate the scsope database (cscope.out)
cscope -b

