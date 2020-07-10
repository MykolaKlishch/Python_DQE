"""Connects with MongoDB on local device or in cloud. Imports data
from csv files into MongoDB. Executes a query to select the names
of projects that include cancelled tasks.
"""

import csv
import os
import pymongo
from typing import NoReturn, Union, Dict


def get_credentials() -> Dict[str, str]:
    """Set the mode of interaction with MongoDB.
    For cloud connection, get credentials and
    database name from the user.

    :return: dict with credentials and database name.
    """
    print("How would you like to connect to MongoDB?")
    while True:
        mode = input("Type 'l' to connect on local device.\n"
                     "Type 'c' to connect in cloud.\n")
        if mode == "c":
            return {"username": input("username: "),
                    "password": input("password: ")}
        if mode == "l":
            return {}


def connect_to_mongo(
        username: str = "",
        password: str = "",
        database: str = "projects_db",
        host: str = "localhost",
        port: int = 27017) -> pymongo.MongoClient:
    """Connects to MongoDB:
        * in cloud (by MongoDB URI which must contain
                    username, password and database name);
        * on local device (by host and port);
    If username, password and database are provided, cloud connection
    is used. Default host and port parameters are ignored. Otherwise,
    host and port are used. Other parameters are ignored.

    :param host: optional; for local connection only;
    :param port: optional; for local connection only;
    :param username: for cloud connection only;
    :param password: for cloud connection only;
    :param database: for cloud connection only;
    :return: pymongo.MongoClient instance (cluster);
    :raises pymongo.errors.OperationFailure if authentication fails.
    """
    if username and password:
        mongo_uri = (f"mongodb+srv://{username}:{password}"
                     f"@cluster0.zkdur.mongodb.net/{database}"
                     f"?retryWrites=true&w=majority")
        cluster = pymongo.MongoClient(mongo_uri)
    else:
        cluster = pymongo.MongoClient(host, port)
    return cluster


def exit_if_file_does_not_exist(filename: Union[str, bytes]) -> NoReturn:
    """Checks file existence. If the file
    does not exist, prints message and exits.

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
    data are imported into it. The method uses 'utf-8-sig' encoding
    which can deal with '\ufeff' character if it appears in CSV file.

    :param collection: pymongo collection to import data into;
    :param filename: CSV file name to export data from;
    :return: None
    """
    exit_if_file_does_not_exist(filename)
    file_handle = open(filename, encoding='utf-8-sig')
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
    cluster = connect_to_mongo(**get_credentials())
    database = cluster["projects_db"]
    import_from_csv_into_collection(
        collection=database["projects"], filename="projects_tbl.csv")
    import_from_csv_into_collection(
        collection=database["tasks"], filename="tasks_tbl.csv")
    execute_query(database)


if __name__ == "__main__":
    make_connection_import_data_and_execute_query()
