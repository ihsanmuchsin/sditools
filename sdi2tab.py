#!/usr/bin/env python3

''' Ihsan Muchsin, Bjorn Pieper. Nov 2017 - . Insertion, Deletion, and SNP'''

from argparse import ArgumentParser
from sys import argv, exit
import glob
import os
import gzip

p = ArgumentParser(prog='sdi2tab', description='Produce an InDel plus SNP table from sdi files.')
p.add_argument('-sdi', metavar='<String>', help='Path containing the sdi files',
               required=True)
p.add_argument('-ref', metavar='<String>', help='Name of the reference strain'+\
               ' used for the alignment in the sdi files', 
               required=True)
p.add_argument('-chr', metavar='<String>', help='Provide the value of the '+\
               'chromosome to process as it occurs in the sdi files', 
               required=True)
p.add_argument('-out', metavar='<string>', help='Output file name', 
               required=True)
p.add_argument('-gz', help='The input files are in gzip format', default=False, action='store_true')
p._optionals.title='options'

if len(argv) == 1:
    p.print_help()
    exit(0)

args = p.parse_args()

if not args.sdi[-1] == '/':
    args.sdi = args.sdi + '/'

# init variables
chrname = args.chr
sdifolder = args.sdi
refname = args.ref
outfile = args.out

# create dictionary
variation = dict()
reference = dict()

names = []

for f in glob.glob(sdifolder+'*'):
    
    fname = os.path.basename(f)
    names.append(fname)
    
    if args.gz:
        fin = gzip.open(f, 'rt')
    else:
        fin = open(f, 'r')
    
    for line in fin.readlines():
        
        le = line.split('\t')
        chrom = le[0]
        pos = int(le[1])
        ref = le[3]
        var = le[4]
        
        if chrom==chrname:
            
            if pos not in variation.keys():
                variation[pos] = dict()
                variation[pos].update({fname:var})
            else:
                variation[pos].update({fname:var})
                
            if pos not in reference.keys():
                reference[pos] = ref
    fin.close()
                
names = sorted(names)

# write the output
fout = open(outfile, 'w')

print ('chromosome', 'position', refname, '\t'.join(names), sep='\t', file=fout)

keys = sorted(list(reference.keys()))
for k in keys:
    wref = reference[k]
    wvar = []
    for n in names:
        try:
            tvar = variation[k][n]
        except KeyError:
            tvar = reference[k]
        wvar.append(tvar)
        
    print (chrname, k, wref, '\t'.join(wvar), sep='\t', file=fout)
    
fout.close()