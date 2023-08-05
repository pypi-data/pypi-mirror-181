import uuid

from dataclasses import dataclass
from typing import Optional, Tuple

from ..widget import Widget, AttributeNames, StateControl


@dataclass
class AltairChart(StateControl):
    title: Optional[str] = None
    alt: any = None

    def to_dict_widget(self, alt_dict: dict = None):
        if alt_dict is None:
            alt_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: AltairChart.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }

        if (self.title is not None):
            alt_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TITLE.value: self.title
            })

        if (self.alt is not None):
            if not hasattr(self.alt, "to_json"):
                raise Exception("You must inject an altair chart")

            alt_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.VALUE.value: self.alt.to_json(indent=2)
            })

        return alt_dict


class AltairChartWidget(Widget, AltairChart):

    def __init__(self,
                 title: Optional[str] = None,
                 alt: Optional[any] = None,
                 **additional
                 ):
        Widget.__init__(self, 'AltairChart', 
                        compatibility= tuple([AltairChart.__name__, ]),
                        **additional)
        AltairChart.__init__(self, title=title, alt=alt)
        self._parent_class = AltairChart.__name__

    def to_dict_widget(self):
        alt_dict = Widget.to_dict_widget(self)
        alt_dict = AltairChart.to_dict_widget(self, alt_dict)
        return alt_dict
