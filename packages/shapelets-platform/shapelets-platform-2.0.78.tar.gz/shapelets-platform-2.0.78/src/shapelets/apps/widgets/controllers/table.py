from __future__ import annotations

import pandas as pd
import numpy as np
import uuid

from typing import Union, Optional, Tuple
from dataclasses import dataclass

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class Table(StateControl):
    data: Optional[pd.DataFrame] = None
    cols: Optional[Union[np.ndarray, list]] = None
    rows_per_page: Optional[int] = None
    tools_visible: Optional[bool] = None

    def from_dataframe(self, data: pd.DataFrame) -> Table:
        self.data = data
        return self

    def to_dataframe(self) -> pd.DataFrame:
        dataframe = self.data
        return dataframe

    def from_list(self, lista: list) -> Table:
        self.data = lista
        return self

    def to_list(self) -> list:
        lista = self.data.values.tolist() if self.data is not None else []
        return lista

    def to_dict_widget(self, table_dict: dict = None):
        if table_dict is None:
            table_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: Table.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        if self.data is not None:
            if isinstance(self.data, pd.DataFrame):
                table_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.COLS.value: list(self.data.columns)
                })
                df_json = self.data.to_json(orient='records')
                table_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.DATA.value: df_json,
                })

        if self.rows_per_page is not None:
            if isinstance(self.rows_per_page, int):
                table_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.ROWS_PER_PAGE.value: self.rows_per_page
                })

        if self.tools_visible is not None:
            if isinstance(self.tools_visible, int):
                table_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TOOLS_VISIBLE.value: self.tools_visible
                })

        return table_dict


class TableWidget(Table, Widget):

    def __init__(self,
                 data: Optional[pd.DataFrame] = None,
                 cols: Optional[Union[np.ndarray, list]] = None,
                 rows_per_page: Optional[int] = None,
                 tools_visible: Optional[bool] = None,
                 **additional):
        Widget.__init__(self, Table.__name__,
                        compatibility=tuple(
                            [pd.DataFrame.__name__, np.ndarray.__name__, list.__name__, Table.__name__]),
                        **additional)
        Table.__init__(self, data=data, cols=cols, rows_per_page=rows_per_page, tools_visible=tools_visible)
        self._parent_class = Table.__name__
        self._compatibility: Tuple = (pd.DataFrame.__name__, np.ndarray.__name__, list.__name__, Table.__name__)

    def to_dict_widget(self):
        table_dict = Widget.to_dict_widget(self)
        table_dict = Table.to_dict_widget(self, table_dict)
        return table_dict
