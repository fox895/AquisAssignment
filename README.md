# AquisAssignment
Repository for the handson test by AquisExchange

## Installation
 - Create a virtual environment (eg `python -m venv venv`)
 - Activate it (on *Nix systems: `$ source venv/bin/activate`, on Windows: ``)
 - Once activated install required packages: `pip install -r requirements.txt`


Entrypoint file is `main.py`. The script expects an input file called `pretrade_current.txt` and generates an output file called `aggregate_output.tsv`


I created a couple of ausiliary modules to better split all the functions I have been using.
This improve a bit readability and understanding of this simple code base.
The file `src/utils.py` containes the fucntions used to parse the data from the text file,
while `src/data_process.py` contains the function that have been used to manipulate the DataFrames.

The jupyter notebook `exploration.ipynb` contains a draft version of all the functions and many tests performed
in order to parse correctly the data and to properly manipulated the DataFrames.
