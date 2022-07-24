from django.db import models

# vok - lotne związki organiczne

"""
[
  {
    "timestamp": 1658249939.278797,
    "temperature": 26.99,
    "humidity": 42.77,
    "pressure": 1016.099976,
    "voc": 19884
  },
  {
    "timestamp": 1658249894.8346677,
    "temperature": 26.98,
    "humidity": 42.384998,
    "pressure": 1016.099976,
    "voc": 20036
  },
  {
    "timestamp": 1658249872.3584795,
    "temperature": 26.98,
    "humidity": 42.183998,
    "pressure": 1016.099976,
    "voc": 19959
  }
]
"""


def load_charts_data(records: list) -> dict:
    plots = dict()

    for record in records:
        timestamp = record['timestamp']

        for key in record:
            if key == 'timestamp':
                continue
            elif key not in plots:
                plots[key] = Plot(key)

            plots[key].add_record(timestamp, record[key])

    return plots


class Plot:
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__timestamps = list()
        self.__values = list()

    def add_record(self, timestamp: float, value) -> None:
        self.__timestamps.append(int(timestamp))
        self.__values.append(value)

    def get_records(self) -> dict:
        return {
            'name': self.__name,
            'timestamps': self.__timestamps,
            'values': self.__values,
        }
