from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from ..widget import AttributeNames, StateControl, Widget


@dataclass
class Selector(StateControl):
    options: Optional[List[Union[int, float, str, any]]] = None
    title: Optional[str] = None
    placeholder: Optional[str] = None
    label_by: Optional[str] = None
    value_by: Optional[str] = None
    default: Optional[Union[str, int, float, List[Union[int, float, str, any]]]] = None
    allow_multi_selection: Optional[bool] = None

    def __post_init__(self):
        # Check value is inside options
        self._check_value()

        if isinstance(self.options, list) and all((isinstance(x, dict)) for x in self.options):
            if self.label_by is None:
                raise Exception("You must indicate the label_by property")
            if self.value_by is None:
                raise Exception("You must indicate the value_by property")

    def from_string(self, string: str) -> Selector:
        self.default = string
        return self

    def to_string(self) -> str:
        return str(self.default)

    def from_int(self, number: int) -> Selector:
        self.default = number
        self._check_value()
        return self

    def to_int(self) -> int:
        return int(self.default)

    def from_float(self, number: float) -> Selector:
        self.default = number
        self._check_value()
        return self

    def to_float(self) -> float:
        return float(self.default)

    def from_list(self, input_list: List) -> Selector:
        self.default = input_list
        self.allow_multi_selection = True
        self._check_value()
        return self

    def to_list(self) -> List:
        return list(self.default)

    def _check_value(self):
        if self.default is not None and self.options is not None:
            if isinstance(self.default, list):
                for item in self.default:
                    if item not in self.options:
                        raise Exception(f"Value {self.default} must be in Options: {self.options}.")
            else:
                # Check when value is not a list.
                if self.default not in self.options:
                    raise Exception(f"Value {self.default} must be in Options: {self.options}.")

    def to_dict_widget(self, selector_dict: dict = None):
        if selector_dict is None:
            selector_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: Selector.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []

        if self.options is not None:
            if isinstance(self.options, Widget):
                target = {"id": self.options.widget_id, "target": AttributeNames.OPTIONS.value}
                _widget_providers.append(target)
            else:
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.OPTIONS.value: self.options,
                })

        if self.title is not None:
            if isinstance(self.title, str):
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title,
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be a string or another widget")

        if self.placeholder is not None:
            if isinstance(self.placeholder, str):
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.PLACEHOLDER.value: self.placeholder,
                })
            elif isinstance(self.placeholder, Widget):
                target = {"id": self.placeholder.widget_id, "target": AttributeNames.PLACEHOLDER.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Placeholder value should be a string or another widget")

        if self.label_by is not None:
            if isinstance(self.label_by, (str, int)):
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.LABEL_BY.value: self.label_by,
                })
            elif isinstance(self.label_by, Widget):
                target = {"id": self.label_by.widget_id, "target": AttributeNames.LABEL_BY.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Label_by value should be a string, int or another widget")

        if self.value_by is not None:
            if isinstance(self.value_by, (str, int)):
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE_BY.value: self.value_by,
                })
            elif isinstance(self.value_by, Widget):
                target = {"id": self.value_by.widget_id, "target": AttributeNames.VALUE_BY.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Value_by value should be a string, int or another widget")

        if self.default is not None:
            if isinstance(self.default, Widget):
                target = {"id": self.default.widget_id, "target": AttributeNames.VALUE.value}
                _widget_providers.append(target)
            else:
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.default,
                })

        if self.allow_multi_selection is not None:
            if isinstance(self.allow_multi_selection, bool):
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.ALLOW_MULTI_SELECTION.value: self.allow_multi_selection,
                })
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: allow_multi_selection value should be a string or another widget")

        if _widget_providers:
            self.add_widget_providers(selector_dict, _widget_providers)

        return selector_dict


class SelectorWidget(Widget, Selector):

    def __init__(self,
                 options: Optional[List[Union[int, float, str, any]]] = None,
                 title: Optional[str] = None,
                 placeholder: Optional[str] = None,
                 label_by: Optional[str] = None,
                 value_by: Optional[str] = None,
                 default: Optional[Union[str, int, float, List[Union[int, float, str, any]]]] = None,
                 allow_multi_selection: Optional[bool] = None,
                 **additional):
        Widget.__init__(self, Selector.__name__, 
                        compatibility = tuple([str.__name__, int.__name__, float.__name__, list.__name__,
                                      List._name, Selector.__name__]),
                        **additional)
        Selector.__init__(self, options=options, title=title, placeholder=placeholder, label_by=label_by,
                          value_by=value_by, default=default, allow_multi_selection=allow_multi_selection)
        self._parent_class = Selector.__name__
        
    def to_dict_widget(self):
        selector_dict = Widget.to_dict_widget(self)
        selector_dict = Selector.to_dict_widget(self, selector_dict)
        return selector_dict
