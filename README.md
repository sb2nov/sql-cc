# SQL Crash Course package

Run an SQL query for the "SQL Crash Course" using sqlcc.

## Install

You can install the package by running:

```
pip install git+https://github.com/sb2nov/sql-cc.git
```

Then you can run a SQL query like:

```Python
from sqlcc import run, check

### Question: q1_1_1
query = "SELECT * FROM listings"

run(query)
check(q1_1_1 = query)
```

The database and its content is locally constructed from the data contained in this package.

For simplification purposes, the query comparison check is made **case-insensitive**.
The tool supports multiple solutions. Solutions are added like: `["solution_query_1" | "solution_query_2" | ...]`.
