## ColorizeLaTexTables: small script to get color coded latex tables from csv files or pandas DataFrames
![colorized table](images/bigtable.png)
# Installation
Install via pip:
```
pip install colorizelatextables
```
# Dependencies
Only necessary dependency is pandas, seaborn is recommended for color palettes:
```
pip install pandas
pip install seaborn
```
# Usage:
You can either use the script or use the module
## Script
```
colorize_table.py examples/BigTable.csv bigtable.tex
```
You can also use seaborn palette names if you have seaborn
```
colorize_table.py --palette "GnBu_r" examples/BigTable.csv bigtable.tex
```
### Options:
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
## Module
```
from colorizelatextables import to_colorized_latex
table_string, defined_colors = to_colorized_latex(df, sns.color_palette("GnBu_d",n_colors=3))
```
You can also provide additional keyword arguments that are passed to pandas [to_latex()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_latex.html) function, e.g.
```
table_string, defined_colors = to_colorized_latex(df, sns.color_palette("GnBu_d",n_colors=3), column_format="|c|c|c|c|c|c|c|c|c|")
```
