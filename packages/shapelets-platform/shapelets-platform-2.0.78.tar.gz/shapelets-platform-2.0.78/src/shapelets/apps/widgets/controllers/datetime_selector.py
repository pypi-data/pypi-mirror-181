from __future__ import annotations

import datetime
import uuid

from dataclasses import dataclass
from typing import Optional, Tuple, Union

from ..widget import AttributeNames, StateControl, Widget


@dataclass
class DateSelector(StateControl):
    title: str = None
    date_time: Union[float, int, str, datetime.datetime, datetime.date, datetime.time] = None
    min_date: Union[float, int, str, datetime.date] = None
    max_date: Union[float, int, str, datetime.date] = None
    _format: Optional[str] = None
    _date_time_str = None
    _min_date_str = None
    _max_date_str = None

    def __post_init__(self):
        if self.date_time is not None:
            if isinstance(self.date_time, datetime.datetime):
                if (self.date_time.tzinfo is not None and self.date_time.tzinfo.utcoffset(self.date_time) is not None):
                    self._is_aware = True  # datetime is aware
                    self._date_time_str = self.date_time.strftime("%Y-%m-%d %H:%M:%S.%f %z")
                    self._format = 'YYYY-MM-DD HH:mm:ss TZ'

                else:
                    self._is_aware = False  # datetime is naive
                    self._date_time_str = self.date_time.strftime("%Y-%m-%d %H:%M:%S")
                    self._format = 'YYYY-MM-DD HH:mm:ss'

            elif isinstance(self.date_time, datetime.date):
                self._is_aware = False  # always date is naive
                self._date_time_str = self.date_time.strftime("%Y-%m-%d")
                self._format = 'YYYY-MM-DD'

            elif isinstance(self.date_time, datetime.time):
                if (self.date_time.tzinfo is not None and self.date_time.tzinfo.utcoffset(None) is not None):
                    self._is_aware = True  # time is aware
                    self._date_time_str = self.date_time.strftime("%H:%M:%S.%f %z")
                    self._format = 'HH:mm:ss TZ'
                else:
                    self._is_aware = False  # time is naive
                    self._date_time_str = self.date_time.strftime("%H:%M:%S")
                    self._format = 'HH:mm:ss'

            elif isinstance(self.date_time, str):
                self._validate_datetime()

            elif isinstance(self.date_time, float):
                self._check_datetime_float()

        if self.min_date is not None:
            if isinstance(self.min_date, str):
                self._validate_min_date()
            elif isinstance(self.min_date, datetime.date):
                pass
            elif isinstance(self.min_date, float) or isinstance(self.min_date, int):
                try:
                    self.min_date = datetime.datetime.fromtimestamp(self.min_date).strftime('%Y-%m-%d')
                except:
                    raise ValueError("Incorrect date format for min_date. Wrong float or int")

        if self.max_date is not None:
            if isinstance(self.max_date, str):
                self._validate_max_date()
            elif isinstance(self.max_date, datetime.date):
                pass
            elif isinstance(self.max_date, float) or isinstance(self.max_date, int):
                try:
                    self.max_date = datetime.datetime.fromtimestamp(self.max_date).strftime('%Y-%m-%d')
                except:
                    raise ValueError("Incorrect date format for max_date. Wrong float or int")

    def from_datetime(self, dt: datetime.datetime) -> DateSelector:
        self.date_time = dt
        return self

    def from_date(self, dt: datetime.date) -> DateSelector:
        self.date_time = dt
        return self

    def from_time(self, dt: datetime.time) -> DateSelector:
        self.date_time = dt
        return self

    def to_string(self) -> str:
        if isinstance(self.date_time, str):
            return self.date_time

        if isinstance(self.date_time, datetime.datetime):
            date_str = self.date_time.strftime("%Y-%m-%d, %H:%M:%S")
            return date_str

        if isinstance(self.date_time, datetime.date):
            date_str = self.date_time.strftime("%Y-%m-%d")
            return date_str

        if isinstance(self.date_time, datetime.time):
            date_str = self.date_time.strftime("%H:%M:%S")
            return date_str

        return self._date_time_str

    def to_datetime(self) -> datetime.datetime:
        if isinstance(self.date_time, datetime.datetime):
            return self.date_time

    def to_date(self) -> datetime.date:
        if isinstance(self.date_time, datetime.datetime):
            try:
                dt = datetime.datetime.strptime(self.date_time, '%Y-%m-%d').date()
                return dt
            except:
                return None

        elif isinstance(self.date_time, datetime.date):
            return self.date_time

        else:
            return None

    def to_time(self) -> datetime.time:
        if isinstance(self.date_time, datetime.datetime):
            try:
                dt = datetime.datetime.strptime(self.date_time, '%H:%M:%S').time()
                return dt
            except:
                try:
                    dt = datetime.datetime.strptime(self.date_time, '%I:%M:%S %p').time()
                    return dt
                except:
                    return None

        elif isinstance(self.date_time, datetime.time):
            return self.date_time

        else:
            return None

    def _validate_min_date(self):
        if isinstance(self.min_date, str):
            try:
                datetime.datetime.strptime(self.min_date, '%Y-%m-%d')
                self._min_date_str = self.min_date
            except ValueError:
                self._min_date_str = None
                raise ValueError("Incorrect date format for min_date, available format: YYYY-MM-DD")

    def _validate_max_date(self):
        if isinstance(self.max_date, str):
            try:
                datetime.datetime.strptime(self.max_date, '%Y-%m-%d')
                self._max_date_str = self.max_date
            except ValueError:
                self._max_date_str = None
                raise ValueError("Incorrect date format for max_date, available format: YYYY-MM-DD")

    def _check_datetime_aware(self):
        try:
            dt = datetime.datetime.strptime(self.date_time, '%Y-%m-%d %H:%M:%S.%f %z')
            self._date_time_str = self.date_time
            self._format = 'YYYY-MM-DD HH:mm:ss TZ'
        except:
            try:
                dt = datetime.datetime.strptime(self.date_time, '%Y-%m-%d %H:%M:%S.%f%z')
                self._date_time_str = self.date_time
                self._format = 'YYYY-MM-DD HH:mm:ss TZ'
            except:
                self._date_time_str = None

    def _check_datetime(self):
        try:
            dt = datetime.datetime.strptime(self.date_time, '%Y-%m-%d %H:%M:%S')
            self._format = 'YYYY-MM-DD HH:mm:ss'
            self._date_time_str = self.date_time
        except:
            try:
                dt = datetime.datetime.strptime(self.date_time, '%Y-%m-%d %I:%M:%S %p')
                self._format = 'YYYY-MM-DD h:mm:ss a'

                size = len(self.date_time)
                mod_string = self.date_time[:size - 3]
                self._date_time_str = mod_string
            except:
                self._date_time_str = None

    def _check_date(self):
        try:
            dt = datetime.datetime.strptime(self.date_time, '%Y-%m-%d').date()
            self._format = 'YYYY-MM-DD'
            self._date_time_str = self.date_time
        except:
            self._date_time_str = None

    def _check_time(self):
        try:
            dt = datetime.datetime.strptime(self.date_time, '%H:%M:%S').time()
            self._format = 'HH:mm:ss'
            self._date_time_str = self.date_time
        except:
            try:
                dt = datetime.datetime.strptime(self.date_time, '%I:%M:%S %p').time()
                self._format = 'h:mm:ss a'

                size = len(self.date_time)
                mod_string = self.date_time[:size - 3]
                self._date_time_str = mod_string
                self._date_time_str = mod_string
            except:
                self._date_time_str = None

    def _check_datetime_float(self):
        try:
            self._date_time_str = datetime.datetime.fromtimestamp(self.date_time).strftime('%Y-%m-%d %H:%M:%S')
            self._format = 'YYYY-MM-DD HH:mm:ss'
        except:
            self._date_time_str = None

    def _validate_datetime(self):

        if isinstance(self.date_time, str):

            self._check_datetime_aware()
            if self._date_time_str is None:
                self._check_datetime()
                if self._date_time_str is None:
                    self._check_date()
                    if self._date_time_str is None:
                        self._check_time()
                        if self._date_time_str is None:
                            raise ValueError("Incorrect date format")

    def to_dict_widget(self, date_dict: dict = None):
        if date_dict is None:
            date_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: DateSelector.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        _widget_providers = []
        if self.title is not None:
            if isinstance(self.title, str):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")

        
        if self.date_time is None:
            self.date_time = datetime.datetime.now() if self.min_date is None else self.min_date
        
        if self.date_time is not None:
            if isinstance(self.date_time, str):
                self._validate_datetime()

                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.DATE_TIME.value: self._date_time_str
                })

            elif isinstance(self.date_time, datetime.datetime):
                if (self.date_time.tzinfo is not None and self.date_time.tzinfo.utcoffset(self.date_time) is not None):
                    self._format = 'YYYY-MM-DD HH:mm:ss'
                    utc_datetime_obj = self.date_time.astimezone(datetime.timezone.utc)
                    self._date_time_str = utc_datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

                else:
                    self._date_time_str = self.date_time.strftime("%Y-%m-%d %H:%M:%S")
                    self._format = 'YYYY-MM-DD HH:mm:ss'

                if self._date_time_str is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.VALUE.value: self._date_time_str
                    })

            elif isinstance(self.date_time, datetime.date):
                self._date_time_str = self.date_time.strftime("%Y-%m-%d")
                self._format = 'YYYY-MM-DD'

                if self._date_time_str is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.VALUE.value: self._date_time_str
                    })

            elif isinstance(self.date_time, datetime.time):
                if (self.date_time.tzinfo is not None and self.date_time.tzinfo.utcoffset(None) is not None):
                    self._date_time_str = self.date_time.strftime("%H:%M:%S.%f %z")
                    self._format = 'HH:mm:ss TZ'
                else:
                    self._date_time_str = self.date_time.strftime("%H:%M:%S")
                    self._format = 'HH:mm:ss'

                if self._date_time_str is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.VALUE.value: self._date_time_str
                    })

            elif isinstance(self.date_time, (int, float)):
                self._check_datetime_float()
                if self._date_time_str is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.VALUE.value: self._date_time_str
                    })

            else:
                raise ValueError(f"Unexpected type {type(self.date_time)} in date_time")

        if self._format is not None:
            date_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.FORMAT.value: self._format
            })

        if self.min_date is not None:

            if isinstance(self.min_date, datetime.date):
                self._min_date_str = self.min_date.isoformat()
            elif isinstance(self.min_date, str):
                self._validate_min_date()
            elif isinstance(self.min_date, (float, int)):
                try:
                    self._min_date_str = datetime.datetime.fromtimestamp(self.min_date).strftime('%Y-%m-%d')
                except:
                    self._min_date_str = None
            else:
                self._min_date_str = None

            if self._min_date_str is not None:
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MIN_DATE.value: self._min_date_str
                })

        if self.max_date is not None:
            if isinstance(self.max_date, datetime.date):
                self._max_date_str = self.max_date.isoformat()
            elif isinstance(self.max_date, str):
                self._validate_max_date()
            elif isinstance(self.max_date, (float, int)):
                try:
                    self._max_date_str = datetime.datetime.fromtimestamp(self.max_date).strftime('%Y-%m-%d')
                except:
                    self._max_date_str = None
            else:
                self._max_date_str = None

            if self._max_date_str is not None:
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MAX_DATE.value: self._max_date_str
                })

        return date_dict


class DateSelectorWidget(DateSelector, Widget):

    def __init__(self, title: str = None,
                 date_time: Union[float, int, str, datetime.datetime, datetime.date, datetime.time] = None,
                 min_date: Union[float, int, str, datetime.date] = None,
                 max_date: Union[float, int, str, datetime.date] = None, **additional):
        Widget.__init__(self, DateSelector.__name__, 
                        compatibility = tuple([DateSelector.__name__, float, str,
                                      datetime.datetime, datetime.date, datetime.time]),
                        **additional)
        DateSelector.__init__(self, title=title, date_time=date_time, min_date=min_date, max_date=max_date)

        self._parent_class = DateSelector.__name__

    def to_dict_widget(self):
        date_dict = Widget.to_dict_widget(self)
        date_dict = DateSelector.to_dict_widget(self, date_dict)
        return date_dict
