import uuid

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from ..widget import Widget, AttributeNames
from .panel import PanelWidget, Panel


@dataclass
class VerticalLayout(Panel):
    placements: dict = field(default_factory=lambda: {})

    def place(self, widget: Widget, width: float = 100.0, offset: int = 0):
        """
        Place widget inside layout
        param widget: widget to place.
        param width: understood as a percentage.
        param offset: distance with the next widget.
        """
        if width > 100:
            raise Exception("Width cannot be over a 100")
        self.widgets.append(widget)
        # self.placements[widget.widget_id] = (width, offset)

    def to_dict_widget(self):
        panel_dict = {
            AttributeNames.ID.value: self.panel_id if self.panel_title else str(uuid.uuid1()),
            AttributeNames.TYPE.value: VerticalLayout.__name__,
            AttributeNames.DRAGGABLE.value: self.draggable,
            AttributeNames.RESIZABLE.value: self.resizable,
            AttributeNames.DISABLED.value: self.disabled,
            AttributeNames.PROPERTIES.value: {}
        }
        if self.panel_title is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                "panel_title": self.panel_title
            })

        if self.placements is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.PLACEMENTS.value: [{
                    AttributeNames.WIDGET_REF.value: key,
                    AttributeNames.WIDTH.value: width,
                    AttributeNames.OFFSET.value: offset
                } for key, (width, offset) in self.placements.items()]
            })

        if self.widgets is not None:
            widgets = [widget.to_dict_widget() for widget in self.widgets]
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.WIDGETS.value: widgets
            })
        # panel_dict[AttributeNames.PROPERTIES.value].update({
        #     AttributeNames.PLACEMENTS.value: [{
        #         AttributeNames.WIDGET_REF.value: key,
        #         AttributeNames.WIDTH.value: width,
        #         AttributeNames.OFFSET.value: offset
        #     } for key, (width, offset) in self.placements.items()]
        # })
        return panel_dict


class VerticalLayoutWidget(PanelWidget):
    """
    Creates a layout that holds widget inside it vertically (stacked on-top of one another).
    """

    def __init__(self,
                 panel_title: Optional[str] = None,
                 panel_id: Optional[str] = None,
                 **additional):
        self._parent_class = VerticalLayout.__name__
        super().__init__(panel_title, panel_id, 
                         compatibility =  tuple([list.__name__, List._name, VerticalLayout.__name__]),
                         **additional)
        self.placements = dict()

    def place(self, widget: Widget, width: float = 100.0, offset: int = 0):
        """
        Place widget inside layout
        param widget: widget to place.
        param width: understood as a percentage.
        param offset: distance with the next widget.
        """
        if width > 100:
            raise Exception("Width cannot be over a 100")
        super()._place(widget)
        self.placements[widget.widget_id] = (width, offset)

    def to_dict_widget(self):
        panel_dict = super().to_dict_widget()
        panel_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.PLACEMENTS.value: [{
                AttributeNames.WIDGET_REF.value: key,
                AttributeNames.WIDTH.value: width,
                AttributeNames.OFFSET.value: offset
            } for key, (width, offset) in self.placements.items()]
        })
        return panel_dict
