# 🧠 NumPy Ultimate Reference (10/10)

``` python
import numpy as np
```

------------------------------------------------------------------------

## 🟢 1. Creation & Metadata

### Array Creation

``` python
np.array([1,2,3])  # → [1 2 3]
np.zeros((2,3))
np.ones((2,2))
np.full((2,2), 7)
np.eye(3)

np.arange(0,10,2)  # → [0 2 4 6 8]
np.linspace(0,1,5) # → [0.   0.25 0.5  0.75 1.]

np.random.randint(0,10,(2,3))
np.random.rand(2,2)
np.random.randn(2,2)
```

### Metadata

``` python
arr = np.arange(12).reshape(3,4)

arr.shape
arr.ndim
arr.size
arr.dtype
arr.nbytes
arr.base
```

------------------------------------------------------------------------

## 🔵 2. Shape & Manipulation

``` python
arr.reshape(2,-1)
arr.flatten()
arr.ravel()

arr[np.newaxis, :]
arr.squeeze()
arr.T
```

### Joining

``` python
np.concatenate((a,b))
np.vstack((a,b))
np.hstack((a,b))
```

------------------------------------------------------------------------

## 🟡 3. Indexing & Filtering

``` python
arr[0:2,1:]
arr[arr > 3]

np.where(arr > 3, 1, 0)
np.clip(arr, 2, 5)

np.unique([1,2,2,3], return_counts=True)
np.sort(arr, axis=1)
```

------------------------------------------------------------------------

## 🔴 4. Arithmetic & Math

``` python
arr + 5
arr - 1
arr * 2
arr / 2
arr ** 2
arr % 2

np.sqrt(arr)
np.exp(arr)
np.log(arr)
np.abs(arr)
```

### Rounding

``` python
np.floor(arr)
np.ceil(arr)
np.round(arr)
```

------------------------------------------------------------------------

## 🔴 5. Statistics & Axis

``` python
np.sum(arr)
np.mean(arr)
np.median(arr)
np.std(arr)
np.var(arr)

np.min(arr)
np.max(arr)

np.argmax(arr)
np.argmin(arr)
```

### Axis

``` python
np.sum(arr, axis=0)  # column-wise
np.sum(arr, axis=1)  # row-wise
```

### keepdims

``` python
np.sum(arr, axis=1, keepdims=True)
```

### Normalization

``` python
(arr - arr.min()) / (arr.max() - arr.min())
(arr - arr.mean()) / arr.std()
```

------------------------------------------------------------------------

## 🟣 6. Linear Algebra

``` python
A @ A
np.dot(A, A)

np.linalg.inv(A)
np.linalg.eig(A)
np.linalg.solve(A, b)
```

------------------------------------------------------------------------

## 🟠 7. NaNs & Cleaning

``` python
np.isnan(arr)
np.isinf(arr)

np.nanmean(arr)
np.nanmedian(arr)

np.nan_to_num(arr, nan=0)
```

------------------------------------------------------------------------

## ⚡ 8. Broadcasting

``` python
a = np.arange(12).reshape(3,4)
b = np.array([10,20,30,40])

a + b
```

------------------------------------------------------------------------

## ⚠️ 9. Views vs Copies

``` python
b = a[1:]
b[0] = 100
```

------------------------------------------------------------------------

## 🧠 10. dtype & Performance

``` python
arr.astype(np.float32)
```

------------------------------------------------------------------------

## 🔥 11. Advanced NumPy

### Fancy Indexing

``` python
arr[[0,2],[1,3]]
```

### einsum

``` python
np.einsum('ij,jk->ik', A, B)
np.einsum('ij->i', A)
```

### ufunc

``` python
np.add.reduce(arr)
np.add.accumulate(arr)
np.add.outer(a, b)
```

### Memory

``` python
arr.flags['C_CONTIGUOUS']
np.ascontiguousarray(arr)
```

### Other

``` python
np.meshgrid(x, y)
np.histogram(data)

np.linalg.svd(A)
```

### Random

``` python
rng = np.random.default_rng(42)
rng.standard_normal(10)
```

------------------------------------------------------------------------

## 🟣 12. File & Utilities

``` python
np.save('file.npy', arr)
np.load('file.npy')

np.intersect1d([1,2,3],[2,3,4])
```

------------------------------------------------------------------------

## 🚨 13. Pitfalls

-   Use `np.sum()` not `sum()`
-   Views modify original
-   Avoid `if arr` → use `.any()` / `.all()`
