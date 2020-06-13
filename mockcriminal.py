#!/usr/bin/env python
from __future__ import print_function
try:
    input = raw_input
    range = xrange
except NameError:
    pass
__doc__ = """\
mockcriminal.py

Usage:    mockcriminal.py < sample.csv
"""
import csv
import sys
from random import choice, shuffle, sample

fname = { 0:"PID",
          1:"firstname",
          2:"lastname",
          3:"address",
          4:"city",
          5:"state",
          6:"zip",
          7:"dob_y",
          8:"dob_m",
          9:"dob_d",
          10:"recordstate",
          11:"recordid",
          12:"recordcounty",
          13:"dob",
          14:"agemin",
          15:"agemax",
          16:"fieldinc",
          17:"fieldexc" }
# EID,name_first,name_last,addr_complete,addr_city,addr_state,addr_zip,dob_y,dob_m,dob_d,source_state,case_number,search_county
shifts = {"person":0,
          "property":1,
          "bankrupt":2,
          "death":3,
          "vehicle":4,
          "criminal":5,
          "boat":6,
          "plane":7,
          "employment":8}

nosingle = set([1,2,4,5,13,14,15,16,17])

subfields = sorted(list(set(range(len(fname))) - set([0,3,4,5,6,13,14,15,16])))
nsub = len(subfields)+1

# byte reversal
def PIDstr(i):
    i ^= 0x80 << 56             # flip sign bit
    result = 'PID:0x'
    for j in range(8):
        result += '{:02x}'.format(i & 0xFF)
        i >>= 8
    return result

# Ignore first line of stdin:
line = readline(sys.stdin)

# Process remainder
for i, line in enumerate(csv.reader(sys.stdin,skipinitialspace=True)):
    coin = choice(range(10))
    # handle leading zeros in SSN:
    field = [foo.strip('"') for foo in line]
    if (coin < 1):
        print('PID:' + field[0])
    else:
        # compress dob_y,dob_m,dob_d fields down to DOB:
        try:
            dob_y = "{:4}".format(int(field[4]))
        except:
            dob_y = '    '
        try:
            dob_m = "{:02}".format(int(field[5]))
        except:
            dob_m = '  '
        try:
            dob_d = "{:02}".format(int(field[6]))
        except:
            dob_d = '  '
        dob = dob_y + dob_m + dob_d
        field += [dob]
        nsamp = 1
        sampj = set([1])
        while (nsamp == 1 and any(k in sampj for k in nosingle)):
            nsamp = choice(range(1,nsub))
            sampj = set([j for j in sample(subfields,nsamp)])
        if 11 in sampj:     # ssn
            flip = choice(range(10))
            if flip < 1:
                field[11] = field[11][:5]
            elif flip < 2:
                field[11] = field[11][5:]
        #if 10 in sampj:     # zip
        #    flip = choice(range(10))
        #    if flip < 1:
        #        field[10] = field[10][:2]
        #    elif flip < 2:
        #        field[10] = field[10][:3]
        if 12 in sampj:     # dob
            flip = choice(range(10))
            if flip < 1:
                try:
                     agemin = str(2010 - int(dob_y))
                except:
                     agemin = '20'
                field += [agemin]
                sampj.remove(12)
                sampj.add(13)
            elif flip < 2:
                try:
                     agemax = str(2020 - int(dob_y))
                except:
                     agemax = '90'
                field += ['0',agemax]
                sampj.remove(12)
                sampj.add(14)
            elif flip < 3:
                try:
                     agemin = str(2010 - int(dob_y))
                except:
                     agemin = '20'
                try:
                     agemax = str(2020 - int(dob_y))
                except:
                     agemax = '90'
                field += [agemin,agemax]
                sampj.remove(12)
                sampj.add(13)
                sampj.add(14)
            elif flip < 4:
                field[12] = dob_y + '  ' + '  '
            elif flip < 5:
                field[12] = dob_y + dob_m + '  '

        flip_for_sample = choice(range(10))
        if flip_for_sample < 1:
            fieldinc = 0
            fieldexc = 0
            while len(field) < 15:
                field += [""]

            flip_for_bits = choice(range(10))
            if flip_for_bits < 4:
                fieldinc |= 1 << shifts["property"]
            elif flip_for_bits < 6:
                fieldinc |= 1 << shifts["bankrupt"]
            elif flip_for_bits < 8:
                fieldinc |= 1 << shifts["death"]

            flip_for_bits = choice(range(10))
            if flip_for_bits < 4:
                fieldexc |= 1 << shifts["employment"]
            elif flip_for_bits < 6:
                fieldexc |= 1 << shifts["criminal"]
            elif flip_for_bits < 8:
                fieldexc |= 1 << shifts["vehicle"]
            field += ["0x%0.8x" % fieldinc]
            field += ["0x%0.8x" % fieldexc]
            sampj.add(15)
            sampj.add(16)

        nonblanksampj = [j for j in sampj if field[j].strip()]
        nnblankj = len(nonblanksampj)
        if ((nnblankj < 1) or
            (nnblankj == 1 and
              any(k in nonblanksampj for k in nosingle))):
            pass
        else:
            print(','.join([fname[j] + ":" + field[j]
                            for j in nonblanksampj]))
