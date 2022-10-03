import sqlite3
import pandas as pd


def sql_query(sql_query: str):
    # Create your connection.
    cnx = sqlite3.connect('airbnb_sydney.sqlite')

    # Open the connection and run the query
    dataframe = pd.read_sql_query(sql_query, cnx)

    # Close the connection.
    cnx.commit()
    cnx.close()

    # Return the output as Pandas dataframe
    return dataframe
