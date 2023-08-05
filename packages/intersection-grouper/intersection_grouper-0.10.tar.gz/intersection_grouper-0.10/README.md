# Groups lists by common intersections

```python
pip install intersection-grouper
```


```python

from intersection_grouper import group_lists_with_intersections

listgroup = [
    [5, 3, 4, 5],
    [5, 11, 12, 3],
    [52, 34],
    [34, 111, 112],
    [1000, 300],
    [300, 5000],
]

x = group_lists_with_intersections(listgroup, keep_duplicates=True)
print(x)
[(34, 34, 52, 111, 112), (300, 300, 1000, 5000), (3, 3, 4, 5, 5, 5, 11, 12)]

x2 = group_lists_with_intersections(listgroup, keep_duplicates=False)
print(x2)
[(34, 52, 111, 112), (300, 1000, 5000), (3, 4, 5, 11, 12)]

```
