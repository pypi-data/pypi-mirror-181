from __future__ import annotations

import datetime
import uuid

from dataclasses import dataclass
from typing import Optional, Tuple, Union

from ..widget import AttributeNames, StateControl, Widget


@dataclass
class DateRangeSelector(StateControl):
    title: str = None
    start_datetime: Union[float, int, str, datetime.datetime, datetime.date, datetime.time] = None
    end_datetime: Union[float, int, str, datetime.datetime, datetime.date, datetime.time] = None
    min_datetime: Union[float, int, str, datetime.date] = None
    max_datetime: Union[float, int, str, datetime.date] = None
    _format: Optional[str] = None

    def __post_init__(self):
        if self.start_datetime is not None:
            if isinstance(self.start_datetime, datetime.datetime):
                if (self.start_datetime.tzinfo is not None and self.start_datetime.tzinfo.utcoffset(
                        self.start_datetime) is not None):
                    self._is_aware = True  # datetime is aware
                    self.start_datetime.strftime("%Y-%m-%d %H:%M:%S.%f %z")
                    self._format = 'YYYY-MM-DD HH:mm:ss TZ'

                else:
                    self._is_aware = False  # datetime is naive
                    self.start_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    self._format = 'YYYY-MM-DD HH:mm:ss'

            elif isinstance(self.start_datetime, datetime.date):
                self._is_aware = False  # always date is naive
                self.start_datetime.strftime("%Y-%m-%d")
                self._format = 'YYYY-MM-DD'

            elif isinstance(self.start_datetime, datetime.time):
                if (self.start_datetime.tzinfo is not None and self.start_datetime.tzinfo.utcoffset(
                        None) is not None):
                    self._is_aware = True  # time is aware
                    self.start_datetime.strftime("%H:%M:%S.%f %z")
                    self._format = 'HH:mm:ss TZ'
                else:
                    self._is_aware = False  # time is naive
                    self.start_datetime.strftime("%H:%M:%S")
                    self._format = 'HH:mm:ss'

            elif isinstance(self.start_datetime, str):
                self._validate_datetime(self.start_datetime)

            elif isinstance(self.start_datetime, float):
                self._check_datetime_float(self.start_datetime)

        if self.min_datetime is not None:
            if isinstance(self.min_datetime, str):
                self._validate_date(self.min_datetime)
            elif isinstance(self.min_datetime, datetime.date):
                pass
            elif isinstance(self.min_datetime, float) or isinstance(self.min_datetime, int):
                try:
                    self.min_datetime = datetime.datetime.fromtimestamp(self.min_datetime).strftime('%Y-%m-%d')
                except:
                    raise ValueError("Incorrect date format for min_datetime. Wrong float or int")

        if self.max_datetime is not None:
            if isinstance(self.max_datetime, str):
                self._validate_date(self.max_datetime)
            elif isinstance(self.max_datetime, datetime.date):
                pass
            elif isinstance(self.max_datetime, float) or isinstance(self.max_datetime, int):
                try:
                    self.max_datetime = datetime.datetime.fromtimestamp(self.max_datetime).strftime('%Y-%m-%d')
                except:
                    raise ValueError("Incorrect date format for max_datetime. Wrong float or int")

    def _validate_date(self, date):
        if isinstance(date, str):
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
                return date
            except ValueError:
                return None

    def _check_datetime_aware(self, date):
        try:
            dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f %z')
            self._format = 'YYYY-MM-DD HH:mm:ss TZ'
            return date
        except:
            try:
                dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f%z')
                self._format = 'YYYY-MM-DD HH:mm:ss TZ'
                return date
            except:
                return None

    def _check_datetime(self, date):
        try:
            dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            self._format = 'YYYY-MM-DD HH:mm:ss'
            return date
        except:
            try:
                dt = datetime.datetime.strptime(self.start_datetime, '%Y-%m-%d %I:%M:%S %p')
                self._format = 'YYYY-MM-DD h:mm:ss a'
                size = len(date)
                mod_string = date[:size - 3]
                return mod_string
            except:
                return None

    def _check_date(self, date):
        try:
            dt = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            self._format = 'YYYY-MM-DD'
            return date
        except:
            return None

    def _check_time(self, time):
        try:
            dt = datetime.datetime.strptime(time, '%H:%M:%S').time()
            self._format = 'HH:mm:ss'
            return time
        except:
            try:
                dt = datetime.datetime.strptime(time, '%I:%M:%S %p').time()
                self._format = 'h:mm:ss a'

                size = len(time)
                mod_string = self.start_datetime[:size - 3]
                return mod_string
            except:
                return None

    def _check_datetime_float(self, date):
        try:
            result = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
            self._format = 'YYYY-MM-DD HH:mm:ss'
            return result
        except:
            return None

    def _validate_datetime(self, date):

        if isinstance(date, str):

            result = self._check_datetime_aware(date)
            if result is None:
                result = self._check_datetime(date)
                if result is None:
                    result = self._check_date(date)
                    if result is None:
                        result = self._check_time(date)
                        if result is None:
                            raise ValueError("Incorrect date format")

            return result

    def to_dict_widget(self, date_dict: dict = None):
        if date_dict is None:
            date_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: DateRangeSelector.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }

        if self.title is not None:
            if isinstance(self.title, str):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
        
        if self.start_datetime is None:
            self.start_datetime = datetime.datetime.now() if self.min_datetime is None else self.min_datetime
        
        if self.end_datetime is None:
            self.end_datetime = datetime.datetime.now() if self.max_datetime is None else self.max_datetime
           
        if self.start_datetime is not None:
            if isinstance(self.start_datetime, str):
                result = self._validate_datetime(self.start_datetime)

                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.START_DATE.value: result
                })

            elif isinstance(self.start_datetime, datetime.datetime):
                if (self.start_datetime.tzinfo is not None and self.start_datetime.tzinfo.utcoffset(
                        self.start_datetime) is not None):
                    self._format = 'YYYY-MM-DD HH:mm:ss'
                    utc_datetime_obj = self.start_datetime.astimezone(datetime.timezone.utc)
                    result = utc_datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

                else:
                    result = self.start_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    self._format = 'YYYY-MM-DD HH:mm:ss'

                if result is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.START_DATE.value: result
                    })

            elif isinstance(self.start_datetime, datetime.date):
                result = self.start_datetime.strftime("%Y-%m-%d")
                self._format = 'YYYY-MM-DD'

                if result is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.START_DATE.value: result
                    })

            elif isinstance(self.start_datetime, datetime.time):
                if (self.start_datetime.tzinfo is not None and self.start_datetime.tzinfo.utcoffset(
                        None) is not None):
                    result = self.start_datetime.strftime("%H:%M:%S.%f %z")
                    self._format = 'HH:mm:ss TZ'
                else:
                    result = self.start_datetime.strftime("%H:%M:%S")
                    self._format = 'HH:mm:ss'

                if result is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.START_DATE.value: result
                    })

            elif isinstance(self.start_datetime, float) or isinstance(self.start_datetime, int):
                result = self._check_datetime_float(self.start_datetime)
                if result is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.START_DATE.value: result
                    })

        if self.end_datetime is not None:
            if isinstance(self.end_datetime, str):
                result = self._validate_datetime(self.end_datetime)

                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.END_DATE.value: result
                })

            elif isinstance(self.end_datetime, datetime.datetime):
                if (self.end_datetime.tzinfo is not None and self.end_datetime.tzinfo.utcoffset(
                        self.end_datetime) is not None):                   
                    self._format = 'YYYY-MM-DD HH:mm:ss'
                    utc_datetime_obj = self.end_datetime.astimezone(datetime.timezone.utc)
                    result = utc_datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

                else:
                    result = self.end_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    self._format = 'YYYY-MM-DD HH:mm:ss'

                if result is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.END_DATE.value: result
                    })

            elif isinstance(self.end_datetime, datetime.date):
                result = self.end_datetime.strftime("%Y-%m-%d")
                self._format = 'YYYY-MM-DD'

                if result is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.END_DATE.value: result
                    })

            elif isinstance(self.end_datetime, datetime.time):
                if (self.end_datetime.tzinfo is not None and self.end_datetime.tzinfo.utcoffset(None) is not None):
                    result = self.end_datetime.strftime("%H:%M:%S.%f %z")
                    self._format = 'HH:mm:ss TZ'
                    
                else:
                    result = self.end_datetime.strftime("%H:%M:%S")
                    self._format = 'HH:mm:ss'

                if result is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.END_DATE.value: result
                    })

            elif isinstance(self.end_datetime, float) or isinstance(self.end_datetime, int):
                result = self._check_datetime_float(self.end_datetime)
                if result is not None:
                    date_dict[AttributeNames.PROPERTIES.value].update({
                        AttributeNames.END_DATE.value: result
                    })

        if self._format is not None:
            date_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.FORMAT.value: self._format
            })

        if self.min_datetime is not None:

            if isinstance(self.min_datetime, datetime.date):
                result = self.min_datetime.isoformat()
            elif isinstance(self.min_datetime, str):
                result = self._validate_date(self.min_datetime)
            elif isinstance(self.min_datetime, float) or isinstance(self.min_datetime, int):
                try:
                    result = datetime.datetime.fromtimestamp(self.min_datetime).strftime('%Y-%m-%d')
                except:
                    result = None
            else:
                result = None

            if result is not None:
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MIN_DATE.value: result
                })

        if self.max_datetime is not None:

            if isinstance(self.max_datetime, datetime.date):
                result = self.max_datetime.isoformat()
            elif isinstance(self.max_datetime, str):
                result = self._validate_date(self.max_datetime)
            elif isinstance(self.max_datetime, float) or isinstance(self.max_datetime, int):
                try:
                    result = datetime.datetime.fromtimestamp(self.max_datetime).strftime('%Y-%m-%d')
                except:
                    result = None
            else:
                result = None

            if result is not None:
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MAX_DATE.value: result
                })

        return date_dict


class DatetimeRangeSelectorWidget(DateRangeSelector, Widget):

    def __init__(self,
                 title: str = None,
                 start_datetime: Union[float, int, str, datetime.datetime, datetime.date, datetime.time] = None,
                 end_datetime: Union[float, int, str, datetime.datetime, datetime.date, datetime.time] = None,
                 min_datetime: Union[float, int, str, datetime.datetime, datetime.date, datetime.time] = None,
                 max_datetime: Union[float, int, str, datetime.datetime, datetime.date, datetime.time] = None,
                 **additional):
        Widget.__init__(self, DateRangeSelector.__name__, 
                        compatibility= tuple([DateRangeSelector.__name__, float, str,
                                      datetime.datetime, datetime.date, datetime.time]),
                        **additional)
        DateRangeSelector.__init__(self, title=title, start_datetime=start_datetime, end_datetime=end_datetime,
                                   min_datetime=min_datetime, max_datetime=max_datetime)

        self._parent_class = DateRangeSelector.__name__
        
    def to_dict_widget(self):
        date_dict = Widget.to_dict_widget(self)
        date_dict = DateRangeSelector.to_dict_widget(self, date_dict)
        return date_dict
