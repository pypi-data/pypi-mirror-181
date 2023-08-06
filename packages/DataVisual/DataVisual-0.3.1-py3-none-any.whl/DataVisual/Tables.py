#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass

from MPSPlots.Utils import ToList


@dataclass
class XParameter(object):
    name: str = None
    values: str = None
    representation: str = None
    format: str = ""
    long_label: str = ""
    unit: str = ""
    short_label: str = ""
    position: int = None

    def __post_init__(self):
        self.values = ToList(self.values)

        if self.representation is None:
            self.representation = self.values

        self.values = self.values

        self.Label = self.long_label + f" [{self.unit}]" if self.long_label != "" else self.name
        self.short_label = self.short_label if self.short_label != "" else self.name

        self.__base_variable__ = None

    def Setvalues(self, values):
        self.values = values

    @property
    def has_unique_value(self):
        if self.values.shape[0] == 1:
            return True
        else:
            return False

    def normalize(self):
        self.unit = "U.A."
        self.values /= self.values.max()

    def __getitem__(self, item):
        return self.values[item]

    def __repr__(self):
        return self.name

    def GetSize(self):
        return self.values.shape[0]

    def __eq__(self, other):
        if other is None:
            return False

        return True if self.name == other.name else False

    def iterate_through_values(self):
        if self.__base_variable__ is True:
            yield slice(None), None, "", ""

        if self.__base_variable__ is False:
            for n, value in enumerate(self.representation):
                if self.has_unique_value:
                    CommonLabel = f" | {self.long_label} : {value}"
                    DiffLabel = ""
                else:
                    CommonLabel = ""
                    DiffLabel = f" | {self.long_label} : {value:{self.format}}"

                yield n, value, CommonLabel, DiffLabel


@dataclass
class XTable(object):
    X: numpy.array

    def __post_init__(self):

        self.X = numpy.array(self.X)
        self.Shape = [x.GetSize() for x in self.X]
        self.name2Idx = {x.name: order for order, x in enumerate(self.X)}

        self.CommonParameter = []
        self.DiffParameter = []

        for x in self:
            if x.values.size == 1:
                self.CommonParameter.append(x)
            else:
                self.DiffParameter.append(x)

    def Getvalues(self, Axis):
        return self[Axis].Value

    def Getposition(self, Value):
        for order, x in enumerate(self.X):
            if x == Value:
                return order

    def __getitem__(self, Val):
        if Val is None:
            return None

        Idx = self.name2Idx[Val] if isinstance(Val, str) else Val

        return self.X[Idx]



class YTable(object):
    def __init__(self, Y):
        self.Y = Y
        self.name2Idx = self.Getname2Idx()

        for n, y in enumerate(self.Y):
            y.position = n

    def GetShape(self):
        return [x.Size for x in self.Y] + [1]

    def Getname2Idx(self):
        return {x.name: order for order, x in enumerate(self.Y)}

    def __getitem__(self, Val):
        if isinstance(Val, str):
            idx = self.name2Idx[Val]
            return self.Y[idx]
        else:
            return self.Y[Val]

# -
