#!/usr/bin/env python3

''' Ihsan Muchsin, Bjorn Pieper. Nov 2017 - . Insertion, Deletion, and SNP'''

from argparse import ArgumentParser
from sys import argv, exit
import glob
import os
import gzip

# define the function
def sdi2csv(args):

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

    print ('chromosome', 'position', refname, ','.join(names), sep=',', file=fout)

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

        print (chrname, k, wref, ','.join(wvar), sep=',', file=fout)

    fout.close()

def clean_indel_table(infile, outfile, min_length, acc_letters):

    fout = open(outfile, 'w')
    fin = open(infile, 'r')

    line_count = 0

    while True:

        line_count += 1

        line = fin.readline()

        if line_count==1:
            print (line.strip(), file=fout)
            continue

        if not line:
            break

        line_elem = line.strip().split(',')

        n_check = False
        max_elem_len = 0

        for i in range (2, len(line_elem)):
            elem_len = len(line_elem[i])
            if max_elem_len < elem_len:
                max_elem_len = elem_len

            for char in line_elem[i]:
                if char.upper() not in acc_letters:
                    n_check = True
                    break

        if max_elem_len > min_length and n_check==False:
            print (','.join(line_elem), file=fout)

    fin.close()
    fout.close()

def cleantable(args):
    if not args.indel[-1] == '/':
        args.indel = args.indel + '/'

    if not args.out[-1] == '/':
        args.out = args.out + '/'

    # init variables
    infolder = args.indel
    min_length = args.length
    outfolder = args.out

    # accepted letters
    acc_letters = ['A', 'T', 'G', 'C', '-']

    # create the outfolder
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    # run the function
    for f in glob.glob(infolder+'*'):

        infile = f
        fname = os.path.basename(f)
        outfile = outfolder + fname

        clean_indel_file(infile, outfile, min_length, acc_letters)

def convert_indel_to_float(infile, outfile):
    pass

# create parser
p = ArgumentParser(prog='sditools', description='Tools for .sdi files processing')

subp = p.add_subparsers()

p_csv = subp.add_parser('sdi2csv', help='Convert .sdi to an indel table stored as .csv file')
p_csv.add_argument('-sdi', metavar='<String>', help='Path of the sdi folder',
               required=True)
p_csv.add_argument('-ref', metavar='<String>', help='Name of the reference strain'+\
               ' used for the alignment in the sdi files', 
               required=True)
p_csv.add_argument('-chr', metavar='<String>', help='Provide the value of the '+\
               'chromosome to process as it occurs in the sdi files', 
               required=True)
p_csv.add_argument('-out', metavar='<string>', help='Output file name', 
               required=True)
p_csv.add_argument('-gz', help='The input files are in gzip format', default=False, action='store_true')
p_csv.set_defaults(func=sdi2csv)

p_clean = subp.add_parser('cleantable', help='Clean indel tables')
p_clean.add_argument('-indel', metavar='<String>', help='Path of the indel table folder',
               required=True)
p_clean.add_argument('-length', metavar='<Integer>', help='Minimum length for the indel',
               required=True, type=int)
p_clean.add_argument('-out', metavar='<String>', help='Output folder name', 
               required=True)
p_clean.set_defaults(func=cleantable)


if len(argv) == 1:
    p.print_help()
    exit(0)

if len(argv) == 2:
    if argv[1] == 'sdi2csv':
        p_csv.print_help()
    elif argv[1] == 'cleantable':
        p_clean.print_help()
    exit(0)

args = p.parse_args()

args.func(args)
