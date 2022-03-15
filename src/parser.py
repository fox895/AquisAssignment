import argparse

parser = argparse.ArgumentParser("Process record data")
parser.add_argument(
    '-i',
    '--input',
    help= "Input file path. Expects only 1 file.",
    default='pretrade_current.txt',
    dest='inputfile'
    )
parser.add_argument(
    '-o',
    '--output',
    help= "Output file path.",
    default='aggregate_output.tsv',
    dest='outputfile'
    )
