# Copyright (c) 2022 Shapelets.io
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from .idataappsrepo import IDataAppsRepo

from ..db import connect, Connection, transaction
from ..model import DataAppField, DataAppProfile, PrincipalId


def _insert_dataapp(details: DataAppProfile, conn: Connection):
    conn.execute("""
            INSERT INTO dataapps 
            (name, major, minor, description, creationDate, updateDate, spec, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
                 [
                     details.name, details.major, details.minor, details.description,
                     details.creationDate, details.updateDate, details.spec, details.tags
                 ])


def _update_dataapp_by_id(dataapp_id: int, profile: Dict[str, Any], conn: Connection):
    pass


def _load_all(attributes: Set[DataAppField],
              skip: Optional[int],
              sort_by: Optional[List[Tuple[DataAppField, bool]]],
              limit: Optional[int],
              conn: Connection) -> List[DataAppProfile]:
    base_query = f"SELECT {', '.join(attributes)} FROM dataapps "
    if sort_by is not None:
        base_query += "ORDER BY "
        sort_expressions = [f"{s[0]} {'ASC' if s[1] else 'DESC'}" for s in sort_by]
        base_query += ', '.join(sort_expressions)
    if limit is not None:
        base_query += f" LIMIT {limit}"
    if skip is not None:
        base_query += f" OFFSET {skip}"

    conn.execute(base_query)
    result = []
    d = {}
    for r in conn.fetch_all():
        for idx, a in enumerate(attributes):
            d[a] = r[idx]
        result.append(DataAppProfile(**d))

    return result


def _load_dataapp_by_name(dataapp_name: str, conn: Connection) -> Optional[DataAppProfile]:
    conn.execute(""" 
        SELECT *
        FROM dataapps
        WHERE name = ?
        ORDER BY major desc, minor desc;
    """, [dataapp_name])

    record = conn.fetch_one()
    if record is None:
        return None

    return DataAppProfile(
        name=record[0],
        major=record[1],
        minor=record[2],
        description=record[3],
        creationDate=record[4],
        updateDate=record[5],
        spec=record[6],
        tags=record[7]
    )


def _load_dataapp_by_name_and_version(dataapp_name: str,
                                      dataapp_major: int,
                                      dataapp_minor: int,
                                      conn: Connection) -> Optional[DataAppProfile]:
    conn.execute(""" 
        SELECT *
        FROM dataapps
        WHERE name = ? AND major = ? AND minor = ?;
    """, [dataapp_name, dataapp_major, dataapp_minor])

    record = conn.fetch_one()
    if record is None:
        return None

    return DataAppProfile(
        name=record[0],
        major=record[1],
        minor=record[2],
        description=record[3],
        creationDate=record[4],
        updateDate=record[5],
        spec=record[6],
        tags=record[7]
    )


def _update_dataapp(dataapp_name: str,
                    major_version: int,
                    minor_version: int,
                    spec: str,
                    update_date: int,
                    conn: Connection) -> Optional[DataAppProfile]:
    conn.execute(""" 
        UPDATE dataapps 
        SET spec = ? , updateDate = ?
        WHERE name = ? AND major = ? AND minor = ?;
    """, [spec, update_date, dataapp_name, major_version, minor_version])


def _delete_dataapp(dataapp_name: str, major: int, minor: int, conn: Connection):
    conn.execute("DELETE FROM dataapps WHERE name = ? AND major = ? AND minor = ?;",
                 [dataapp_name, major, minor]);


def _clear_all_dataapps(conn: Connection):
    conn.execute("DELETE FROM dataapps;")


def _get_dataapp_principals(dataapp_id: int, conn: Connection) -> List[PrincipalId]:
    pass
    # conn.execute("SELECT scope, id FROM principals where id = ?;", [dataapp_id])
    # records = conn.fetch_all()
    # return [PrincipalId(scope=str(r[0]), id=str(r[1])) for r in records]


def _get_dataapp_versions(dataapp_name: str, conn: Connection):
    conn.execute(""" 
        SELECT major, minor
        FROM dataapps
        WHERE name = ? 
        ORDER BY major DESC and minor DESC;
    """, [dataapp_name])

    result = []
    for r in conn.fetch_all():
        version = float(f"{r[0]}.{r[1]}")
        result.append(version)
    return result


def _get_dataapp_tags(dataapp_name: str, conn: Connection):
    conn.execute(""" 
        SELECT tags
        FROM dataapps
        WHERE name = ? 
        ORDER BY major DESC and minor DESC;
    """, [dataapp_name])

    result = conn.fetch_one()
    return result


class DataAppsRepo(IDataAppsRepo):

    def create(self, details: DataAppProfile) -> Optional[DataAppProfile]:
        with transaction() as conn:
            dataapp_name = details.name
            # Set Update Date
            details.updateDate = int(datetime.now().timestamp())
            if details.major is None and details.minor is None:
                # if details.version is None:
                details.creationDate = int(datetime.now().timestamp())
                # check if dataApp exists
                dataapp = _load_dataapp_by_name(dataapp_name, conn)
                if dataapp:
                    # If existed, increase minor version
                    details.major = dataapp.major
                    details.minor = dataapp.minor + 1
                else:
                    # first time dataApp is registered
                    details.major = 0
                    details.minor = 1
                _insert_dataapp(details, conn)
            else:
                # user provides version
                dataapp = _load_dataapp_by_name_and_version(dataapp_name, details.major, details.minor, conn)
                if dataapp:
                    # If dataapp exists with same version -> Update spec
                    _update_dataapp(dataapp_name, details.major, details.minor, details.spec, details.updateDate, conn)
                else:
                    # Otherwise, insert new version
                    details.creationDate = int(datetime.now().timestamp())
                    _insert_dataapp(details, conn)
            return _load_dataapp_by_name(dataapp_name, conn)

    def load_by_name(self, dataapp_name: str) -> Optional[DataAppProfile]:
        with connect() as conn:
            return _load_dataapp_by_name(dataapp_name, conn)

    def load_by_principal(self, principal: PrincipalId) -> Optional[DataAppProfile]:
        pass

    def delete_by_name(self, dataapp_name: str, major: int, minor: int):
        with connect() as conn:
            _delete_dataapp(dataapp_name, major, minor, conn)

    def load_all(self,
                 attributes: Set[DataAppField],
                 skip: Optional[int],
                 sort_by: Optional[List[Tuple[DataAppField, bool]]],
                 limit: Optional[int]) -> List[DataAppProfile]:
        with connect() as conn:
            return _load_all(attributes, sort_by, skip, limit, conn)

    def delete_all(self):
        with transaction() as conn:
            # _clear_all_principals(conn)
            _clear_all_dataapps(conn)

    def get_dataapp_versions(self, dataapp_name: str) -> List[float]:
        with connect() as conn:
            return _get_dataapp_versions(dataapp_name, conn)

    def get_dataapp_by_version(self, dataapp_name: str, major: int, minor: int) -> DataAppProfile:
        with connect() as conn:
            return _load_dataapp_by_name_and_version(dataapp_name, major, minor, conn)

    def get_dataapp_last_version(self, dataapp_name: str) -> float:
        with connect() as conn:
            return _get_dataapp_versions(dataapp_name, conn)[0]

    def get_dataapp_tags(self, dataapp_name: str) -> List[str]:
        with connect() as conn:
            return _get_dataapp_tags(dataapp_name, conn)[0]
