import pandas


class predictions:
    def __init__(self, data):
        """
        Given a single match dataframe, returns a dataframe with
        predictions added.
        :param data: DataFrame object.
        """
        self.data = data

        self.team_a = self.data.ix[self.data.index[1], 1]
        self.team_b = self.data.ix[self.data.index[2], 0]
        self.time = self.data.ix[self.data.index[1], 0]
        self.D14 = float(self.data.ix[self.data.index[1], 2])
        self.D15 = float(self.data.ix[self.data.index[2], 1])
        self.E14 = float(self.data.ix[self.data.index[1], 3])
        self.E15 = float(self.data.ix[self.data.index[2], 2])
        self.F14 = float(self.data.ix[self.data.index[1], 4])
        self.F15 = float(self.data.ix[self.data.index[2], 3])
        self.G14 = float(self.data.ix[self.data.index[1], 5])
        self.G15 = float(self.data.ix[self.data.index[2], 4])
        self.H14 = float(self.data.ix[self.data.index[1], 6])
        self.I14 = float(self.data.ix[self.data.index[1], 7])
        self.K14 = float(self.data.ix[self.data.index[1], 9])
        self.K15 = float(self.data.ix[self.data.index[2], 6])
        self.L14 = float(self.data.ix[self.data.index[1], 10])
        self.L15 = float(self.data.ix[self.data.index[2], 7])

    def return_predictions(self):
        """
        :return: DataFrame obj of match and predictions.
        """
        _configs = {
            'config_1': self.config_1(), 'config_2': self.config_2(),
            'config_3': self.config_3(), 'config_4': self.config_4(),
            'config_5': self.config_5(), 'config_6': self.config_6(),
            'config_7': self.config_7(), 'config_8': self.config_8(),
            'config_8a': self.config_8a(), 'config_9': self.config_9(),
            'config_9a': self.config_9a(), 'config_10': self.config_10(),
            'config_10a': self.config_10a(), 'config_11': self.config_11(),
            'config_11a': self.config_11a(), 'config_12': self.config_12(),
            'config_13': self.config_13(), 'config_14': self.config_14(),
            'config_15': self.config_15(), 'config_15a': self.config_15a(),
            'config_16': self.config_16(), 'config_17': self.config_17(),
            'config_17a': self.config_17a(), 'config_18': self.config_18(),
            'config_18a': self.config_18a()
        }
        transform = self.data.T.fillna(value='')
        temp_list = list(transform.iloc[:, 2])
        temp_list.insert(0, 0)
        del temp_list[-1]
        transform.iloc[:, 2] = temp_list
        result = transform.T.append(pandas.DataFrame.from_dict(_configs,
                                                               orient='index')
                                    .T)
        return [result.fillna(value=''), _configs]

    def config_1(self):
        if self.D15 > 0.24 and self.D15 < self.F15 and self.G15 < self.G14 \
                and self.E15 <= self.E14 and self.E15 >= self.G15:
            return 2
        else:
            return 0

    def config_2(self):
        if self.G14 < self.G15 and self.D14 == 0 and self.F14 > 0 and \
                self.E14 < self.G14:
            return 1
        else:
            return 0

    def config_3(self):
        if self.G14 < self.G15 and self.D14 == 0.25 and self.F14 < 0.25 and \
                self.E14 < self.G14:
            return 1
        else:
            return 0

    def config_4(self):
        if self.G15 < self.G14 and self.D15 == 0.25 and self.F15 < 0.25 and \
                self.E15 < self.G15:
            return 1
        else:
            return 0

    def config_5(self):
        if self.G14 < self.G15 and self.D14 == 0.5 and self.D14 < self.F14 \
                and self.E14 < self.E15:
            return 1
        else:
            return 0

    def config_6(self):
        if self.G15 < self.G14 and self.D15 == 0.75 and self.D15 > self.F15 \
                and self.E15 < self.G15:
            return 1
        else:
            return 0

    def config_7(self):
        if (self.F14 < 0 and self.D14 < self.F14 and self.H14 == self.I14
                and self.H14 == 3 and self.K14 < self.L14) or \
                (self.F15 < 0 and self.D15 < self.F15 and self.H14 == self.I14
                    and self.H14 == 3 and self.K14 < self.L14):
            return 1
        else:
            return 0

    def config_8(self):
        if (self.F14 < 0 and self.D14 > self.F14 and self.H14 == self.I14
                and 3.25 >= self.H14 <= 3 and self.K14 < self.L14) or \
                (self.F15 < 0 and self.D15 > self.F15 and self.H14 == self.I14
                    and 3.25 >= self.H14 <= 3 and self.K14 < self.L14):
            return 1
        else:
            return 0

    def config_8a(self):
        if (self.F14 < 0 and self.D14 > self.F14 and self.H14 < self.I14 and
                3.25 >= self.H14 <= 3 and self.K14 < 2) or \
                (self.F15 < 0 and self.D15 > self.F15 and self.H14
                    < self.I14 and 3.25 >= self.H14 <= 3 and self.K14 < 2):
            return 1
        else:
            return 0

    def config_9(self):
        if (self.D14 <= -0.5 and self.E14 < 1.9 and self.E15 >= 2 and
                self.H14 == self.I14 and self.K14 != self.L14 and self.K14
                > 2 and self.H14 > 2.25) or \
                    (self.D15 <= -0.5 and self.E15 < 1.9 and self.E14 >= 2
                        and self.H14 == self.I14 and self.K14 != self.L14 and
                        self.K14 > 2 and self.H14 > 2.25):
            return 1
        else:
            return 0

    def config_9a(self):
        if (self.D14 <= -1 and self.E14 < 1.9 and self.E15 >= 2 and
                self.H14 == self.I14 and self.K14 != self.L14 and self.K14 > 2
                and self.H14 <= 2.25) or \
                    (self.D15 <= -1 and self.E15 < 1.9 and self.E14 >= 2 and
                        self.H14 == self.I14 and self.K14 != self.L14 and
                        self.K14 > 2 and self.H14 <= 2.25):
            return 1
        else:
            return 0

    def config_10(self):
        if (self.D14 <= -0.5 and self.E14 < 1.9 and self.E15 >= 2 and
                self.H14 == self.I14 and self.H14 >= 2.5 and self.K14 <
                self.L14 and self.K14 < 2 and self.H14 > 2.25) or \
                    (self.D15 <= -0.5 and self.E15 < 1.9 and self.E14 >= 2
                        and self.H14 == self.I14 and self.K14 != self.L14 and
                        self.K14 > 2 and self.H14 > 2.25):
            return 1
        else:
            return 0

    def config_10a(self):
        if (self.D14 <= -0.5 and self.E14 < 1.9 and self.E15 >= 2 and
                self.H14 == self.I14 and self.H14 >= 2.5 and self.K14 <
                self.L14 and self.K14 < 2 and self.H14 > 2.25) or \
                    (self.D15 <= -0.5 and self.E15 < 1.9 and self.E14 >= 2 and
                        self.H14 == self.I14 and self.K14 != self.L14 and
                        self.K14 > 2 and self.H14 > 2.25):
            return 1
        else:
            return 0

    def config_11(self):
        if (self.D14 == self.F14 and self.G14 < self.G15 and self.E14 >
                self.E15 and self.H14 > 2.69 and self.K14 < self.L14) or \
                    (self.D14 == self.F14 and self.G15 < self.G14 and
                        self.E15 > self.E14 and self.H14 > 2.69 and
                        self.K14 < self.L14):
            return 1
        else:
            return 0

    def config_11a(self):
        if (self.D14 == self.F14 and self.G14 < self.G15 and self.E14 >
                self.E15 and self.H14 > 2.69 and self.K14 < self.L14) or \
                    (self.D14 == self.F14 and self.G15 < self.G14 and self.E15
                        > self.E14 and self.H14 > 2.69 and
                        self.K14 < self.L14):
            return 1
        else:
            return 0

    def config_12(self):
        if (self.D14 == 0.5 and 3 >= self.H14 <= 2.5 and self.H14 > self.I14) \
            or (self.D15 == 0.5 and 3 >= self.H14 <= 2.5 and
                self.H14 > self.I14):
            return 1
        else:
            return 0

    def config_13(self):
        if (self.F14 < 0 and self.D14 > self.F14 and self.H14 == self.I14
                and self.K14 < self.L14) or \
                (self.F14 > 0 and self.D14 < self.F14 and self.H14 == self.I14
                    and self.K14 < self.L14):
            return 1
        else:
            return 0

    def config_14(self):
        if (self.D14 == 0 and self.D14 > self.F14 and self.H14 == self.I14
                and self.H14 < 2.8 and self.K14 < self.L14 and self.K14 < 2):
            return 1
        else:
            return 0

    def config_15(self):
        if (self.D14 == self.F14 and self.G14 < self.G15 and self.E14 >
                self.E15 and self.H14 == self.I14 and 3.5 <= self.H14 and
                3.75 >= self.H14 and self.K14 < self.L14) or \
                    (self.D14 == self.F14 and self.G15 < self.G14 and self.E15
                        > self.E14 and self.H14 == self.I14 and 3.5 <= self.H14
                        and 3.75 >= self.H14 and self.K14 < self.L14):
            return 1
        else:
            return 0

    def config_15a(self):
        if (self.F14 < 0 and self.D14 > self.F14 and self.H14 == self.I14 and
                3.5 <= self.H14 and 3.75 >= self.H14 and self.K14 < self.L14) \
                    or (self.F15 < 0 and self.D15 > self.F15 and
                        self.H14 == self.I14 and 3.5 <= self.H14 and 3.75
                        >= self.H14 and self.K14 < self.L14):
            return 1
        else:
            return 0

    def config_16(self):
        if (self.D14 == 0 and self.D14 > self.F14 and self.H14 == self.I14
                and 2.5 <= self.H14 and 2.75 >= self.H14 and self.K14 <
                self.L14 and self.K14 < 2):
            return 1
        else:
            return 0

    def config_17(self):
        if (self.F14 < 0 and self.D14 < self.F14 and self.H14 >= 3 and
                self.H14 > self.I14 and self.K14 < 2) or \
                (self.F15 < 0 and self.D15 < self.F15 and self.H14 >= 3 and
                    self.H14 > self.I14 and self.K14 < 2):
            return 1
        else:
            return 0

    def config_17a(self):
        if (self.F14 < 0 and self.D14 < self.F14 and self.H14 == 2.75 and
                self.H14 > self.I14 and self.K14 < 1.9) or \
                    (self.F15 < 0 and self.D15 < self.F15 and self.H14 == 2.75
                        and self.H14 > self.I14 and self.K14 < 1.9):
            return 1
        else:
            return 0

    def config_18(self):
        if (self.D14 < self.D15 and self.D14 == self.F14 and self.G14 <
                self.G15 and self.E14 < self.G14 and self.H14 == self.I14 and
                self.H14 >= 3 and self.K14 < self.L14 and self.K14 < 2) or \
                    (self.D15 < self.D14 and self.D15 == self.F15 and
                     self.G15 < self.G14 and self.E15 < self.G15 and
                     self.H14 == self.I14 and self.H14 >= 3 and self.K14 <
                     self.L14 and self.K14 < 2):
            return 1
        else:
            return 0

    def config_18a(self):
        if (self.D14 < self.D15 and self.D14 == self.F14 and self.G14 <
                self.G15 and self.E14 < self.G14 and self.H14 == self.I14 and
                self.H14 == 2.75 and self.K14 < self.L14 and self.K14 <= 1.9)\
                 or (self.D15 < self.D14 and self.D15 == self.F15 and
                     self.G15 < self.G14 and self.E15 < self.G15 and
                     self.H14 == self.I14 and self.H14 == 2.75 and self.K14
                     < self.L14 and self.K14 <= 1.9):
            return 1
        else:
            return 0
