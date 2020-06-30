"""Imports data from csv files into the new database
and provides the ability to execute queries on it.

Detailed description:
 1. Creates database as a single file.
 2. Creates two tables in the database: projects_tbl, tasks_tbl.
    Defines column names, column data types, relations and constraints.
 3. Imports data from the respective .csv files
    and inserts these data into the tables.
 4. Takes user input in a form of executable SQLite query.
    In order to extend functionality, user input requires a full query,
    not just a part of it. Queries on both tables using JOIN are
    supported as well. Despite default hardcoded query is specified
    and is executed if no user input is provided.
 5. Prints selected data in a table. Automatically detects column width.

File names, database and table names, column names, column data types,
relations and constraints are hardcoded. File content can be modified as
long as these modifications do not contradict with data types and
constraints.
"""

import csv
import os
import re
import sqlite3
import sys
from typing import Any, Iterable, NoReturn, Union


def get_and_execute_user_query(cursor: sqlite3.Cursor) -> NoReturn:
    """Gets a query from the user and executes it.
    Raises exception if the query is invalid.

    :param cursor: cursor object to execute a query.
    """
    print("\nEnter your query below and press Enter twice to execute it:")
    query = ""
    while True:
        new_query_line = next(sys.stdin)
        if new_query_line.isspace():
            break
        query += new_query_line
    if not query:
        print("No query was detected", end="")
        cursor.close()
        exit()
    yield query
    cursor.execute(query)


def pretty_print_response(headers: Iterable[str],
        records: Iterable[Iterable[Union[str, int]]]) -> NoReturn:
    """Prints response as a table. Automatically detects column width.

    :param headers: headers from recent selection
    :param records: response fetched from a cursor
    """

    def _align_fields(column: Iterable[Any]) -> Iterable[str]:
        """Transforms all values in the column
        into str type and unifies their length.
        """

        def _align_cell(field: str) -> str:
            return f"{field: ^{width}}"

        column_str_only = tuple(map(str, column))
        width = max(map(len, column_str_only))
        return map(_align_cell, column_str_only)

    def _join_row(row: Iterable[str]) -> str:
        return " │ ".join(row)

    columns = zip(headers, *records)
    columns_aligned = map(_align_fields, columns)
    records_aligned = zip(*columns_aligned)
    records_strings = map(_join_row, records_aligned)
    headers_aligned = next(records_strings)
    header_body_sep = re.sub("│", "┼", re.sub("[^│]", "─", headers_aligned))
    print(headers_aligned, header_body_sep, *records_strings, sep="\n")


if __name__ == "__main__":
    # 0. Set data definition and insertion queries for later use
    INITIALIZATION_SQL_SCRIPT = """
    DROP TABLE IF EXISTS projects_tbl;
    CREATE TABLE projects_tbl(
        project_id   NUMBER  PRIMARY KEY,
        name         TEXT,
        description  TEXT,
        deadline     DATE
    );
    DROP TABLE IF EXISTS tasks_tbl;
    CREATE TABLE tasks_tbl( 
        task_id      NUMBER  PRIMARY KEY,
        priority     INTEGER,
        details      TEXT,
        status       TEXT    CHECK(
            status IN('new', 'pending', 'done', 'canceled')),
        deadline     DATE,
        completed    DATE,
        project_id   NUMBER,
        FOREIGN KEY(project_id) REFERENCES project_tbl(project_id)
    );"""
    # Most names are hardcoded because formatting sql queries
    # is not safe due to potential SQL injections.
    # Only ? placeholders are used.
    INSERTION_COMMANDS = {
        "projects_tbl.csv": "INSERT INTO projects_tbl VALUES (?, ?, ?, ?);",
        "tasks_tbl.csv": "INSERT INTO tasks_tbl VALUES (?, ?, ?, ?, ?, ?, ?);", }

    # 1. Create database and tables
    conn = sqlite3.connect("task_db.sqlite3")
    cur = conn.cursor()
    cur.executescript(INITIALIZATION_SQL_SCRIPT)

    # 2. Read data from csv files and insert them into tables
    for filename in INSERTION_COMMANDS.keys():
        if not os.path.exists(filename):
            print(f"Could not find file '{filename}'!")
            cur.close()
            exit()
        reader = csv.reader(open(filename, encoding='utf-8-sig', newline=""))
        # 'utf-8-sig' can handle '\ufeff' character
        next(reader)
        cur.executemany(INSERTION_COMMANDS.get(filename), reader)

    # 3. Get query from the user, execute the query and print the response
    print("""\nPlease enter SQL query and press double Enter.
    * Both inline and multiline queries are supported.
    * Use single Enter to type multiline queries.
      After pressing Enter, the line is saved.
      Any edits of this line will be discarded.
    * Use double Enter to execute your query.
    * You can execute next query after successful
      execution of the previous one (only one query at a time).
    * You may type your own queries or start with
      the examples to explore the dateset.
    * To quit, press Enter without input.
    \nExamples:
    \033[36mSELECT * FROM tasks_tbl;
    \033[34mSELECT * FROM projects_tbl;
    \033[36mSELECT * FROM tasks_tbl WHERE project_id = 400;
    \033[34mSELECT p.name AS ProjectName, COUNT(*) AS NumberOfTasks
    FROM tasks_tbl t INNER JOIN projects_tbl p
    ON t.project_id = p.project_id
    GROUP BY p.name;\033[0m""")
    while True:
        get_and_execute_user_query(cur)
        pretty_print_response(
            headers=[description[0] for description in cur.description],
            records=cur.fetchall())
