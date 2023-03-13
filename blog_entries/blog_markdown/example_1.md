# Example 1

Everything you can do with markdown [is shown here](https://culturedcode.com/things/support/articles/4651820/)

Some *embedded* Markdown which `md-block` can convert for you!
This is some inline LateX \\(a=b \sum_{ij}\\) 

This is some proper equation space
$$ a=b_k $$

We can __now__ try some ::really nice:: _things_ like **black** things and lists:

* like This
* and that

Numbered list

1. One
2. Two 
3. So on...

```python
for i in range(9):
    print(i)

def function(x:np.array):
    return x.sum()
```


```sql
SELECT 
    grouping_column, 
    COUNT(DISTINCT id) AS dist_id
FROM some_table
WHERE some_condition
GROUP BY grouping_column
HAVING dist_id > 1
```

To see some YouTube videos on this markdown just do (notice the **embed** keyword after www.youtube.com/):
```html
<div align="center"><iframe
    width="640"
    height="480"
    src="https://www.youtube.com/embed/PI22k8-Yi0s"
    frameborder="0"
    allow="autoplay; encrypted-media"
>
</iframe>
</div>
```

<div align="center"><iframe
    width="640"
    height="480"
    src="https://www.youtube.com/embed/PI22k8-Yi0s"
    frameborder="0"
    allow="autoplay; encrypted-media"
>
</iframe>
</div>