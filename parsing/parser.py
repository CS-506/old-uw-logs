#!/usr/bin/env python
import dir_parser
import gpa_parser

# all sections
dirs = dir_parser.parse_dir_pdf('dir_1174.pdf')

# seems to list:
# * most lecture sections (not AAE 652 - 0 enrolled)
# * independent study sometimes
# 
# just random in general?
gpas = gpa_parser.parse_gpa_pdf('gpa_1174.pdf')
