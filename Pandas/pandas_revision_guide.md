# Pandas Notes & Revision Guide

> Comprehensive beginner-friendly notes based strictly on the topics covered in the uploaded notebook.

---

# 1. What is Pandas?

Pandas is a Python library used for:

- Data analysis
- Data cleaning
- Working with tables
- Handling structured data

Import pandas:

```python
import pandas as pd
```

---

# 2. Main Data Structures

| Structure | Meaning |
|---|---|
| Series | 1D labeled data |
| DataFrame | 2D table |

---

# 3. Pandas Series

## Creating a Series

```python
x=[10,20,30,40]

var=pd.Series(x)
print(var)
```

Output:

```python
0    10
1    20
2    30
3    40
```

Pandas automatically creates indexes.

---

# 4. Custom Index

```python
var=pd.Series(
    [1,2,3,4],
    index=['a','b','c','d']
)
```

Output:

```python
a    1
b    2
c    3
d    4
```

Access value:

```python
print(var['c'])
```

---

# 5. Datatype in Series

```python
var=pd.Series(
    [1,2,3,4],
    dtype='float'
)
```

Output values become:

```python
1.0 2.0 3.0 4.0
```

---

# 6. Naming a Series

```python
var=pd.Series(
    [1,2,3],
    name='python'
)
```

---

# 7. Series from Dictionary

```python
dic={
    'name':['a','b','c','d'],
    'pop':[12,13,14,15],
    'rank':[1,4,3,2]
}

var_1=pd.Series(dic)
```

Important:
- Only ONE Series is created.
- Keys become indexes.
- Lists become values.

Accessing `"c"`:

```python
var_1['name'][2]
```

---

# 8. Scalar Series

```python
pd.Series(12,index=[1,2,3,4])
```

Output:

```python
1    12
2    12
3    12
4    12
```

Same value repeats for all indexes.

---

# 9. Arithmetic Operations on Series

```python
s1=pd.Series([1,2,3])
s2=pd.Series([4,5,6])

print(s1+s2)
```

Output:

```python
0    5
1    7
2    9
```

Operations happen element-wise.

---

# 10. What is NaN?

Example:

```python
s1=pd.Series([1,2,3])
s2=pd.Series([1,2,3,4])

print(s1+s2)
```

Output:

```python
0    2
1    4
2    6
3    NaN
```

NaN means:

```python
Missing Value
```

---

# 11. DataFrame

A DataFrame is a 2D table containing:
- Rows
- Columns

---

# 12. Creating DataFrame from Dictionary

```python
d={
    'a':[1,2,3],
    'b':[4,5,6]
}

var=pd.DataFrame(d)
```

Output:

```python
   a  b
0  1  4
1  2  5
2  3  6
```

Dictionary keys become column names.

---

# 13. Selecting Columns

```python
print(var['a'])
```

A DataFrame column itself is a Series.

---

# 14. Accessing Specific Values

```python
print(var['b'][1])
```

Meaning:

```python
[column][row]
```

---

# 15. DataFrame from Nested List

```python
list_1=[
    [1,2,3],
    [4,5,6]
]

pd.DataFrame(list_1)
```

Each inner list becomes one row.

---

# 16. DataFrame from Multiple Series

```python
sr1=pd.Series([1,2,3])
sr2=pd.Series([4,5,6])

pd.DataFrame({
    'A':sr1,
    'B':sr2
})
```

Each Series becomes a separate column.

---

# 17. Arithmetic Operations in DataFrame

```python
var['C']=var['A']+var['B']
```

Other operations:

```python
-
*
/
//
```

Operations happen row-by-row.

---

# 18. Boolean Operations

```python
var['C']=var['A']<3
```

Output contains:

```python
True
False
```

Used for:
- Filtering
- Conditions
- Data cleaning

---

# 19. Multiple Conditions

```python
(var['A']<3) & (var['B']<5)
```

`&` means AND.

Use `&`, not `and`.

---

# 20. Insert Function

```python
var.insert(2,'C',[10,20,30])
```

Syntax:

```python
insert(position,column_name,data)
```

---

# 21. Must-Know Concepts

## DataFrame Columns are Series

```python
var['A']
```

returns a Series.

---

## Pandas Uses Index Alignment

Pandas matches data using indexes.

Missing indexes produce:

```python
NaN
```

---

## Series vs DataFrame

| Series | DataFrame |
|---|---|
| 1D | 2D |
| One column | Multiple columns |
| Like list | Like table |

---

## Element-Wise Operations

```python
var['A']+var['B']
```

adds values row-by-row.

---

## Dictionary Behavior

### In Series
Keys become indexes.

### In DataFrame
Keys become column names.

---

# 22. Common Beginner Mistakes

## Mistake 1
Confusing Series with DataFrame.

## Mistake 2
Forgetting indexes.

## Mistake 3
Using different column lengths.

## Mistake 4

Confusing:

```python
var['A']
```

with:

```python
var[['A']]
```

First gives Series.
Second gives DataFrame.

---

