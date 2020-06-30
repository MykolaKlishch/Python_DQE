"""Imports data from csv files into the new database
and provides the ability to execute queries on it.

Detailed description:
 1. Creates sqlite3 database.
 2. Creates two tables in the database: 'projects_tbl' and 'tasks_tbl'.
    Defines column names, column data types, relations and constraints.
 3. Imports data from .csv files and inserts these data into
    the corresponding tables.
 4. Takes user input in a form of executable SQLite query.
    In order to expand functionality, user input requires a full query,
    not just a part of it. Multiline queries, queries on both tables
    using JOIN syntax, subqueries are supported as well.
 5. Prints selected data in a table. Automatically detects column width.

File names, database and table names, column names, column data types,
relations and constraints are hardcoded because formatting sql queries
is not safe due to potential SQL injections. File content can be
modified as long as these modifications do not contradict with
data types and constraints.
"""

import csv
import os
import re
import sqlite3
import sys
from typing import Any, Iterable


class CursorForProjectsDB(sqlite3.Cursor):
    """A subclass of Cursor with additional methods. Three of
    these methods correspond to main stages of script execution.
    """
    def create_database_schema(self):
        """Executes SQL script which creates
        tables and defines their structure.
        """
        self.executescript("""
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
            FOREIGN KEY(project_id) REFERENCES projects_tbl(project_id)
        );""")

    def import_data_into_database(self):
        """Reads data from csv files and inserts them into tables.
        The method can handle '\ufeff' character which may occur in
        csv files The method uses 'utf-8-sig' encoding which ignores
        '\ufeff' character ('utf-8' does not).
        """
        insertion_commands = {
            "projects_tbl.csv": "INSERT INTO projects_tbl VALUES (?,?,?,?);",
            "tasks_tbl.csv": "INSERT INTO tasks_tbl VALUES (?,?,?,?,?,?,?);"
        }
        for filename in insertion_commands.keys():
            if not os.path.exists(filename):
                self._show_message_and_exit(f"Could not find '{filename}'!")
            reader = csv.reader(open(filename, encoding='utf-8-sig'))
            next(reader)
            self.executemany(insertion_commands.get(filename), reader)

    def execute_user_queries(self):
        """Gets query from the user input, executes it and prints
        the response. Does NOT catch errors for invalid queries.

        :raises sqlite3.Warning, sqlite3.Error and its subclasses
        """
        print(self._get_guide())
        while True:
            query = next(self._get_query())
            self.execute(query)
            self.pretty_print_query_result()

    @staticmethod
    def _get_guide():
        return """\nPlease enter SQL query and press double Enter.
        * Both inline and multiline queries are supported.
        * Use double Enter to execute your query.
        * You can execute next query only after successful
          execution of the previous one (one query at a time).
        * Use single Enter to type multiline queries.
          After pressing Enter, the line is saved.
          Any edits of this line will be discarded.
        * You may type your own query or start with
          the examples to explore the data set.
        * To quit, press Enter without input.
        \nExamples:
        \033[36mSELECT * FROM projects_tbl;
        \033[34mSELECT * FROM tasks_tbl;
        \033[36mSELECT * FROM tasks_tbl WHERE project_id = 400;
        \033[34mSELECT p.name AS ProjectName, COUNT(*) AS NumberOfTasks
        FROM tasks_tbl t INNER JOIN projects_tbl p
        ON t.project_id = p.project_id
        GROUP BY p.name;\033[0m"""

    def _get_query(self):
        """Generator which gets queries from stdin.
        Queries are NOT validated at this stage.
        """
        print("\n\033[0mType your query below "
              "and double press Enter to execute it:\033[33m")
        new_query = ""
        while True:
            new_query_line = next(sys.stdin)
            if new_query_line.isspace():
                break
            new_query += new_query_line
        if not new_query:
            self._show_message_and_exit("No query was detected")
        yield new_query

    def _show_message_and_exit(self, message=""):
        """Prints message, closes the cursor and exits.

        :param message: message to print before exit
        """
        print(message, end="")
        self.connection.close()
        exit()

    def pretty_print_query_result(self):
        """Prints query result as a table.
        Automatically detects column width.
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

        headers = [description[0] for description in self.description]
        records = self.fetchall()
        columns = zip(headers, *records)
        columns_aligned = map(_align_fields, columns)
        records_aligned = zip(*columns_aligned)
        records_strings = map(_join_row, records_aligned)
        headers_aligned = next(records_strings)
        header_body_sep = re.sub(
            "│", "┼", re.sub("[^│]", "─", headers_aligned))
        print(headers_aligned, header_body_sep, *records_strings, sep="\n")
        print(f"\n{len(records)} rows selected")


if __name__ == "__main__":
    conn = sqlite3.connect("projects.db")
    cur = conn.cursor(factory=CursorForProjectsDB)
    cur.create_database_schema()
    cur.import_data_into_database()
    cur.execute_user_queries()
