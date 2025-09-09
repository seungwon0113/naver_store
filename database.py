import types
from typing import Any, List, Optional, Tuple, Type, Union

import psycopg2

from envs import environments as envs


class Databases:
    def __init__(self) -> None:
        self.db = psycopg2.connect(
            host=envs.POSTGRES_HOST,
            dbname=envs.POSTGRES_DB,
            user=envs.POSTGRES_USER,
            password=envs.POSTGRES_PASSWORD,
            port=5432,
        )
        self.cursor = self.db.cursor()

    def __enter__(self) -> "Databases":
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[types.TracebackType],
    ) -> None:
        self.close()

    def close(self) -> None:
        self.cursor.close()
        self.db.close()

    def execute(
        self,
        query: str,
        args: Optional[Union[Tuple[Any, ...], List[Any]]] = None,
        fetch: bool = True,
    ) -> Optional[List[Tuple[Any, ...]]]:
        self.cursor.execute(query, args or ())
        if fetch:
            return self.cursor.fetchall()
        self.db.commit()
        return None

    def commit(self) -> None:
        self.db.commit()
