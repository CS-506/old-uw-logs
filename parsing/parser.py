#!/usr/bin/env python
import dir_parser
import gpa_parser
import dir_fetcher

# all sections
dirs = dir_parser.parse_dir_pdf('../data/dir_1174.pdf')
print(len(dirs))
# seems to list:
# * most lecture sections (not AAE 652 - 0 enrolled)
# * independent study sometimes
# 
# just random in general?
# gpas = gpa_parser.parse_gpa_pdf('gpa_1174.pdf')
