# Merges multiple DataFrames, ignores Exceptions if desired 

```python

$pip install a-pandas-ex-multimerge


# Ignores all Exceptions, but prints them, this behavior can be changed by passing disable=True

from a_pandas_ex_multimerge import pd_add_multimerge
import pandas as pd

pd_add_multimerge()
df1 = pd.DataFrame(
    {
        "A": ["A0", "A1", "A2", "A3"],
        "B": ["B0", "B1", "B2", "B3"],
        "C": ["C0", "C1", "C2", "C3"],
        "D": ["D0", "D1", "D2", "D3"],
    },
    index=[0, 1, 2, 3],
)

df2 = pd.DataFrame(
    {
        "A": ["A4", "A5", "A6", "A7"],
        "B": ["B4", "B5", "B6", "B7"],
        "C": ["C4", "C5", "C6", "C7"],
        "D": ["D4", "D5", "D6", "D7"],
    },
    index=[4, 5, 6, 7],
)

df3 = pd.DataFrame(
    {
        "A": ["A8", "A9", "A10", "A11"],
        "B": ["B8", "B9", "B10", "B11"],
        "C": ["C8", "C9", "C10", "C11"],
        "D": ["D8", "D9", "D10", "D11"],
    },
    index=[8, 9, 10, 11],
)
t1 = df1.ds_multimerge(
    dataframes=[df2, df3],
    on_index=False,
    columns_to_merge=None,
    print_exception=True,
    how="outer",
    disable=False,
)
t2 = df2.ds_multimerge(
    dataframes=[df2, df3],
    on_index=True,
    columns_to_merge=None,
    print_exception=False,
    how="outer",
    disable=False,
)

t3 = df3.ds_multimerge(
    dataframes=[df1, df2, ""],
    on_index=False,
    columns_to_merge=None,  # will merge on all common columns
    print_exception=True,
    how="outer",
    disable=False,
)
t4 = df1.ds_multimerge(
    dataframes=[df2, df3, 1],
    on_index=True,
    columns_to_merge=None,
    print_exception=False,
    how="outer",
    disable=False,
)

t5 = df1.ds_multimerge(
    dataframes=[
        df2,
        df3,
        1,
    ],  # won't raise an Exception. The string will be ignored
    on_index=False,
    columns_to_merge=["A", "B"],
    how="outer",
    print_exception=False,
    disable=False,
)
t6 = df2.ds_multimerge(
    dataframes=[
        df1,
        df3,
        1,
    ],  # won't raise an Exception. The number will be ignored
    on_index=False,
    columns_to_merge=["C", "D"],
    how="outer",
    print_exception=True,
    disable=False,
)
t7 = df2["A"].ds_multimerge(
    dataframes=[
        df1,
        df3,
        1,
    ],  # won't raise an Exception. The number will be ignored
    on_index=False,
    columns_to_merge=None,
    how="outer",
    print_exception=True,
)

 Ignores all Exceptions, but prints them, this behavior can be changed by passing disable=True
descriptor 'union' for 'set' objects doesn't apply to a 'function' object
descriptor 'union' for 'set' objects doesn't apply to a 'function' object
descriptor 'union' for 'set' objects doesn't apply to a 'function' object
descriptor 'union' for 'set' objects doesn't apply to a 'function' object
descriptor 'union' for 'set' objects doesn't apply to a 'function' object
Can only merge Series or DataFrame objects, a <class 'str'> was passed
Can only merge Series or DataFrame objects, a <class 'int'> was passed
descriptor 'union' for 'set' objects doesn't apply to a 'function' object
descriptor 'union' for 'set' objects doesn't apply to a 'function' object
descriptor 'union' for 'set' objects doesn't apply to a 'function' object
Can only merge Series or DataFrame objects, a <class 'int'> was passed
t7
Out[4]:
      A  B_x  C_x  D_x  B_y  C_y  D_y
0    A4  NaN  NaN  NaN  NaN  NaN  NaN
1    A5  NaN  NaN  NaN  NaN  NaN  NaN
2    A6  NaN  NaN  NaN  NaN  NaN  NaN
3    A7  NaN  NaN  NaN  NaN  NaN  NaN
4    A0   B0   C0   D0  NaN  NaN  NaN
5    A1   B1   C1   D1  NaN  NaN  NaN
6    A2   B2   C2   D2  NaN  NaN  NaN
7    A3   B3   C3   D3  NaN  NaN  NaN
8    A8  NaN  NaN  NaN   B8   C8   D8
9    A9  NaN  NaN  NaN   B9   C9   D9
10  A10  NaN  NaN  NaN  B10  C10  D10
11  A11  NaN  NaN  NaN  B11  C11  D11
t1
Out[5]:
      A    B    C    D
0    A0   B0   C0   D0
1    A1   B1   C1   D1
2    A2   B2   C2   D2
3    A3   B3   C3   D3
4    A4   B4   C4   D4
5    A5   B5   C5   D5
6    A6   B6   C6   D6
7    A7   B7   C7   D7
8    A8   B8   C8   D8
9    A9   B9   C9   D9
10  A10  B10  C10  D10
11  A11  B11  C11  D11
t2
Out[6]:
    A_x  B_x  C_x  D_x  A_y  B_y  C_y  D_y    A    B    C    D
4    A4   B4   C4   D4   A4   B4   C4   D4  NaN  NaN  NaN  NaN
5    A5   B5   C5   D5   A5   B5   C5   D5  NaN  NaN  NaN  NaN
6    A6   B6   C6   D6   A6   B6   C6   D6  NaN  NaN  NaN  NaN
7    A7   B7   C7   D7   A7   B7   C7   D7  NaN  NaN  NaN  NaN
8   NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN   A8   B8   C8   D8
9   NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN   A9   B9   C9   D9
10  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  A10  B10  C10  D10
11  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  A11  B11  C11  D11
t3
Out[7]:
      A    B    C    D
0    A8   B8   C8   D8
1    A9   B9   C9   D9
2   A10  B10  C10  D10
3   A11  B11  C11  D11
4    A0   B0   C0   D0
5    A1   B1   C1   D1
6    A2   B2   C2   D2
7    A3   B3   C3   D3
8    A4   B4   C4   D4
9    A5   B5   C5   D5
10   A6   B6   C6   D6
11   A7   B7   C7   D7
t4
Out[8]:
    A_x  B_x  C_x  D_x  A_y  B_y  C_y  D_y    A    B    C    D
0    A0   B0   C0   D0  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN
1    A1   B1   C1   D1  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN
2    A2   B2   C2   D2  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN
3    A3   B3   C3   D3  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN
4   NaN  NaN  NaN  NaN   A4   B4   C4   D4  NaN  NaN  NaN  NaN
5   NaN  NaN  NaN  NaN   A5   B5   C5   D5  NaN  NaN  NaN  NaN
6   NaN  NaN  NaN  NaN   A6   B6   C6   D6  NaN  NaN  NaN  NaN
7   NaN  NaN  NaN  NaN   A7   B7   C7   D7  NaN  NaN  NaN  NaN
8   NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN   A8   B8   C8   D8
9   NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN   A9   B9   C9   D9
10  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  A10  B10  C10  D10
11  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  A11  B11  C11  D11
t5
Out[9]:
      A    B  C_x  D_x  C_y  D_y    C    D
0    A0   B0   C0   D0  NaN  NaN  NaN  NaN
1    A1   B1   C1   D1  NaN  NaN  NaN  NaN
2    A2   B2   C2   D2  NaN  NaN  NaN  NaN
3    A3   B3   C3   D3  NaN  NaN  NaN  NaN
4    A4   B4  NaN  NaN   C4   D4  NaN  NaN
5    A5   B5  NaN  NaN   C5   D5  NaN  NaN
6    A6   B6  NaN  NaN   C6   D6  NaN  NaN
7    A7   B7  NaN  NaN   C7   D7  NaN  NaN
8    A8   B8  NaN  NaN  NaN  NaN   C8   D8
9    A9   B9  NaN  NaN  NaN  NaN   C9   D9
10  A10  B10  NaN  NaN  NaN  NaN  C10  D10
11  A11  B11  NaN  NaN  NaN  NaN  C11  D11
t6
Out[10]:
    A_x  B_x    C    D  A_y  B_y    A    B
0    A4   B4   C4   D4  NaN  NaN  NaN  NaN
1    A5   B5   C5   D5  NaN  NaN  NaN  NaN
2    A6   B6   C6   D6  NaN  NaN  NaN  NaN
3    A7   B7   C7   D7  NaN  NaN  NaN  NaN
4   NaN  NaN   C0   D0   A0   B0  NaN  NaN
5   NaN  NaN   C1   D1   A1   B1  NaN  NaN
6   NaN  NaN   C2   D2   A2   B2  NaN  NaN
7   NaN  NaN   C3   D3   A3   B3  NaN  NaN
8   NaN  NaN   C8   D8  NaN  NaN   A8   B8
9   NaN  NaN   C9   D9  NaN  NaN   A9   B9
10  NaN  NaN  C10  D10  NaN  NaN  A10  B10
11  NaN  NaN  C11  D11  NaN  NaN  A11  B11
t7
Out[11]:
      A  B_x  C_x  D_x  B_y  C_y  D_y
0    A4  NaN  NaN  NaN  NaN  NaN  NaN
1    A5  NaN  NaN  NaN  NaN  NaN  NaN
2    A6  NaN  NaN  NaN  NaN  NaN  NaN
3    A7  NaN  NaN  NaN  NaN  NaN  NaN
4    A0   B0   C0   D0  NaN  NaN  NaN
5    A1   B1   C1   D1  NaN  NaN  NaN
6    A2   B2   C2   D2  NaN  NaN  NaN
7    A3   B3   C3   D3  NaN  NaN  NaN
8    A8  NaN  NaN  NaN   B8   C8   D8
9    A9  NaN  NaN  NaN   B9   C9   D9
10  A10  NaN  NaN  NaN  B10  C10  D10
11  A11  NaN  NaN  NaN  B11  C11  D11


```
