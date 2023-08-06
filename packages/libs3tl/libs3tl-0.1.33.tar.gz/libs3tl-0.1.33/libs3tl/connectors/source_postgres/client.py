
import os
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.dialects.postgresql import insert
from urllib.parse import quote_plus as urlquote


class PostgresSource:
    """
    Source connector for PostgreSQL database using SQLAlchemy.
    """

    def __init__(self):
        self.metadata = None
        self.conn = None
        self.engine = None
        self.dbname = None
        self.table = None
        self.schema = None

    def url_encoded_password(self, password):
        return urlquote(password)

    def check(self, config: dict):
        """
        Connect to a Postgres database using the config provided and check the connection status to the database.

        Configuration parameters in json format:
        - host (string): Hostname or IP address of the database.
        - port (int): Port used by the database.
        - user (string): User to authenticate with.
        - password (string): Password to authenticate with.
        - database (string): Name of the database to use.
        - schema (string): Name of the schema to use.

        creates SQLAlchemy engine using config json object in self.engine
        """
        try:
            self.dbname = config["dbname"]
            self.table = config["table"]
            self.schema = config["schema"]
            config['encodedPassword'] = self.url_encoded_password( config['password'])
            self.engine = create_engine(
                "postgresql://{user}:{encodedPassword}@{host}:{port}/{dbname}".format_map(config)
            )
            connection = self.engine.connect()
            connection.close()
            # self.logInfo(self.step, 'Setup source connection successfull')
            # return AirbyteConnectionStatus(status=AirbyteConnectionStatus.Status.SUCCEEDED)
        except Exception as e:
            print(str(e))
            # self.logInfo(self.step, 'Connection error: ' + str(e))
            # return AirbyteConnectionStatus(status=AirbyteConnectionStatus.Status.FAILED, message=str(e))

    def discover(self):
        """
        Discover tables in the connected database.
        """
        table_list = []
        try:
            if self.schema is None:
                query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            else:
                query = "SELECT table_name FROM information_schema.tables WHERE table_schema = '{}';".format(self.schema)
            result = self.conn.execute(query).fetchall()
            for row in result:
                table_list.append(row[0])
            # return AirbyteConnectionStatus(status=AirbyteConnectionStatus.Status.SUCCEEDED, message=table_list)
        except Exception as e:
            pass
            # logger.error(str(e))
            # return AirbyteConnectionStatus(status=AirbyteConnectionStatus.Status.FAILED, message=str(e))

    def read(self, query: str = None):
        """
        Read from the connected database.
        The read() method takes an optional query parameter, and executes the query on the connected database.
        If no query is provided, it runs a SELECT * query on the specified table.
        Returns:
            records: list of dictionaries.
        """
        try:
            if not query:
                query = "SELECT * FROM {}.{}".format(self.schema, self.table)
            records = []
            with self.engine.connect() as conn:
                with conn.begin():
                    query_data = conn.execute(query)
                    col_names = [elem[0] for elem in query_data.cursor.description]
                    result = query_data.fetchall()
                    for row in result:
                        records.append(dict(zip(col_names, row)))
                        # records.append(AirbyteRecord(data=dict(zip(self.columns, row))))
                    return records
        except Exception as e:
            print(str(e))
            # logger.error(str(e))
            # return AirbyteConnectionStatus(status=AirbyteConnectionStatus.Status.FAILED, message=str(e))

    def setup_metadata(self):
        """
        configuring metadata with sqlalchemy engine
        The setup_metadata() method sets up the database engine and creates a MetaData object to store the database information.
        """
        try:
            self.metadata = MetaData(schema=self.schema)
            self.metadata.bind = self.engine
        except Exception as e:
            print(str(e))

    def get_table(self):
        """
        The get_table() method creates a connection to the database using the engine and begins a transaction.
        It then creates a Table object using the table name, metadata, schema, and connection.
        """
        try:
            self.setup_metadata()
            with self.engine.connect() as conn:
                with conn.begin():
                    return Table(self.table, self.metadata, schema=self.schema, autoload_with=conn)
        except Exception as e:
            print(str(e))

