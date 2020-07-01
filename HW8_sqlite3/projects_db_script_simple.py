"""Imports data from csv files into the new database
and executes queries like this
'SELECT * FROM tasks_tbl WHERE project_id =?;'
project_id is taken from user input


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
            status       TEXT,
            deadline     DATE,
            completed    DATE,
            project_id   NUMBER,
            CONSTRAINT PR_ID_FK FOREIGN KEY(project_id) 
                REFERENCES projects_tbl(project_id),
            CONSTRAINT ST_CHK CHECK(status IN(
                'new', 'pending', 'done', 'canceled'))
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
        """Makes queries based on user input, executes it and prints
        the response. Does NOT catch errors for invalid queries.

        :raises sqlite3.Warning, sqlite3.Error and its subclasses
        """
        print("\nPlease enter project_id value to execute the statement:\n"
              "\033[36mSELECT * FROM tasks_tbl WHERE project_id = ?;\033[0m\n"
              "Available project_id values: "
              f"{self._get_project_id_values()}\n")
        while True:
            param = self._get_param()
            self.execute(
                "SELECT * FROM tasks_tbl WHERE project_id = ?;", (param,))
            self.pretty_print_query_result()

    def _get_param(self):
        """Takes project_id value from user input"""
        while True:
            try:
                param = int(input(
                    "\033[0mType project_id and press Enter: \033[33m"
                ).strip())
            except EOFError or KeyboardInterrupt:
                self._show_message_and_exit("Terminated")
            except ValueError:
                pass
            else:
                if param in self._get_project_id_values():
                    return param

    def _get_project_id_values(self):
        """Get project_id values that are actually present in the table."""
        self.execute("SELECT DISTINCT project_id FROM projects_tbl")
        return tuple(row[0] for row in self.fetchall())

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
