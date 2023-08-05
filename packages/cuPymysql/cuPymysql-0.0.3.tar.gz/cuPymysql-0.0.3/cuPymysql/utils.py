import logging.handlers
from dataclasses import dataclass
from typing import Any, List, Optional, Set, Union


@dataclass
class Logger:
    """Logger class for logging"""
    log_dir: str
    log_level: str = "DEBUG"

    def __post_init__(self):
        self.logger = logging.getLogger("LOG")
        formatter = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s")
        file_handler = logging.FileHandler(self.log_dir)
        stream_handler = logging.StreamHandler()
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(self.log_level)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def exception(self, msg):
        self.logger.exception(msg)

    def log(self, level, msg):
        self.logger.log(level, msg)


class DataType:
    INT = "int"
    VARCHAR = "varchar"
    FLOAT = "float"
    DOUBLE = "double"
    TEXT = "text"
    BLOB = "blob"
    ENUM = "enum"
    SET = "set"
    TINYINT = "tinyint"
    SMALLINT = "smallint"
    MEDIUMINT = "mediumint"
    BIGINT = "bigint"
    DECIMAL = "decimal"
    DATE = "date"
    DATETIME = "datetime"
    NOT_NULL = "NOT NULL"
    AUTO_INCREMENT = "AUTO_INCREMENT"
    NULL = "NULL"
    DEFAULT = "default"

    @property
    def int(self, size: int = 11):
        return f"{self.INT}({size})"

    def varchar(self, size: int = 255):
        return f"{self.VARCHAR}({size})"

    def float(self, size: int = 11):
        return f"{self.FLOAT}({size})"

    def double(self, size: int = 11):
        return f"{self.DOUBLE}({size})"

    def text(self):
        return self.TEXT

    def blob(self):
        return self.BLOB

    def enum(self, *args):
        return f"{self.ENUM}({','.join(args)})"

    def set(self, *args):
        return f"{self.SET}({','.join(args)})"

    def tinyint(self, size: int = 4):
        return f"{self.TINYINT}({size})"

    def smallint(self, size: int = 6):
        return f"{self.SMALLINT}({size})"

    def mediumint(self, size: int = 9):
        return f"{self.MEDIUMINT}({size})"

    def bigint(self, size: int = 20):
        return f"{self.BIGINT}({size})"

    def decimal(self, size: int = 10, decimal: int = 2):
        return f"{self.DECIMAL}({size},{decimal})"

    def date(self):
        return self.DATE

    @property
    def _datetime(self):
        return self.DATETIME

    def not_null(self):
        return self.NOT_NULL

    def auto_increment(self):
        return self.AUTO_INCREMENT

    def null(self):
        return self.NULL

    def default(self, value):
        return f"{self.DEFAULT} {value}"


@dataclass
class Column:
    name: str
    data_type: DataType
    null: bool = False
    primary_key: bool = False
    auto_increment: bool = False
    default: Optional[Any] = None
    unique: bool = False


@dataclass
class Table:
    name: str
    columns: Union[List[str], Set[Column]]

    def create_table_query(self):
        query = f"CREATE TABLE {self.name} ("
        for column in self.columns:
            if isinstance(column, str):
                query += f"{column}, "
            else:
                query += f"{column.name} {column.data_type} "
                if not column.null:
                    query += f"{DataType.NOT_NULL} "
                if column.auto_increment:
                    query += f"{DataType.AUTO_INCREMENT} "
                if column.primary_key:
                    query += f"PRIMARY KEY "
                if column.unique:
                    query += f"UNIQUE "
                if column.defualt is not None:
                    query += f"{DataType.DEFAULT} {column.defualt} "
                query += ", "
        query = query[:-2]
        query += ");"
        return query
