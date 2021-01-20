import pytest
import pandas as pd
import seaborn as sns
from colorizelatextables.colorize_table import to_colorized_latex as colat

expected_multi = (
    r"\begin{tabular}{lllllllllllllllll}"
    + "\n"
    + r"\toprule"
    + "\n"
    + r" & framework & \multicolumn{3}{l}{A} & \multicolumn{3}{l}{B} & \multicolumn{3}{l}{C} & \multicolumn{3}{l}{D} & \multicolumn{3}{l}{E} \\"
    + "\n"
    + r"    & metric &                         fm &   prec &    rec &                         fm &   prec &    rec &                         fm &   prec &    rec &     fm &   prec &    rec &     fm &   prec &    rec \\"
    + "\n"
    + r" ds\_size & dataset &                            &        &        &                            &        &        &                            &        &        &        &        &        &        &        &        \\"
    + "\n"
    + r" \midrule"
    + "\n"
    + r" v1 & D1 &                      0.844 &  0.993 &  0.733 &                      0.837 &  0.989 &  0.726 &  {\cellcolor{rankcolor1}}0.926 &  0.907 &  0.945 &  0.815 &  0.907 &  0.741 &  0.812 &  0.896 &  0.742 \\"
    + "\n"
    + r"    & D2 &  {\cellcolor{rankcolor1}}0.959 &  0.987 &  0.934 &                      0.925 &  0.988 &  0.870 &                      0.936 &  0.924 &  0.949 &  0.836 &  0.925 &  0.762 &  0.831 &  0.897 &  0.774 \\"
    + "\n"
    + r"    & D3 &  {\cellcolor{rankcolor1}}0.996 &  0.997 &  0.995 &                      0.991 &  1.000 &  0.983 &                      0.992 &  0.990 &  0.994 &  0.984 &  0.994 &  0.974 &  0.983 &  0.991 &  0.974 \\"
    + "\n"
    + r"    & D4 &  {\cellcolor{rankcolor1}}0.997 &  0.995 &  0.998 &                      0.993 &  0.999 &  0.987 &                      0.993 &  0.993 &  0.994 &  0.985 &  0.983 &  0.987 &  0.984 &  0.982 &  0.987 \\"
    + "\n"
    + r"    & D5 &  {\cellcolor{rankcolor1}}0.983 &  0.993 &  0.974 &                      0.975 &  0.992 &  0.958 &                      0.972 &  0.971 &  0.972 &  0.968 &  0.990 &  0.946 &  0.967 &  0.988 &  0.946 \\"
    + "\n"
    + r"    & D6 &  {\cellcolor{rankcolor1}}0.988 &  0.994 &  0.983 &                      0.981 &  0.992 &  0.971 &                      0.975 &  0.972 &  0.978 &  0.968 &  0.993 &  0.945 &  0.966 &  0.987 &  0.946 \\"
    + "\n"
    + r"    & D7 &  {\cellcolor{rankcolor1}}0.977 &  0.994 &  0.961 &                      0.962 &  0.995 &  0.931 &                      0.956 &  0.959 &  0.953 &  0.947 &  0.988 &  0.910 &  0.946 &  0.985 &  0.911 \\"
    + "\n"
    + r"    & D8 &  {\cellcolor{rankcolor1}}0.976 &  0.991 &  0.962 &  {\cellcolor{rankcolor1}}0.976 &  0.990 &  0.963 &                      0.964 &  0.959 &  0.969 &  0.964 &  0.991 &  0.938 &  0.962 &  0.987 &  0.938 \\"
    + "\n"
    + r" v2 & D1 &  {\cellcolor{rankcolor1}}0.888 &  0.988 &  0.807 &                      0.861 &  0.991 &  0.762 &                      0.876 &  0.844 &  0.910 &  0.837 &  0.886 &  0.793 &  0.823 &  0.865 &  0.784 \\"
    + "\n"
    + r"    & D2 &  {\cellcolor{rankcolor1}}0.947 &  0.994 &  0.904 &                      0.927 &  0.992 &  0.870 &                      0.904 &  0.895 &  0.913 &  0.863 &  0.899 &  0.830 &  0.848 &  0.859 &  0.837 \\"
    + "\n"
    + r"    & D3 &  {\cellcolor{rankcolor1}}0.992 &  1.000 &  0.983 &                      0.991 &  0.998 &  0.985 &                      0.979 &  0.974 &  0.983 &  0.971 &  0.985 &  0.957 &  0.971 &  0.984 &  0.958 \\"
    + "\n"
    + r"    & D4 &  {\cellcolor{rankcolor1}}0.995 &  0.999 &  0.990 &  {\cellcolor{rankcolor1}}0.995 &  0.998 &  0.992 &                      0.986 &  0.985 &  0.987 &  0.974 &  0.972 &  0.977 &  0.974 &  0.973 &  0.976 \\"
    + "\n"
    + r"    & D5 &  {\cellcolor{rankcolor1}}0.978 &  0.993 &  0.964 &                      0.975 &  0.993 &  0.957 &                      0.971 &  0.976 &  0.966 &  0.969 &  0.992 &  0.948 &  0.962 &  0.977 &  0.948 \\"
    + "\n"
    + r"    & D6 &  {\cellcolor{rankcolor1}}0.982 &  0.989 &  0.975 &  {\cellcolor{rankcolor1}}0.982 &  0.995 &  0.970 &                      0.974 &  0.967 &  0.982 &  0.973 &  0.993 &  0.954 &  0.969 &  0.984 &  0.955 \\"
    + "\n"
    + r"    & D7 &  {\cellcolor{rankcolor1}}0.970 &  0.995 &  0.947 &                      0.969 &  0.995 &  0.944 &                      0.956 &  0.959 &  0.953 &  0.953 &  0.983 &  0.924 &  0.952 &  0.979 &  0.926 \\"
    + "\n"
    + r"    & D8 &                      0.959 &  0.989 &  0.930 &  {\cellcolor{rankcolor1}}0.987 &  0.992 &  0.983 &                      0.966 &  0.963 &  0.970 &  0.971 &  0.992 &  0.951 &  0.970 &  0.992 &  0.950 \\"
    + "\n"
    + r" \multicolumn{2}{c}{Avg Rank}  & \multicolumn{3}{c}{{\cellcolor{avgrankcolor1}}\textcolor{white}{1.500}} & \multicolumn{3}{c}{{\cellcolor{avgrankcolor2}}2.062} & \multicolumn{3}{c}{{\cellcolor{avgrankcolor3}}2.688} & \multicolumn{3}{c}{4.000} & \multicolumn{3}{c}{4.750}\\"
    + "\n"
    + "\n"
    + r" \bottomrule"
    + "\n"
    + r" \end{tabular}"
    + "\n"
)

expected_normal = (
    r"\begin{tabular}{lllllllll}"
    + "\n"
    + r"\toprule"
    + "\n"
    + r"{} &                          A &                          B &      C &                          D &                          E &                          F &      G &                          H \\"
    + "\n"
    + r"Data  &                            &                            &        &                            &                            &                            &        &                            \\"
    + "\n"
    + r"\midrule"
    + "\n"
    + r"data1 &  {\cellcolor{rankcolor1}}0.997 &                      0.763 &  0.795 &                      0.795 &  {\cellcolor{rankcolor1}}0.997 &                      0.993 &  0.909 &                      0.994 \\"
    + "\n"
    + r"data2 &                      0.997 &  {\cellcolor{rankcolor1}}0.999 &  0.971 &                      0.971 &                      0.956 &                      0.937 &  0.850 &                      0.930 \\"
    + "\n"
    + r"data3 &                      0.999 &  {\cellcolor{rankcolor1}}1.000 &  0.733 &                      0.535 &                      0.322 &  {\cellcolor{rankcolor1}}1.000 &  0.867 &                      0.977 \\"
    + "\n"
    + r"data4 &  {\cellcolor{rankcolor1}}0.999 &                      0.799 &  0.929 &  {\cellcolor{rankcolor1}}0.999 &                      0.919 &  {\cellcolor{rankcolor1}}0.999 &  0.926 &  {\cellcolor{rankcolor1}}0.999 \\"
    + "\n"
    + r"data5 &                      0.993 &  {\cellcolor{rankcolor1}}1.000 &  0.235 &                      0.386 &  {\cellcolor{rankcolor1}}1.000 &  {\cellcolor{rankcolor1}}1.000 &  0.937 &                      0.937 \\"
    + "\n"
    + r"data6 &  {\cellcolor{rankcolor1}}0.987 &                      0.986 &  0.986 &                      0.986 &                      0.980 &                      0.977 &  0.808 &                      0.858 \\"
    + "\n"
    + r"data7 &  {\cellcolor{rankcolor1}}0.660 &                      0.558 &  0.558 &                      0.558 &                      0.536 &                      0.536 &  0.361 &                      0.361 \\"
    + "\n"
    + r"data8 &  {\cellcolor{rankcolor1}}0.964 &                      0.940 &  0.939 &                      0.939 &                      0.952 &                      0.952 &  0.829 &                      0.875 \\"
    + "\n"
    + r"data9 &  {\cellcolor{rankcolor1}}0.732 &                      0.617 &  0.615 &                      0.615 &                      0.644 &                      0.660 &  0.369 &                      0.369 \\"
    + "\n"
    + r"Avg Rank & {\cellcolor{avgrankcolor1}}\textcolor{white}{1.833} & {\cellcolor{avgrankcolor3}}3.833 & 5.111 & 4.833 & 4.444 & {\cellcolor{avgrankcolor2}}3.556 & 6.722 & 5.667\\ "
    + "\n"
    + "\n"
    + r"\bottomrule"
    + "\n"
    + r"\end{tabular}"
    + "\n"
)


expected_defined = [
    "\definecolor{rankcolor1}{rgb}{0.42274509803921567,0.684075355632449,0.8398923490965013}",
    "\definecolor{avgrankcolor1}{rgb}{0.41636293733179547,0.3190003844675125,0.639923106497501}",
    "\definecolor{avgrankcolor2}{rgb}{0.6214532871972318,0.606074586697424,0.7855440215301807}",
    "\definecolor{avgrankcolor3}{rgb}{0.8568396770472895,0.8566551326412918,0.9224913494809688}",
]


@pytest.fixture
def multi_df():
    return pd.read_csv("test/multiindex.csv", index_col=[0, 1], header=[0, 1])


@pytest.fixture
def normal_df():
    return pd.read_csv("test/normal.csv", index_col=[0], header=[0])


def _check_general_form(ls: str, df: pd.DataFrame):
    for line in ls.split("\n"):
        if (
            len(line) > 2
            and "rule" not in line
            and "tabular" not in line
            and "multicolumn" not in line
        ):
            assert len(df.columns) == (line.count("&") + len(df.index.names) - 1)


def test_multiindex_full(multi_df):
    ls, defined = colat(
        multi_df,
        colors_rgb=sns.color_palette("Blues_r", n_colors=1),
        avg_rank_colors_rgb=sns.color_palette("Purples_r", n_colors=3),
        level_value="fm",
        level=1,
    )
    assert expected_multi.replace(" ", "") == ls.replace(" ", "")
    assert expected_defined == defined


def test_normal_full(normal_df):
    ls, defined = colat(
        normal_df,
        colors_rgb=sns.color_palette("Blues_r", n_colors=1),
        avg_rank_colors_rgb=sns.color_palette("Purples_r", n_colors=3),
    )
    assert expected_normal.replace(" ", "") == ls.replace(" ", "")
    assert expected_defined == defined


@pytest.mark.parametrize("args", [{}])
def test_normal_args(normal_df, args):
    ls, defined = colat(normal_df, **args)
    _check_general_form(ls, normal_df)
