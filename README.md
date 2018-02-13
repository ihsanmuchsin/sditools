# sditools
usage: sditools [-h] {sdi2indel,cleantable,indel2float,decisiontree} ...

Tools for .sdi files processing

positional arguments:
  {sdi2indel,cleantable,indel2float,decisiontree}
    sdi2indel           Convert .sdi to an indel table stored as .csv file
    cleantable          Clean indel tables
    indel2float         Convert values in indel table to float
    decisiontree        Make the decision tree

optional arguments:
  -h, --help            show this help message and exit

# sdi2indel
usage: sditools sdi2indel [-h] -sdi <String> -ref <String> -chr <String> -out
                          <string> [-gz]

optional arguments:
  -h, --help     show this help message and exit
  -sdi <String>  Path of the sdi folder
  -ref <String>  Name of the reference strain used for the alignment in the
                 sdi files
  -chr <String>  Provide the value of the chromosome to process as it occurs
                 in the sdi files
  -out <string>  Output file name
  -gz            The input files are in gzip format

# cleantable
usage: sditools cleantable [-h] -indel <String> -length <Integer> -out
                           <String>

optional arguments:
  -h, --help         show this help message and exit
  -indel <String>    Path of the indel table folder
  -length <Integer>  Minimum length for the indel
  -out <String>      Output folder name

# indel2float
usage: sditools indel2float [-h] -indel <String> -out <String>

optional arguments:
  -h, --help       show this help message and exit
  -indel <String>  Path of the indel table folder
  -out <String>    Output folder name

# decisiontree
usage: sditools decisiontree [-h] -indel <String> [-features <String>]
                             [-depth <String>] -out <String>

optional arguments:
  -h, --help          show this help message and exit
  -indel <String>     Path of the indel table folder
  -features <String>  Maximum features of the tree
  -depth <String>     Maximum depth of the tree
  -out <String>       Output folder name
