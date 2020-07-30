#!/usr/bin/python3
import sys, argparse
from os import path, getcwd, walk, listdir
from glob import glob
import pdb

def convert_vp2_to_wav(inputfile=None,directory=None,recurse=False,outputdir=None):
    # RIFF in ascii
    wav_header = b'\x52\x49\x46\x46'
    files = list()
    if inputfile is None and directory is None:
        raise ValueError("Must specify either a file or a directory of files to process")
    if inputfile is not None:
        files = [inputfile]
    elif directory is not None:
        if recurse:
            files = [y for x in walk(directory) for y in glob(path.join(x[0],'*.vp2'))]
        else:
            files = [path.join(directory,x) for x in listdir(directory) if x.endswith(".vp2")]
    if outputdir == None:
        outputdir = getcwd()
    if len(files) == 0:
        raise FileNotFoundError("Could not find any .vp2 files with the given parameters.")
    for vp2file in files:
        outputfile = path.join(outputdir,path.basename(vp2file).replace(".vp2",".wav"))
        # just strip the bogus metadata
        with open(vp2file,'rb') as file:
            content = file.read()
        start_index = content.find(wav_header)
        new_content = content[start_index:]
        with open(outputfile,"wb") as file:
            file.write(bytes(new_content))


def main():
    parser = argparse.ArgumentParser(
        add_help=False,
        description=
        '''Convert files from .vp2 to .wav format''',
        formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=40)
    )

    parser.add_argument('-f', '--inputfile', type=str, metavar="STRING", default=None, help="Convert the specicied file.")
    parser.add_argument('-d', '--directory', type=str, metavar="STRING", default=None, help="Convert all files in the directory specified.")
    parser.add_argument('-r', '--recurse', action='store_true', help="If directory is specified, recurse through it. (default: False)")
    parser.add_argument('-o', '--outputdir', type=str, metavar="STRING", default=None, help="Directory to write the output to. Files will be renamed to <filename>.wav. (default: current dir)")
    
    if len(sys.argv) >= 2 and sys.argv[1] in ('-h','--help'):
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    convert_vp2_to_wav(inputfile=args.inputfile,directory=args.directory,recurse=args.recurse,outputdir=args.outputdir)
    sys.exit(0)

if __name__ == '__main__':
    main()