import random

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


def random_color() -> str:
    return '#%02X%02X%02X' % (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))


def map_known_keys(key: str) -> str:
    map = {
        'temperature': 'Temperatura',
        'humidity': 'Wilgotność powietrza',
        'pressure': 'Ciśnienie',
        'voc': 'Lotne związki organiczne'
    }

    return map.get(key, key)


def load_charts_data(records: list, plot_name: str = None) -> dict:
    plots = dict()

    for record in records:
        if type(record) is not dict or 'timestamp' not in record.keys():
            continue

        timestamp = record['timestamp']

        for key in record:
            if key == 'timestamp':
                continue
            elif key not in plots:
                plots[key] = Plot(key, map_known_keys(key), random_color())

            if plot_name is None or key == plot_name:
                plots[key].add_record(timestamp, record[key])

    # Don't show plots with small amount of data
    for plot_name in plots:
        if plots[plot_name].count_records() < 50:
            plots.pop(plot_name)

    return plots


class Plot:
    def __init__(self, name: str, mapped_name: str, color: str) -> None:
        self.__name = name
        self.__mapped_name = mapped_name
        self.__color = color
        self.__timestamps = list()
        self.__values = list()

    def add_record(self, timestamp: float, value) -> None:
        if value is None:
            return

        self.__timestamps.append(int(timestamp * 1000))
        self.__values.append(value)

    def get_records(self) -> dict:
        return {
            'name': self.__name,
            'mapped_name': self.__mapped_name,
            'timestamps': self.__timestamps,
            'values': self.__values,
            'color': self.__color
        }

    def count_records(self) -> int:
        return len(self.__timestamps)
