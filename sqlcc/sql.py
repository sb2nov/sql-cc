import sqlite3
import pandas as pd
import hashlib
import os
import pkgutil
from io import StringIO

DATA_FOLDER_URL = "data/"
DB_SCHEMA_URL = "db_creation_script.sql"
SQLITE_URL = "airbnb_sydney.sqlite"
CSV_FILES_URL = ["sql_neighbourhoods.csv", "sql_listings.csv",
                 "sql_calendar.csv", "sql_reviews.csv"]
SOLUTION_CSV = "project_solutions.csv"


def run(sql_query: str) -> pd.DataFrame:
    """
    Run an SQL query on a database
    """
    # Check if db is set up
    __init()

    # Create your connection.
    cnx = sqlite3.connect(SQLITE_URL)

    # Open the connection and run the query
    dataframe = pd.read_sql_query(sql_query, cnx)

    # Close the connection.
    cnx.commit()
    cnx.close()

    # Return the output as Pandas dataframe
    return dataframe


def check(**key_user_sql_query):
    print("-------------------")
    sql_solutions = pd.read_csv(StringIO(pkgutil.get_data(
        __name__, DATA_FOLDER_URL + SOLUTION_CSV).decode("utf-8")), sep=";", header=0)
    sql_sol_dict = dict(zip(sql_solutions.key, sql_solutions.value))

    for key, user_sql_query in key_user_sql_query.items():
        try:
            if key in sql_sol_dict:
                # Check if one or many solutions are available
                # Interpret string as list
                solution_list = sql_sol_dict[key][1:-
                                                  1].replace('"', "").split('|')
                solution_list = [solution.strip()
                                 for solution in solution_list]

                # There is only one possible solution.
                if len(solution_list) == 1:
                    sql_sol_df = run(solution_list[0].lower())
                    current_sql_df = run(user_sql_query.lower())
                    # order the columns
                    sql_sol_df.sort_index(axis=1, inplace=True)
                    current_sql_df.sort_index(axis=1, inplace=True)

                    # First check if contains the same columns
                    if sql_sol_df.columns.tolist() != current_sql_df.columns.tolist():
                        print("Your SQL query does NOT match our solution. There is a column mismatch:" +
                              "\n" +
                              "\nYou have:\t" + str(current_sql_df.columns.tolist()) +
                              "\nExpected:\t" + str(sql_sol_df.columns.tolist()) +
                              "\n-------------------")
                    else:
                        if sql_sol_df.equals(current_sql_df):
                            print("Your SQL query is correct!")
                        else:
                            print(
                                "Your SQL query does NOT match our solution. The number of rows is different.")

                # There are more than one possible solution available.
                else:
                    # String which is only printed if none of solutions match
                    output_log = ("There are " +
                                  str(len(solution_list)) +
                                  " possible solutions for this SQL query. Your different in:")
                    state = 0

                    for ix, solution in enumerate(solution_list):
                        sql_sol_df = run(solution.lower())
                        current_sql_df = run(user_sql_query.lower())
                        # order the columns
                        sql_sol_df.sort_index(axis=1, inplace=True)
                        current_sql_df.sort_index(axis=1, inplace=True)

                        # First check if contains the same columns
                        if sql_sol_df.columns.tolist() != current_sql_df.columns.tolist():
                            temp_log = ("\n\n> Solution " + str(ix + 1) +
                                        ": Your SQL query differs from this solution due to a column mismatch:" +
                                        "\n" +
                                        "\nYou have:\t" + str(current_sql_df.columns.tolist()) +
                                        "\nExpected:\t" + str(sql_sol_df.columns.tolist()))
                            output_log = "".join((output_log, temp_log))

                        else:
                            # Make sure to output the right log
                            if sql_sol_df.equals(current_sql_df):
                                state = 1
                            else:
                                state = 1 if state == 1 else 2

                    if state == 1:
                        print("Your SQL query is correct!")
                    elif state == 2:
                        print(
                            "Your SQL query does NOT match our solution. The number of rows is different.")
                    else:
                        print(output_log)
                print("\n-------------------")

            else:
                raise QuestionKeyUnknown
        except QuestionKeyUnknown:
            print("The variable name used for the parameter" +
                  " in the check function does not match" +
                  " any of our solution keys.")


class QuestionKeyUnknown(Exception):
    """
    Raised when the variable name does not match
    any of the keys we've defined for our question-
    solution pairs.
    """
    pass


def __init():
    """
    (Re-)creates the database
    """
    if "SQLITE_DB_HASH" in os.environ:
        if os.path.isfile(SQLITE_URL):
            hash = __calculate_file_hash(SQLITE_URL)

            if hash != os.environ["SQLITE_DB_HASH"]:
                # Delete db
                __delete_db(SQLITE_URL)

                # Recreate db
                __create_db(DATA_FOLDER_URL, DB_SCHEMA_URL,
                            SQLITE_URL, CSV_FILES_URL)
        else:
            # Create db
            __create_db(DATA_FOLDER_URL, DB_SCHEMA_URL,
                        SQLITE_URL, CSV_FILES_URL)
    else:
        # Delete db
        __delete_db(SQLITE_URL)

        # Create db
        __create_db(DATA_FOLDER_URL, DB_SCHEMA_URL, SQLITE_URL, CSV_FILES_URL)

        # Set hash to env variable
        os.environ["SQLITE_DB_HASH"] = __calculate_file_hash(SQLITE_URL)


def __calculate_file_hash(file_url: str) -> str:
    """
    Calculate the hash of given file
    """
    BUF_SIZE = 60000  # read in ~60kb chunks
    blake2b = hashlib.blake2b()

    with open(file_url, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            blake2b.update(data)

    return blake2b.hexdigest()


def __create_db(data_folder: str, db_schema_url: str, sqlite_url: str, csv_files_url: list):
    """
    (Re-)create the database from scratch using SQL and CSV scripts.
    """
    db_schema_string = pkgutil.get_data(
        __name__, data_folder + db_schema_url).decode("utf-8")

    conn = sqlite3.connect(sqlite_url)
    c = conn.cursor()
    c.executescript(db_schema_string)

    conn.commit()

    # Remove "sql_" and ".csv" from csv_files
    table_names = [file.replace("sql_", "").replace(".csv", "")
                   for file in csv_files_url]

    for csv_file, table_name in zip(csv_files_url, table_names):
        df = pd.read_csv(StringIO(pkgutil.get_data(
            __name__, data_folder + csv_file).decode("utf-8")))
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()

    conn.close()


def __delete_db(file_url: str):
    """
    Delete the database
    """
    try:
        os.remove(file_url)
    except FileNotFoundError:
        pass
