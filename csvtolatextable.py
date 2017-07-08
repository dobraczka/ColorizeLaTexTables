import sys, argparse
import pandas as pd
 
precision = 3
colors = ["{\cellcolor{green!20}}","{\cellcolor{orange!20}}","{\cellcolor{yellow!20}}"]
nth = 3


def get_nth_largest_values(data_frame, dataset, nth, number_of_columns):
    nlargestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).nlargest(nth).unique()
    count = nth
    while len(nlargestValues) != nth and count <= number_of_columns:
        count = count + 1
        nlargestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).nlargest(count).unique()
    return nlargestValues

def get_nth_smallest_values(data_frame, dataset, nth):
    nsmallestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).nsmallest(nth).unique()
    count = nth
    while len(nsmallestValues) != nth and count <= number_of_columns:
        count = count + 1
        nsmallestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).nsmallest(count).unique()
    return nsmallestValues

def get_latex_string(data_frame, nth):
    rows_string = ''
    number_of_columns = len(data_frame.columns)
    rows_string = rows_string + r'\begin{tabular}{' + 'c' * number_of_columns + '}\n' + '\\hline \n'
    rows_string = rows_string + " & ".join(data_frame.columns.values.tolist()) + r'\\ ' + '\hline \n'
    for dataset in range(number_of_columns):
        nlargestValues = get_nth_largest_values(data_frame, dataset, nth, number_of_columns)
        for value in range(len(data_frame.iloc[dataset])):
            delimiter_char = r' & '
            if value == len(data_frame.iloc[dataset]) -1:
                delimiter_char = r'\\' + '\n'
            if value==0:
                rows_string = rows_string + data_frame.iloc[dataset][value] + delimiter_char
            else:
                cellvalue = data_frame.iloc[dataset][value]
                extreme_value = False
                for i in range(len(nlargestValues)):
                    if cellvalue==nlargestValues[i]:
                        rows_string = rows_string + colors[i] + str(cellvalue) + delimiter_char
                        extreme_value = True
                        break
                if not extreme_value:
                    rows_string = rows_string + str(cellvalue) + delimiter_char
    rows_string = rows_string + '\\hline \n \\end{tabular}'
    return rows_string


def main():
    #Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("inputpath", help="the path to the .csv table")
    parser.add_argument("outputpath", help="the path where you want the .tex file")
    args = parser.parse_args()

    #Read
    data_frame = pd.read_csv(args.inputpath,sep='\t')
    data_frame = data_frame.round(precision)

    #Get latex string
    result = get_latex_string(data_frame, nth)

    #Write result
    with open(args.outputpath, 'w') as out_file:
        out_file.write(result)

if __name__ == "__main__":
        main()
