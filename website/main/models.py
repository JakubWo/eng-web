import random


def map_data_to_object(measurements: dict) -> list:
    plots = list()

    for key in measurements:
        plots.append(Plot(key, measurements[key]))

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
    def __init__(self, name: str, records: list):
        self.__name = name
        self.__mapped_name = map_known_keys(name)
        self.__records = records
        self.__color = random_color()

    def get_name(self):
        return self.__name

    def get_mapped_name(self):
        return self.__mapped_name

    def get_records(self):
        return self.__records

    def get_color(self):
        return self.__color

