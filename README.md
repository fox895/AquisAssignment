# AquisAssignment
Repository for the handson test by AquisExchange.
Python version tested with 3.8.12 and 3.10.2

## Installation
 - Create a virtual environment (eg `python -m venv venv`)
 - Activate it (on *Nix systems: `$ source venv/bin/activate`, on Windows: ``)
 - Once activated install required packages: `pip install -r requirements.txt`

To run the script execute:
```
python main.py
```
By default the scripts expects a file called `pretrade_current.txt` and will generate a tsv file called `aggregate_output.tsv`.
To customize these options the `-i`/`--input` and `-o`/`--output` flags can be used.
```
python main.py -h
usage: Process record data [-h] [-i INPUTFILE] [-o OUTPUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --input INPUTFILE
                        Input file path. Expects only 1 file.
  -o OUTPUTFILE, --output OUTPUTFILE
                        Output file path.
```

## Notes

I created a couple of ausiliary modules to better split all the functions I have been using.
This improve a bit readability and understanding of this simple code base.
The file `src/utils.py` containes the fucntions used to parse the data from the text file,
while `src/data_process.py` contains the function that have been used to manipulate the DataFrames.

The jupyter notebook `exploration.ipynb` contains a draft version of all the functions and many tests performed
in order to parse correctly the data and to properly manipulated the DataFrames.
