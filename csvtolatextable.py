import sys
import argparse
import pandas as pd


precision = 3
nth = 3
# colors = ["{\cellcolor{green!20}}", "{\cellcolor{orange!20}}",
# "{\cellcolor{yellow!20}}"]
colors = ["{\cellcolor{blue!20}}", "{\cellcolor{green!20}}",
          "{\cellcolor{yellow!20}}"]
smallest = False
fulldocument = False


def create_header(data_frame):
    rows_string = ''
    if fulldocument:
        rows_string = r'\documentclass[landscape]{article}' + '\n' +\
            r'\usepackage{xcolor}' + '\n' + r'\usepackage{colortbl}' + '\n' +\
            r'\begin{document}' + '\n'
        rows_string = rows_string + r'\noindent\makebox[\textwidth]{' + '\n'
    rows_string = rows_string + r'\begin{tabular}{' + '|c' * \
        data_frame.shape[1] + '|}\n' + '\\hline \n'
    rows_string = rows_string + " & ".join(data_frame.columns.values.tolist())\
        + r'\\ ' + '\hline \n'
    return rows_string


def get_nth_largest_values(data_frame, dataset, nth, number_of_rows):
    nlargestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).\
        nlargest(nth).unique()
    count = nth
    while len(nlargestValues) != nth and count <= number_of_rows:
        count = count + 1
        nlargestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).\
            nlargest(count).unique()
    return nlargestValues


def get_nth_smallest_values(data_frame, dataset, nth, number_of_rows):
    nsmallestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).\
        nsmallest(nth).unique()
    count = nth
    while len(nsmallestValues) != nth and count <= number_of_rows:
        count = count + 1
        nsmallestValues = pd.to_numeric(data_frame.iloc[dataset][1:]).\
            nsmallest(count).unique()
    return nsmallestValues


def get_latex_string(data_frame, nth, variance_frame=None):
    number_of_rows = data_frame.shape[0]
    rows_string = create_header(data_frame)
    for dataset in range(number_of_rows):
        if smallest:
            nValues = get_nth_smallest_values(data_frame, dataset, nth,
                                              number_of_rows)
        else:
            nValues = get_nth_largest_values(data_frame, dataset, nth,
                                             number_of_rows)
        for value in range(len(data_frame.iloc[dataset])):
            delimiter_char = r' & '
            if value == len(data_frame.iloc[dataset]) - 1:
                delimiter_char = r'\\' + '\n'
            if value == 0:
                rows_string = rows_string + data_frame.iloc[dataset][value] + \
                    delimiter_char
            else:
                cellvalue = data_frame.iloc[dataset][value]
                if variance_frame is not None:
                    varvalue = variance_frame.iloc[dataset][value]
                extreme_value = False
                for i in range(len(nValues)):
                    if cellvalue == nValues[i]:
                        cellvalue = "{num:.{prec}f}".format(
                            num=data_frame.iloc[dataset][value],
                            prec=precision)
                        if variance_frame is not None:
                            varvalue = "{num:.{prec}f}".format(
                                num=variance_frame.iloc[dataset][value],
                                prec=precision)
                            rows_string = rows_string + colors[i] +\
                                cellvalue + " (" + varvalue +\
                                ")" + delimiter_char
                        else:
                            rows_string = rows_string + colors[i] +\
                                cellvalue + delimiter_char
                        extreme_value = True
                        break
                if not extreme_value:
                    cellvalue = "{num:.{prec}f}".format(
                        num=data_frame.iloc[dataset][value], prec=precision)
                    if variance_frame is not None:
                        varvalue = "{num:.{prec}f}".format(
                            num=variance_frame.iloc[dataset][value],
                            prec=precision)
                        rows_string = rows_string + cellvalue + " (" +\
                            varvalue + ")" + delimiter_char
                    else:
                        rows_string = rows_string + cellvalue +\
                            delimiter_char
    rows_string = rows_string + '\\hline \n \\end{tabular}'
    if fulldocument:
        rows_string = rows_string + '}\n'
        rows_string = rows_string + '\n' + r'\end{document}'
    return rows_string


def main():
    global smallest
    global nth
    global precision
    global fulldocument
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("inputpath", help="the path to the .csv table")
    parser.add_argument("outputpath", help="the path where you want the"
                        ".tex file")
    parser.add_argument("-s", "--smallest", action="store_true",
                        help="highlight smallest, default is largest")
    parser.add_argument("-p", "--precision", type=int, help="decimal precision"
                        ",default is 3")
    parser.add_argument("-n", "--nelements", type=int, help="highlight largest"
                        "/smallest, secondlargest/smallest, ..., "
                        "nthlargest/smallest.\n Must be between 1 and 3")
    parser.add_argument("-f", "--full", action="store_true", help="creates a "
                        "complete .tex document, rather than only the tabular"
                        "statement")
    parser.add_argument("--variance", help="file containing variance values,"
                        "that will be added after values in brackets")
    args = parser.parse_args()
    if args.smallest:
        smallest = True
    if args.precision is not None:
        precision = args.precision
    if args.nelements:
        if args.nelements > 3 or args.nelements < 1:
            print "nelements must be between 1 and 3!"
            sys.exit(2)
        nth = args.nelements
    if args.full:
        fulldocument = True

    # Read
    data_frame = pd.read_csv(args.inputpath, sep='\t')
    data_frame = data_frame.round(precision)

    if args.variance:
        variance_frame = pd.read_csv(args.variance, sep='\t')
        variance_frame = variance_frame.round(precision)
        result = get_latex_string(data_frame, nth, variance_frame)
    else:
        result = get_latex_string(data_frame, nth)

    # Write result
    with open(args.outputpath, 'w') as out_file:
        out_file.write(result)


if __name__ == "__main__":
        main()
