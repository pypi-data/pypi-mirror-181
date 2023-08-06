from typing import Any
from pandas import DataFrame, read_sql, Series
from enum import Enum
from abc import ABC, abstractmethod
from .utils import VerbosePrintHandler


QUERY_ROW_LIMIT = 10_000_000


class FileFormat(str, Enum):
    CSV = "csv"


class ExportWritePolicy(str, Enum):
    APPEND = "append"
    FAIL = "fail"
    REPLACE = "replace"


class BaseIO(ABC):
    """
    Data connector interface. All data connectors must inherit from this interface.
    """

    def __init__(self, verbose=False) -> None:
        self.verbose = verbose
        self.printer = VerbosePrintHandler(
            f"{type(self).__name__} initialized", verbose=verbose
        )

    def _enforce_limit(self, query: str, limit: int = QUERY_ROW_LIMIT) -> str:
        """
        Modifies SQL SELECT query to enforce a limit on the number of rows returned by the query.
        This method is currently supports PostgreSQL syntax, which means it can be used with
        PostgreSQL, Amazon Redshift, Snowflake, and Google BigQuery.

        Args:
            query (str): The SQL query to modify
            limit (int): The limit on the number of rows to return.

        Returns:
            str: Modified query with limit on row count returned.
        """
        return f'SELECT * FROM ({query.strip(";")}) AS subquery LIMIT {limit};'

    @abstractmethod
    def load(self, *args, **kwargs) -> DataFrame:
        """
        Loads a data frame from source, returns it to memory. Subclasses must
        override this method to specify how this data frame is to be returned.

        Returns:
            DataFrame: dataframe returned by the source.
        """
        pass

    @abstractmethod
    def export(self, df: DataFrame, *args, **kwargs) -> None:
        """
        Exports the input dataframe to the specified source. Subclasses must override
        this method to specify of this data frame should be exported.

        Args:
            df (DataFrame): Data frame to export.
        """
        pass


class BaseSQLDatabase(BaseIO):
    """
    Base data connector for connecting to a SQL database. This adds `query` method which allows a user
    to send queries to the database server.
    """

    @abstractmethod
    def execute(self, query_string: str, **kwargs) -> None:
        """
        Sends query to the connected database

        Args:
            query_string (str): Query to send to the connected database.
            **kwargs: Additional arguments to pass to query, such as query configurations
        """
        pass

    def sample(
        self, schema: str, table: str, size: int = QUERY_ROW_LIMIT, **kwargs
    ) -> DataFrame:
        """
        Sample data from a table in the connected database. Sample is not
        guaranteed to be random.

        Args:
            schema (str): The schema to select the table from.
            size (int): The number of rows to sample. Defaults to 100,000
            table (str): The table to sample from in the connected database.

        Returns:
            DataFrame: Sampled data from the data frame.
        """
        return self.load(f"SELECT * FROM {schema}.{table} LIMIT {str(size)};", **kwargs)

    def _clean_query(self, query_string: str) -> str:
        """
        Cleans query before sending to database. Cleaning steps include:
        - Removing surrounding whitespace, newlines, and tabs

        Args:
            query_string (str): Query string to clean

        Returns:
            str: Clean query string
        """
        return query_string.strip(" \n\t")


class BaseSQLConnection(BaseSQLDatabase):
    """
    Data connector for connected SQL data sources. Can be used as a context manager or by
    manually opening or closing the connection to the SQL data source after data loading
    is complete.

    WARNING: queries may continue to run on data source unless connection manually closed.
    For this reason it is recommended to use a context
    manager when connecting to external data sources.
    """

    def __init__(self, verbose=False, **kwargs) -> None:
        """
        Initializes the connection with the settings given as keyword arguments.
        Specific data connectors will have access to different settings.
        """
        super().__init__(verbose=verbose)
        self.settings = kwargs

    def close(self) -> None:
        """
        Close the underlying connection to the SQL data source if open. Else will do nothing.
        """
        if "_ctx" in self.__dict__:
            self._ctx.close()
            del self._ctx
        if self.verbose and self.printer.exists_previous_message:
            print("")

    def commit(self) -> None:
        """
        Commits all changes made to database since last commit
        """
        self.conn.commit()

    @property
    def conn(self) -> Any:
        """
        Returns the connection object to the SQL data source. The exact connection type depends
        on the source and the definition of the data connector.
        """
        try:
            return self._ctx
        except AttributeError:
            raise ConnectionError(
                "No connection currently open. Open a new connection to access this property."
            )

    @abstractmethod
    def open(self) -> None:
        """
        Opens an underlying connection to the SQL data source.
        """
        pass

    def rollback(self) -> None:
        """
        Rolls back (deletes) all changes made to database since last commit.
        """
        self.conn.rollback()

    def __del__(self):
        self.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()
