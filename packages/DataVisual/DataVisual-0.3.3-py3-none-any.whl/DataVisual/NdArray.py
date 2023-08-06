#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import itertools

import DataVisual.Tables as Table
import MPSPlots.Render2D as Plots


class DataV(object):
    def __init__(self, array, x_table, y_table, **kwargs):

        self._data = array

        self.x_table = x_table if isinstance(x_table, Table.Xtable) else Table.Xtable(x_table)

        self.y_table = y_table if isinstance(y_table, Table.Ytable) else Table.Ytable(y_table)

    @property
    def shape(self):
        return self._data.shape

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
        array = numpy.mean(self._data, axis=axis.position)

        return DataV(array, x_table=[x for x in self.x_table if x != axis], y_table=self.y_table)

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

        Array = numpy.mean(self._data, axis=axis.position)

        return DataV(array=Array, x_table=[x for x in self.x_table if x != axis], y_table=self.y_table)

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

        Array = numpy.std(self._data, axis=self.x_table.nameTable[axis]) \
                / numpy.mean(self._data, axis=self.x_table.nameTable[axis])

        return DataV(array=Array, x_table=[x for x in self.x_table if x != axis], y_table=self.y_table)

    def Plot(self, x, y, normalize: bool = False, std: Table.Xparameter = None, **kwargs):
        y.values = self._data

        Fig = Plots.Scene2D(unit_size=(12, 4))

        if normalize:
            y.normalize()

        ax = Plots.Axis(row=0, col=0, x_label=x.Label, y_label=y.Label, show_legend=True, **kwargs)

        Fig.AddAxes(ax)

        if std is not None:
            Artists = self._plot_std_(x=x, y=y, std=std, **kwargs)
        else:
            Artists = self._plot_normal_(x=x, y=y, **kwargs)

        ax.AddArtist(*Artists)

        return Fig

    def _get_x_table_generator_(self, base_variable):
        generator = []
        for x in self.x_table:
            if x in base_variable:
                x.__base_variable__ = True
            else:
                x.__base_variable__ = False

            x.generator = x.iterate_through_values()
            generator.append(x.generator)

        return itertools.product(*generator)

    def _plot_normal_(self, x: Table.Xparameter, y: Table.Xparameter, **kwargs):
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Args:
            x: Key of the self dict which represent the abscissa.
            y: Key of the self dict which represent the ordinate.

        """
        Artist = []

        for iteration in self._get_x_table_generator_(base_variable=[x]):
            common_label = ""
            slicer = []
            different_label = y.short_label

            for idx, value, common, diff in iteration:
                slicer += [idx]
                common_label += common
                different_label += diff

            data = y[tuple([y.position, *slicer])]

            Artist.append(Plots.Line(x=x.values, y=data, label=different_label))

        Artist.append(Plots.Text(text=common_label, position=[0.9, 0.9], font_size=8))

        return Artist

    def _plot_std_(self, x, y, std, **kwargs):
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Args:
            x: Key of the self dict which represent the abscissa.
            y: Key of the self dict which represent the ordinate.

        """

        Artist = []

        for iteration in self._get_x_table_generator_(base_variable=[x, std]):
            common_label = ""
            slicer = []
            different_label = y.short_label

            for idx, value, common, diff in iteration:
                slicer += [idx]
                common_label += common
                different_label += diff

            Ystd = numpy.std(self._data, axis=std.position, keepdims=True)[tuple([y.position, *slicer])]
            y_mean = numpy.mean(self._data, axis=std.position, keepdims=True)[tuple([y.position, *slicer])]

            Artist.append(Plots.STDLine(x=x.values, y_mean=y_mean.squeeze(), y_std=Ystd.squeeze(), label=different_label))

        Artist.append(Plots.Text(text=common_label, position=[0.9, 0.9], font_size=8))

        return Artist

# -
