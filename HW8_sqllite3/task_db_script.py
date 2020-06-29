import sqlite3
import csv
import os
import re
from typing import Any, Iterable, NoReturn, Union


def ensure_that_files_exist(*filenames: str) -> NoReturn:
    for filename in filenames:
        if not os.path.exists(filename):
            print(f"Could not find file '{filename}'!")
            exit()


def insert_into_db_from_csv(
        cursor: sqlite3.Cursor,
        filename: str,
        command: str) -> NoReturn:
    """utf-8-sig' is used to ignore '\ufeff character'"""
    reader = csv.reader(open(filename, encoding='utf-8-sig', newline=""))
    next(reader)
    cursor.executemany(command, reader)


def execute_query_with_output(cursor: sqlite3.Cursor) -> NoReturn:
    default_query = (
        "SELECT p.name AS ProjectName, COUNT(*) AS NumberOfTasks\n"
        "FROM tasks_tbl t INNER JOIN projects_tbl p\n"
        "ON t.project_id = p.project_id\n"
        "GROUP BY p.name;"
    )
    query = input(
        "\nPlease enter SQLite query. You may type your own query\n"
        "or start with the examples to explore the dateset:\n\n"
        "Examples:\n"
        "SELECT * FROM tasks_tbl;\n"
        "SELECT * FROM projects_tbl;\n"
        "SELECT * FROM tasks_tbl WHERE project_id = 400;\n"
        f"{default_query}\n"
        "\nYour query:"
    )
    if not query:
        print("No input query was detected. Default query was executed:")
        print(default_query)
        query = default_query
    cursor.execute(query)
    print()
    pretty_print_table(
        headers=[description[0] for description in cursor.description],
        records=cursor.fetchall()
    )


def pretty_print_table(
        headers: Iterable[str],
        records: Iterable[Iterable[Union[str, int]]]) -> NoReturn:

    def _align_fields(column: Iterable[Any]) -> Iterable[str]:

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
    initialisation_sql_script = """
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

    insertion_commands = {
        "projects_tbl.csv": "INSERT INTO projects_tbl VALUES (?, ?, ?, ?);",
        "tasks_tbl.csv": "INSERT INTO tasks_tbl VALUES (?, ?, ?, ?, ?, ?, ?);",
    }
    ensure_that_files_exist(*insertion_commands.keys())

    conn = sqlite3.connect("task_db.sqlite3")
    cur = conn.cursor()
    cur.executescript(initialisation_sql_script)
    for filename_command_pair in insertion_commands.items():
        insert_into_db_from_csv(cur, *filename_command_pair)
    execute_query_with_output(cur)
