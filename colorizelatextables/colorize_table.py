#!/usr/bin/env python3

import sys
import argparse
import pandas as pd
import ast
from typing import List, Tuple

default_color_palettes = {
    2: [
        (0.21568627450980393, 0.5294117647058824, 0.7542483660130719),
        (0.6718954248366014, 0.8143790849673203, 0.9006535947712418),
    ],
    3: [
        (0.1271049596309112, 0.4401845444059977, 0.7074971164936563),
        (0.41708573625528644, 0.6806305267204922, 0.8382314494425221),
        (0.7752402921953095, 0.8583006535947711, 0.9368242983467897),
    ],
    4: [
        (0.09019607843137256, 0.39294117647058824, 0.6705882352941177),
        (0.2909803921568628, 0.5945098039215686, 0.7890196078431373),
        (0.5796078431372549, 0.7701960784313725, 0.8737254901960784),
        (0.8141176470588235, 0.883921568627451, 0.9498039215686275),
    ],
    5: [
        (0.06251441753171857, 0.35750865051903113, 0.6429065743944637),
        (0.21568627450980393, 0.5294117647058824, 0.7542483660130719),
        (0.41708573625528644, 0.6806305267204922, 0.8382314494425221),
        (0.6718954248366014, 0.8143790849673203, 0.9006535947712418),
        (0.8406920415224913, 0.9016378316032295, 0.9586620530565167),
    ],
    6: [
        (0.044059976931949255, 0.3338869665513264, 0.6244521337946944),
        (0.16696655132641292, 0.48069204152249134, 0.7291503267973857),
        (0.32628988850442137, 0.6186236063052672, 0.802798923490965),
        (0.5356862745098039, 0.746082276047674, 0.8642522106881968),
        (0.7309496347558632, 0.8394771241830065, 0.9213225682429834),
        (0.8584083044982699, 0.9134486735870818, 0.9645674740484429),
    ],
    7: [
        (0.03137254901960784, 0.3140945790080738, 0.606489811610919),
        (0.1271049596309112, 0.4401845444059977, 0.7074971164936563),
        (0.25628604382929643, 0.5700115340253749, 0.7751633986928105),
        (0.41708573625528644, 0.6806305267204922, 0.8382314494425221),
        (0.6172549019607844, 0.7908650519031142, 0.8818454440599769),
        (0.7752402921953095, 0.8583006535947711, 0.9368242983467897),
        (0.8702191464821223, 0.9213225682429834, 0.9685044213763937),
    ],
    8: [
        (0.03137254901960784, 0.301914648212226, 0.588404459823145),
        (0.10557477893118032, 0.41262591311034214, 0.6859669357939254),
        (0.21568627450980393, 0.5294117647058824, 0.7542483660130719),
        (0.34646674356016915, 0.632402921953095, 0.8106728181468666),
        (0.5105882352941177, 0.7323029603998462, 0.8588389081122645),
        (0.6718954248366014, 0.8143790849673203, 0.9006535947712418),
        (0.7993540945790081, 0.8740792003075739, 0.944882737408689),
        (0.8825067281814687, 0.929196462898885, 0.9724413687043445),
    ],
    9: [
        (0.03137254901960784, 0.2897347174163783, 0.570319108035371),
        (0.09019607843137256, 0.39294117647058824, 0.6705882352941177),
        (0.1791464821222607, 0.49287197231833907, 0.7354248366013072),
        (0.2909803921568628, 0.5945098039215686, 0.7890196078431373),
        (0.41708573625528644, 0.6806305267204922, 0.8382314494425221),
        (0.5796078431372549, 0.7701960784313725, 0.8737254901960784),
        (0.7161860822760477, 0.8332026143790849, 0.916155324875048),
        (0.8141176470588235, 0.883921568627451, 0.9498039215686275),
        (0.8917339484813533, 0.9351018838908112, 0.9753940792003075),
    ],
}


def _create_color_palette(rgb_list):
    defined = []
    color_proxy = []
    colors = []
    it = 1
    prefix = "rankcolor"
    for color in rgb_list:
        cname = prefix + str(it)
        defined.append(
            "\definecolor{"
            + cname
            + "}{rgb}{"
            + ",".join([str(v) for v in color])
            + "}"
        )
        color_proxy.append(cname)
        it += 1
        colors.append("{\cellcolor{" + cname + "}}")
    return defined, color_proxy, colors


def _colorize(row, n, precision, ascending, color_proxy):
    # test if contains numeric
    if not pd.to_numeric(row, errors="coerce").notnull().all():
        return row
    row = pd.to_numeric(row).round(precision)
    ranks = row.rank(ascending=ascending)
    colored_ranks = ranks.drop_duplicates().nsmallest(n).to_list()
    for row_entry, r in zip(row.items(), ranks):
        i, e = row_entry
        if r in colored_ranks:
            row[i] = color_proxy[colored_ranks.index(r)] + str(e)
        else:
            row[i] = str(e)
    return row


def to_colorized_latex(
    df: pd.DataFrame,
    colors_rgb: List[Tuple[float]],
    precision=3,
    ascending=False,
    columnwise=False,
    **latex_kwargs,
) -> (str, str):
    """Transforms pandas DataFrame to colorized LaTex table, with cells colored based on cell rank.

    Parameters
    ----------
    df : DataFrame
        DataFrame that will be transformed
    colors_rgb : List [Tuple[float]]
        colors that will be used to color cells in rank order.
        It is recommended to use this to pass seaborn color palettes e.g.
        ``sns.color_palette("Greens_r",n_colors=n))``
    precison: int
        Number of decimals to which the DataFrame will be rounded
    ascending: bool, default False
        Whether or not the elements should be ranked in ascending order.
    columnwise: bool, default False
        if True, calculate column-wise rank, else row-wise rank
    kwargs: key, value mappings
        Other keyword arguments are passed down to ``pandas.DataFrame.to_latex()``.

    Returns
    -------
    table_string: str
        string representation of latex table
    defined_colors: str
        latex definition of used colors
    """
    axis = 0 if columnwise else 1
    defined, color_proxy, colors = _create_color_palette(colors_rgb)
    string_df = df.apply(
        _colorize, args=(len(color_proxy), precision, ascending, color_proxy), axis=axis
    )
    latex_str = string_df.to_latex(**latex_kwargs)
    for p, c in zip(color_proxy, colors):
        latex_str = latex_str.replace(p, c)
    return latex_str, defined


def main():
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("inputpath", help="the path to the .csv table")
    parser.add_argument(
        "outputpath",
        help="the path where you want the" ".tex file",
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "-a",
        "--ascending",
        action="store_true",
        help="highlight from smallest to largest, default is descending",
    )
    parser.add_argument(
        "--precision", type=int, help="decimal precision" ",default is 3", default=3,
    )
    parser.add_argument(
        "-n", "--nranks", type=int, help="number of ranks to highlight", default=3,
    )
    parser.add_argument(
        "--colors",
        type=str,
        help="rgb_codes as list of float triples. if you have seaborn it is recommended to use the --palette option",
    )
    parser.add_argument("--palette", type=str, help="seaborn color palette name")
    parser.add_argument(
        "-f",
        "--full",
        action="store_true",
        help="creates a "
        "complete .tex document, rather than only the tabular "
        "statement",
        default=False,
    )
    parser.add_argument(
        "--seperator", help="seperator of csv, comma is default", default=","
    )
    parser.add_argument(
        "--columnwise",
        help="calculate columnwise rank rather than rowwise rank",
        action="store_true",
    )
    args = parser.parse_args()
    if args.colors:
        colors_rgb = ast.literal_eval(args.colors)
        if args.nranks != len(colors_rgb):
            print(
                f"Warning! Number of colors ({len(colors_rgb)}) and n ({args.nranks})are not equal!"
            )
    elif args.palette:
        import seaborn as sns

        colors_rgb = sns.color_palette(args.palette, n_colors=args.nranks)
    else:
        try:
            colors_rgb = default_color_palettes[args.nranks]
        except KeyError:
            print(
                "No default palette with {args.nelements} values available, please provide list of rgb colorcodes"
            )
            sys.exit(2)

    # Read
    data_frame = pd.read_csv(args.inputpath, sep=args.seperator, index_col=0, header=0)
    data_frame = data_frame.round(args.precision)

    result, defined = to_colorized_latex(
        data_frame, colors_rgb, args.precision, args.ascending, args.columnwise,
    )

    if args.full:
        result = (
            r"\documentclass[landscape]{article}"
            + "\n"
            + r"\usepackage{xcolor}"
            + "\n"
            + r"\usepackage{booktabs}"
            + "\n"
            + r"\usepackage{colortbl}"
            + "\n"
            + "\n".join(defined)
            + "\n"
            + r"\begin{document}"
            + "\n"
            + r"\noindent\makebox[\textwidth]{"
            + "\n"
            + result
            + "}\n"
            + "\n"
            + r"\end{document}"
        )

    if args.outputpath is None:
        print(result)
    else:
        # Write result
        with open(args.outputpath, "w") as out_file:
            out_file.write(result)


if __name__ == "__main__":
    main()
