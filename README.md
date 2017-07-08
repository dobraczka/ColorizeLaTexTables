## CSVtoLaTeXTable: small script to get color coded latex tables from csv files
# Dependencies
Only dependency is pandas:
```
pip install pandas
```
# Example usage:
```
python csvtolatextable.py examples/BigTable.csv bigtable.tex
```
# Result:
![colorized table](images/bigtable.png)

# Options:
```
usage: csvtolatextable.py [-h] [-s] [-p PRECISION] [-n NELEMENTS] [-f]
                          inputpath outputpath

positional arguments:
  inputpath             the path to the .csv table
  outputpath            the path where you want the .tex file

optional arguments:
  -h, --help            show this help message and exit
  -s, --smallest        highlight smallest, default is largest
  -p PRECISION, --precision PRECISION
                        decimal precision, default is 3
  -n NELEMENTS, --nelements NELEMENTS
                        highlight largest/smallest, secondlargest/smallest,
                        ..., nthlargest/smallest. Must be between 1 and 3
  -f, --full            creates a complete .tex document, rather than only the
                        tabular statement
```
