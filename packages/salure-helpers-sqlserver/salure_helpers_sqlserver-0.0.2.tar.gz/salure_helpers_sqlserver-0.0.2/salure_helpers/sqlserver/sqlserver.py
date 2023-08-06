import math
import time
from typing import Union, Optional, List
import pandas as pd
import pymysql
from datetime import datetime
from salure_helpers.salureconnect import SalureConnect


class SQLServer:

    def __init__(self, salureconnect_connection: SalureConnect, label: Union[str, List], debug=False):
        self.salureconnect_connection = salureconnect_connection
        credentials = self.salureconnect_connection.get_system_credential(system='mssql', label=label)
        self.host = credentials['host']
        self.user = credentials['user']
        self.password = credentials['password']
        self.database = credentials['database']
        self.port = 1433 if credentials['port'] is None else credentials['port']
        self.debug = debug

    def raw_query(self, query, insert=False):
        start = time.time()
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
        cursor = connection.cursor()
        cursor.execute(query)
        if insert:
            connection.commit()
            data = '{0} - Writing data took {1} seconds'.format(time.strftime('%H:%M:%S'), time.time() - start)
        else:
            data = cursor.fetchall()
        connection.close()
        return data

    def update(self, table: str, columns: list, values: list, filter: str = None, return_queries: bool = False) -> Optional[str]:
        update_values = ''

        def __map_strings(item):
            if isinstance(item, str):
                return "'" + str(item) + "'"
            elif isinstance(item, datetime):
                return "'" + item.strftime("%Y-%m-%d %H:%M:%S") + "'"
            else:
                return str(item)

        for index in range(len(columns)):
            if index != len(columns) - 1:
                update_values += f"{columns[index]} = {__map_strings(values[index])},"
            else:
                update_values += f"{columns[index]} = { __map_strings(values[index])}"
        update_values = update_values.replace('None', 'DEFAULT')
        query = f"UPDATE {table} SET {update_values} {filter};"
        if self.debug:
            print(query)
        if return_queries:
            return query
        else:
            connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            connection.close()

    def select(self, table: str, columns: list, filter: str = None, return_queries: bool = False) -> Union[list, str]:
        query = f"SELECT {','.join(columns)} FROM {table} {filter if filter is not None else ''}"
        if self.debug:
            print(query)
        if return_queries:
            return query
        else:
            connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
            cursor = connection.cursor()
            cursor.arraysize = 10000
            cursor.execute(query)
            data = cursor.fetchall()
            connection.close()

            return list(data)

    def insert(self, table: str, df: pd.DataFrame, columns: list = None, return_queries: bool = False) -> Union[list, str]:
        queries = []
        for i in range(math.ceil(len(df.index) / 1000)):
            # Split df in batches because you can insert maximum of 1000 rows in sql server at once
            df_batch = df[0 + i * 1000: 1000 + i * 1000]
            columns = columns if columns else ', '.join(str(column) for column in df_batch.columns)
            values = ', '.join(str(index[1:]) for index in df_batch.itertuples())
            values = values.replace('None', 'DEFAULT')
            values = values.replace('NaT', 'NULL')
            values = values.replace('nan', 'NULL')
            values = values.replace("'NULL'", "NULL")
            values = values.replace('"', "'")
            values = values.replace("\\\\'", "''")
            queries.append(f"""INSERT INTO {table} ({columns}) VALUES {values}""")

        if return_queries:
            return queries
        else:
            connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
            cursor = connection.cursor()
            for query in queries:
                cursor.execute(query)
            connection.commit()
            connection.close()

