#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import itertools

import DataVisual.Tables as Table
import MPSPlots.Render2D as Plots


class DataV(object):
    def __init__(self, array, Xtable, Ytable, **kwargs):

        self.Data = array

        self.Xtable = Xtable if isinstance(Xtable, Table.XTable) else Table.XTable(Xtable)

        self.Ytable = Ytable if isinstance(Ytable, Table.YTable) else Table.YTable(Ytable)

    @property
    def Shape(self):
        return self.Data.shape

    def Mean(self, axis: str):
        """Method compute and the mean value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the mean value of axis.

        """
        Array = numpy.mean(self.Data, axis=axis.position)

        return DataV(Array, Xtable=[x for x in self.Xtable if x != axis], Ytable=self.Ytable)

    def std(self, axis: str):
        """
        Method compute and the std value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the std value of axis.

        """

        Array = numpy.mean(self.Data, axis=axis.position)

        return DataV(array=Array, Xtable=[x for x in self.Xtable if x != axis], Ytable=self.Ytable)

    def Rsd(self, axis: str):
        """Method compute and the rsd value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.
        rsd is defined as std/mean.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the rsd value of axis.

        """

        Array = numpy.std(self.Data, axis=self.Xtable.nameTable[axis]) \
                / numpy.mean(self.Data, axis=self.Xtable.nameTable[axis])

        return DataV(array=Array, Xtable=[x for x in self.Xtable if x != axis], Ytable=self.Ytable)

    def Plot(self, x, y, normalize: bool = False, std: Table.XParameter = None, **kwargs):
        y.values = self.Data

        Fig = Plots.Scene2D(unit_size=(12, 4))

        if normalize:
            y.normalize()

        ax = Plots.Axis(row=0, col=0, x_label=x.Label, y_label=y.Label, show_legend=True, **kwargs)

        Fig.AddAxes(ax)

        if std is not None:
            Artists = self.PlotSTD(x=x, y=y, std=std, **kwargs)
        else:
            Artists = self.PlotNormal(x=x, y=y, **kwargs)

        ax.AddArtist(*Artists)

        return Fig

    def _get_xTable_generator_(self, base_variable):
        Generators = []
        for x in self.Xtable:
            if x in base_variable:
                x.__base_variable__ = True
            else:
                x.__base_variable__ = False

            x.generator = x.iterate_through_values()
            Generators.append(x.generator)

        return itertools.product(*Generators)

    def PlotNormal(self, x: Table.XParameter, y: Table.XParameter, **kwargs):
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Args:
            x: Key of the self dict which represent the abscissa.
            y: Key of the self dict which represent the ordinate.

        """
        Artist = []

        for iteration in self._get_xTable_generator_(base_variable=[x]):
            CommonLabel = ""
            slicer = []
            DiffLabel = y.short_label

            for idx, value, common, diff in iteration:
                slicer += [idx]
                CommonLabel += common
                DiffLabel += diff

            data = y[tuple([y.position, *slicer])]

            Artist.append(Plots.Line(x=x.values, y=data, label=DiffLabel))

        Artist.append(Plots.Text(text=CommonLabel, position=[0.9, 0.9], font_size=8))

        return Artist

    def PlotSTD(self, x, y, std, **kwargs):
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Args:
            x: Key of the self dict which represent the abscissa.
            y: Key of the self dict which represent the ordinate.

        """

        Artist = []

        for iteration in self._get_xTable_generator_(base_variable=[x, std]):
            CommonLabel = ""
            slicer = []
            DiffLabel = y.short_label

            for idx, value, common, diff in iteration:
                slicer += [idx]
                CommonLabel += common
                DiffLabel += diff

            Ystd = numpy.std(self.Data, axis=std.position, keepdims=True)[tuple([y.position, *slicer])]
            Ymean = numpy.mean(self.Data, axis=std.position, keepdims=True)[tuple([y.position, *slicer])]

            Artist.append(Plots.STDLine(x=x.values, y_mean=Ymean.squeeze(), y_std=Ystd.squeeze(), label=DiffLabel))

        Artist.append(Plots.Text(text=CommonLabel, position=[0.9, 0.9], font_size=8))

        return Artist

    def __str__(self):
        name = [parameter.name for parameter in self.Ytable]

        text = f'DataVisual array: Variable: {name.__str__()}'

        text += "Parameter" + newLine

        for xParameter in self.Xtable:
            text += f"""| {xParameter.Label:40s}\
            | dimension = {xParameter.name:30s}\
            | size      = {xParameter.GetSize()}\
            \n"""

        return text
