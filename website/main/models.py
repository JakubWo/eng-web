import random


def map_data_to_object(measurements: dict, period: str) -> list:
    plots = list()

    for key in measurements:
        plots.append(Plot(key, measurements[key], period))

    return plots


def map_known_keys(key: str) -> str:
    switch = {
        'temperature': 'Temperatura',
        'humidity': 'Wilgotność powietrza',
        'pressure': 'Ciśnienie',
        'voc': 'Lotne związki organiczne'
    }

    return switch.get(key, key)


def random_color() -> str:
    return '#%02X%02X%02X' % (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))


class Plot:
    def __init__(self, name: str, records: list, period: str):
        self.__name = name
        self.__mapped_name = map_known_keys(name)
        self.__color = random_color()
        self.__records = records
        self.__period = period

        if period != 'cały okres' and period != 'ostatnie 100':
            self.__records_length = len(records)
            self.__time_gaps = self.get_time_gaps()
            self.__time_gaps_length = len(self.__time_gaps)

    def get_time_gaps(self) -> list:
        time_gaps = list()
        for i in range(1, self.__records_length):
            time_gaps.append(self.__records[i-1]['timestamp'] - self.__records[i]['timestamp'])

        return time_gaps

    def get_name(self) -> str:
        return self.__name

    def get_mapped_name(self) -> str:
        return self.__mapped_name

    def get_color(self) -> str:
        return self.__color

    def get_records(self) -> list:
        return self.__records

    def get_period(self) -> str:
        return self.__period

    def get_records_length(self) -> int:
        return self.__records_length

    def get_avg_value(self) -> float:
        return sum(record['value'] for record in self.__records) / self.__records_length

    def get_min_value(self) -> float:
        return min(record['value'] for record in self.__records)

    def get_max_value(self) -> float:
        return max(record['value'] for record in self.__records)

    def get_avg_period_between_records(self) -> float:
        return sum(time_gap for time_gap in self.__time_gaps) / len(self.__time_gaps)

    def get_min_period_between_records(self) -> int:
        return min(self.__time_gaps)

    def get_max_period_between_records(self) -> int:
        return max(self.__time_gaps)