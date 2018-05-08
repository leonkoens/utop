import logging


class Period:

    def __init__(self, ticks_max):
        self.ticks_max = ticks_max
        self.ticks = []

    def add_tick(self, tick):
        self.ticks.append(tick)
        self.ticks = self.ticks[-1 * self.ticks_max:]

    def is_list(self):
        # Get the latest tick.
        latest = self.ticks[-1]

        # Check if this is a Period of Lists, in that case the calculation of the delta is
        # different
        return 'List' in latest.__class__.__name__

    def get_delta(self, values):
        delta = {}

        # Get the latest tick.
        latest = self.ticks[-1]
        latest_data = latest.get_data()

        if not self.is_list():
            # Remove the keys that weren't asked for.
            for remove in set(latest_data.keys()) - set(values):
                del latest_data[remove]


        # Search for the keys in the other ticks.
        for key in latest_data.keys():
            for i in range(self.ticks_max):

                tick = self.ticks[i]
                tick_data = tick.get_data()

                # If the key is present in this tick, then we can calculate the delta and break the
                # loop.
                if key in tick_data:

                    if self.is_list():
                        # If this is a list object then the values we want are in the data of the
                        # tick.

                        latest_element_data = latest_data[key]
                        tick_element_data = tick_data[key]

                        element_delta = {}

                        for value in values:
                            element_delta[value] = \
                                float(latest_element_data[value]) - float(tick_element_data[value])

                        delta[key] = element_delta
                    else:
                        # If it is not a list object then the key is already ony of the values we
                        # want.
                        delta[key] = float(latest_data[key]) - float(tick_data[key])

                    break

            # If the key wasn't found then the latest tick is all the data we have.
            if key not in delta:
                delta[key] = latest_data[key]

        return delta

    def get_list_totals(self, keys):
        totals = {}

        if not self.is_list():
            return totals

        for tick in self.ticks:
            for list_key, list_value in tick.get_data().items():
                for key in keys:
                    value = float(list_value[key])
                    try:
                        totals[list_key][key] += value
                    except KeyError:
                        try:
                            totals[list_key][key] = value
                        except KeyError:
                            totals[list_key] = {key: value}

        return totals

    def get_total(self, keys):
        totals = {}

        for tick in self.ticks:
            tick_data = tick.get_data()
            for key in keys:
                try:
                    totals[key] += tick_data[key]
                except KeyError:
                    totals[key] = tick_data[key]

        return totals


