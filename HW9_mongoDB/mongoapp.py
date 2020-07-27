"""Connects with MongoDB on local device or in cloud. Imports data
from csv files into MongoDB. Executes a query to select the names
of projects that include cancelled tasks.
"""

import csv
import os
import pymongo
from typing import NoReturn, Union


def connect_to_mongo() -> pymongo.MongoClient:
    """Set the mode of interaction with MongoDB. For cloud connection,
    get credentials and database name from the user. Establish the connection.

    :return: pymongo.MongoClient instance (cluster)
    """
    print("How would you like to connect to MongoDB?")
    while True:
        mode = input("Type 'l' to connect on local device.\n"
                     "Type 'c' to connect in cloud.\n")
        if mode == "c":
            return _connect_remotely(username=input("username: "),
                                     password=input("password: "))
        if mode == "l":
            return _connect_locally()


def _connect_locally(
        host: str = "localhost",
        port: int = 27017) -> pymongo.MongoClient:
    """Connects to MongoDB on local device.

    :param host: optional; host name; default: 'localhost';
    :param port: optional; port number; default: 27017;
    :return: pymongo.MongoClient instance (cluster)
    """
    return pymongo.MongoClient(host, port)


def _connect_remotely(
        username: str,
        password: str,
        database: str = "projects_db---") -> pymongo.MongoClient:
    """Connects to MongoDB in cloud by MongoDB URI which must contain
    username, password and database name (default: 'projects_db').

    :return: pymongo.MongoClient instance (cluster);
    :raises pymongo.errors.OperationFailure if authentication fails.
    :raises pymongo.errors.InvalidURI for missing password and/or username;
    :raises pymongo.errors.ConfigurationError for missing password
    or if cluster0 does not exist
    """
    mongo_uri = (f"mongodb+srv://{username}:{password}"
                 f"@cluster0.zkdur.mongodb.net/{database}"
                 f"?retryWrites=true&w=majority")
    return pymongo.MongoClient(mongo_uri)


def exit_if_file_does_not_exist(filename: Union[str, bytes]) -> NoReturn:
    """Checks file existence. If the file
    does not exist, prints warning message and exits.

    :param filename: absolute or relative filename to be checked;
    :return: None
    """
    if not os.path.exists(filename):
        print(f"Data import failed! Could not find '{filename}'!")
        exit()


def import_from_csv_into_collection(
        collection: pymongo.collection.Collection,
        filename: Union[str, bytes]) -> NoReturn:
    """Imports data into specified collection from specified CSV file.
    File existence is checked. The collection is cleared before new
    data are imported into it. The function uses 'utf-8-sig' encoding
    which can deal with '\ufeff' character if it appears in CSV file.

    :param collection: pymongo collection to import data into;
    :param filename: CSV file name to export data from;
    :return: None
    """
    exit_if_file_does_not_exist(filename)
    file_handle = open(file=filename, mode="rt", encoding='utf-8-sig')
    reader = csv.DictReader(file_handle)
    collection.delete_many({})
    collection.insert_many(reader)


def execute_query(
        database: pymongo.mongo_client.database.Database) -> NoReturn:
    """Selects the names of projects that include cancelled tasks.
    Executes the query and prints the result. The query is equivalent
    to the following SQL query:

    SELECT _id FROM database.projects
    WHERE _id IN (SELECT project_id from database.tasks
                  WHERE status = "canceled");

    :param database: Database instance to query;
    :return: None
    """
    query_result = [
        project["name"] for project in database["projects"].find(
            {"_id": {"$in": [
                task["project_id"] for task in database["tasks"].find(
                    {"status": "canceled"}
                )
            ]}}
        )
    ]
    print("\nProjects with cancelled tasks:\033[32m", *query_result, sep="\n")


def make_connection_import_data_and_execute_query() -> NoReturn:
    cluster = connect_to_mongo()
    database = cluster["projects_db"]
    import_from_csv_into_collection(
        collection=database["projects"], filename="projects_tbl.csv")
    import_from_csv_into_collection(
        collection=database["tasks"], filename="tasks_tbl.csv")
    execute_query(database)


if __name__ == "__main__":
    make_connection_import_data_and_execute_query()
