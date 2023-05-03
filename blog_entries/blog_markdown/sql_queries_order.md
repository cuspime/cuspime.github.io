# Understanding the Structure of a simple SQL Query

Structured Query Language (SQL) is a programming language used to manage and manipulate relational databases.
It is essential for data management and analysis in many industries, from finance to healthcare to retail.
Even though it is often rather easy to read a SQL query, the order of the statements that make a SQL query is important.
If this order is not the proper one, the query will fail (in the best case scenario) or it can throw some pretty weird
results that at first glance seem to be what we wanted.
In this article, we will break down the structure of a simple, yet somewhat general SQL query.

## General query

The form of a general single query on SQL often used by data scientists/analysts looks like:

```sql
SELECT
    t1.col1,
    FIRST(t1.col2) AS col2,
    MAX(t1.col3) AS max_col3,
    MIN(t2.col4) AS min_col4,
    MAX(t2.col4) AS max_col4
FROM table1 AS t1
INNER JOIN table2 AS t2
ON t1.id = t2.table1_id
WHERE 
    t1.col2 BETWEEN 'min_value_col2' AND 'max_value_col2'
    AND t1.col3 > 'min_value_col3'
GROUP BY t1.col1
HAVING COUNT(*) > 1
ORDER BY max_col4 DESC
LIMIT 10;
```

This query selects data from two tables (`table1` and `table2`) and specifies several conditions and
limitations on the results.
Let's break down each part of the query to understand its purpose.

### SELECT

The `SELECT` statement specifies which columns to retrieve from the tables.
In this example, the `AS` keyword is used to create aliases for the columns, which can make the query easier to read and interpret.

**NB**: thes aliases are necessary for the part of the query that follows the _GROUP BY_ statement (like _HAVING_ and _ORDER BY_).

### FROM and JOIN

The `FROM` statement specifies the tables to retrieve data from, and the `JOIN` statement specifies how to join the tables.
In this example, the `ON` keyword is used to specify the _condition_ for the join, which is ultimately a boolean
condition for matching each row of both tables.
If you ever have doubts about the
operations' hierarchy for the condition you can always use parentheses to ensure each logical step in the condition.

### WHERE

The `WHERE` statement specifies the condition that each row must meet to be included in the result set. 

### GROUP BY

The `GROUP BY` statement is used to group rows based on the values in one or more columns.
In this example, the results are grouped by the values in `table1.col1`.

### HAVING

The `HAVING` statement is used to specify a condition that must be met by each group to be included in the result set.
In this example, the condition is that each group must have a count of rows greater than 1.

### ORDER BY

The `ORDER BY` statement is used to sort the result set based on one or more columns.
This statement will look for the alias of the column if given one.
In this example, the results are sorted in descending order by the values in `max_col4`.

### LIMIT

The `LIMIT` statement specifies the maximum number of rows to retrieve from the result set. In this example, the result set is limited to 10 rows.

## Order of execution

SQL queries are not executed as they are written (or read). The query is parsed in a different logical order for these statements or operations.
The importance of such order increases with the size of our database and the number of join operations amongst the used
tables.

The order is as follows:

1. FROM (and JOIN)
2. WHERE
3. GROUP BY
4. HAVING
5. SELECT
6. ORDER BY
7. LIMIT

It is thus important to keep this in mind when writing queries. If we only want a few rows to be matched from one of our
tables, it is better to write a subquery, appending a `WITH` statement to the `SELECT` statement we want, otherwise the
exectution plan will first join all rows and then filter by the condition of the WHERE statement.

For example: 

```sql
WITH small_table AS (
    SELECT * 
    FROM table2 AS t2
    ORDER BY t2.col1 DESC
    LIMIT 5
)

SELECT * 
FROM table1 
INNER JOIN small_table AS st
ON t1.id = st.table1_id
```

## Conclusion

Understanding the structure of a complex SQL query is essential for managing and analyzing data in a relational database.
By using the `SELECT`, `FROM`, `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT` and `WITH` statements, you can retrieve specific data from one or more tables based on your needs.
