#!/usr/bin/env python
# -*- coding: utf8 -*-

from sys import stdout
from string import replace
import argparse
import re
import csv


parser = argparse.ArgumentParser()
parser.add_argument('-y', '--year', help = "Year for invoice")
parser.add_argument('-s', '--src', help = "Read from file")
# parser.add_argument('-o', '--output', help = "Target for output - .csv")
args = parser.parse_args()

def get_year(year):
    yr = re.compile(r'[0-9][0-9][0-9][0-9]')
    if yr.match(year):
        return year

def convert_date(day, month, year):
    day_prefix = re.compile(r'(st|nd|rd|th)')
    months = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
        }

    date_str =  day_prefix.sub('', day) + '/' +  months[month] + '/' + year
    return date_str

# Open a file and read lines, print non-blanks only
f = open(args.src)

# Create a CSV writer to output properly
linewriter = csv.writer(stdout, quotechar = '"', quoting = csv.QUOTE_ALL)

# Set up a header
header = ["Date", "Payee", "Memo", "Outflow", "Inflow"]

# Print the header
linewriter.writerow(header)

# List up the statement lines
statement_lines = []

for line in f:
    if line not in ['\n', '\r\n']:
        if '?' in line:
            statement_lines.append(replace(line, '?', '').split())
        elif '£' in line:
            statement_lines.append(replace(line, '£', '').split())
        elif 'CR' in line:
            statement_lines.append(replace(line, 'CR', '+').split())
        else:
            statement_lines.append(line.split())

for field in statement_lines[:]:
    descr = ""
    for v in field[4:-2]:
        descr = descr + v + " "
    if float(field[-2]) > 0:
        result = (convert_date(field[0], field[1], args.year), "NEXT Directory" ,descr, field[-2], "")
    else:
        result = (convert_date(field[0], field[1], args.year), "NEXT Directory" ,descr, "", field[-2].strip("-"))
    linewriter.writerow(result)

