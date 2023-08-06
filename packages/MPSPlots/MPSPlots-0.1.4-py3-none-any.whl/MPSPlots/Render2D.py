#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import numpy
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
from itertools import cycle
from . import CMAP

from dataclasses import dataclass


import matplotlib
matplotlib.style.use('ggplot')
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams["font.family"] = "serif"
plt.rcParams['axes.edgecolor'] = 'black'


linecycler = cycle(["-", "--", "-.", ":"])


@dataclass
class ColorBar:
    color: str = 'viridis'
    discreet: bool = False
    position: str = 'left'
    orientation: str = "vertical"
    symmetric: bool = False
    log_norm: bool = False
    numeric_format: str = ':.3f'
    n_ticks: int = None
    label_size: int = None

    def _render_(self, Ax, Scalar, Image) -> None:
        divider = make_axes_locatable(Ax._ax)
        cax = divider.append_axes(self.position, size="10%", pad=0.15)
        if self.discreet:
            unique_values = numpy.unique(Scalar)
            Norm = colors.BoundaryNorm(unique_values, unique_values.size + 1, extend='both')
            ticks = numpy.unique(Scalar)
            cbar = plt.colorbar(mappable=Image, norm=Norm, boundaries=ticks, cax=cax, orientation=self.orientation, format=self.numeric_format)

        elif self.log_norm and self.symmetric:
            Norm = matplotlib.colors.SymLogNorm(linthresh=1e-10)
            Norm.autoscale(Scalar)
            Image.set_norm(Norm)
            cbar = plt.colorbar(mappable=Image, norm=Norm, cax=cax, orientation=self.orientation, format=self.numeric_format)

        elif self.log_norm and not self.symmetric:
            Norm = matplotlib.colors.LogNorm(linthresh=0.03)
            Norm.autoscale(Scalar)
            Image.set_norm(Norm)
            cbar = plt.colorbar(mappable=Image, norm=Norm, cax=cax, orientation=self.orientation, format=self.numeric_format)

        elif not self.log_norm and self.symmetric:
            Norm = matplotlib.colors.TwoSlopeNorm(vcenter=0, vmax=numpy.abs(Scalar).max(), vmin=-numpy.abs(Scalar).max())
            Image.set_norm(Norm)
            cbar = plt.colorbar(mappable=Image, norm=Norm, cax=cax, orientation=self.orientation)

        else:
            cbar = plt.colorbar(mappable=Image, norm=None, cax=cax, orientation=self.orientation, format=self.numeric_format)

        if self.n_ticks is not None and not self.log_norm:
            cbar.ax.locator_params(nbins=self.n_ticks)

        if self.label_size is not None:
            cbar.ax.tick_params(labelsize=self.label_size)


@dataclass
class Contour:
    x: numpy.ndarray
    y: numpy.ndarray
    scalar: numpy.ndarray
    colormap: str = CMAP.BKR
    isolines: list = None

    def _render_(self, Ax) -> None:
        Ax.contour(self.x,
                   self.y,
                   self.scalar,
                   level=self.isolines,
                   colors="black",
                   linewidth=.5)

        Ax.contourf(self.x,
                    self.y,
                    self.scalar,
                    level=self.isolines,
                    cmap=self.colormap,
                    norm=colors.LogNorm())


@dataclass
class Mesh:
    x: numpy.ndarray
    y: numpy.ndarray
    scalar: numpy.ndarray
    colormap: str = CMAP.BKR

    def _render_(self, Ax):
        Image = Ax._ax.pcolormesh(self.x, self.y, self.scalar.T, cmap=self.colormap, shading='auto')
        Image.set_edgecolor('face')

        if Ax.colorbar is not None:
            Ax.colorbar._render_(Ax=Ax, Scalar=self.scalar, Image=Image)

        return Image


@dataclass
class FillLine:
    x: numpy.ndarray
    y0: numpy.ndarray
    y1: numpy.ndarray
    label: str = None
    fill: bool = False
    color: str = None
    line_style: str = None
    show_outline: bool = True

    def _render_(self, Ax) -> None:
        if self.line_style is None:
            self.line_style = next(linecycler)

        Ax._ax.fill_between(self.x, self.y0, self.y1, color=self.color, linestyle=self.line_style, alpha=0.7, label=self.label)

        if self.show_outline:
            Ax._ax.plot(self.x, self.y1, color='k', linestyle='-', linewidth=1)


@dataclass
class STDLine:
    x: numpy.ndarray
    y_mean: numpy.ndarray
    y_std: numpy.ndarray
    label: str = None
    color: str = None
    line_style: str = None

    def _render_(self, Ax):
        if self.line_style is None:
            self.line_style = next(linecycler)

        y0 = self.y_mean - self.y_std / 2
        y1 = self.y_mean + self.y_std / 2

        line = Ax._ax.plot(self.x, self.y_mean, color=self.color, label=self.label + '[mean]', linestyle=self.line_style)

        Ax._ax.fill_between(self.x, y0, y1, color=line[-1].get_color(), linestyle='-', alpha=0.3, label=self.label + '[std]')


@dataclass
class Line:
    x: numpy.ndarray
    y: numpy.ndarray
    label: str = None
    color: str = None
    line_style: str = None

    def _render_(self, Ax):
        if self.line_style is None:
            self.line_style = next(linecycler)

        if numpy.iscomplexobj(self.y):
            Ax._ax.plot(self.x, self.y.real, label=self.label + "[real]", color=self.color, linestyle=self.line_style)
            Ax._ax.plot(self.x, self.y.imag, label=self.label + "[imag]", color=self.color, linestyle=self.line_style)
        else:
            Ax._ax.plot(self.x, self.y, label=self.label, color=self.color, linestyle=self.line_style)


@dataclass
class Text:
    position: list = (0.9, 0.9)
    font_size: int = 8
    text: str = ''

    def _render_(self, Ax):
        art = AnchoredText(self.text,
                           loc='lower left',
                           prop=dict(size=self.font_size),
                           frameon=True,
                           bbox_to_anchor=(0.05, 1.0),
                           bbox_transform=Ax._ax.transAxes)

        Ax._ax.get_figure().add_artist(art)


@dataclass
class Scene2D:
    unit_size: tuple = (10, 3)
    tight_layout: bool = False
    title: str = ""

    def __post_init__(self):
        self.AxisGenerated = False
        self._Axis = []
        self.nCols = None
        self.nRows = None

    def font_size(self, value: int):
        for ax in self:
            ax.font_size = value

    def tick_size(self, value: int):
        for ax in self:
            ax.tick_size = value

    def x_limits(self, value: list):
        for ax in self:
            ax.x_limits = value

    def y_limits(self, value: list):
        for ax in self:
            ax.y_limits = value

    def x_label(self, value: list):
        for ax in self:
            ax.x_label = value

    def y_label(self, value: list):
        for ax in self:
            ax.y_label = value

    def water_mark(self, value: str):
        for ax in self:
            ax.water_mark = value

    def equal(self, value: bool):
        for ax in self:
            ax.equal = value

    def show_legend(self, value: bool):
        for ax in self:
            ax.show_legend = value

    def show_grid(self, value: bool):
        for ax in self:
            ax.show_grid = value

    def colorbar_n_ticks(self, value: int):
        for ax in self:
            ax.colorbar.n_ticks = value

    def colorbar_label_size(self, value: int):
        for ax in self:
            ax.colorbar.label_size = value

    font_size = property(None, font_size)
    tick_size = property(None, tick_size)
    x_limits = property(None, x_limits)
    y_limits = property(None, y_limits)
    x_label = property(None, x_label)
    y_label = property(None, y_label)
    water_mark = property(None, water_mark)
    equal = property(None, equal)
    show_legend = property(None, show_legend)
    show_grid = property(None, show_grid)
    colorbar_n_ticks = property(None, colorbar_n_ticks)
    colorbar_label_size = property(None, colorbar_label_size)

    def __getitem__(self, idx):
        return self.Axis[idx]

    @property
    def Axis(self):
        if not self.AxisGenerated:
            self._generate_axis_()

        return self._Axis

    def AddAxes(self, *Axis):
        for ax in Axis:
            self._Axis.append(ax)

        return self

    def _get_max_col_row_(self):
        max_row, max_col = 0, 0
        for ax in self._Axis:
            max_row = ax.row if ax.row > max_row else max_row
            max_col = ax.col if ax.col > max_col else max_col

        return max_row + 1, max_col + 1

    def _generate_axis_(self):
        max_row, max_col = self._get_max_col_row_()

        FigSize = [self.unit_size[0] * max_col, self.unit_size[1] * max_row]

        self.Figure = plt.figure(figsize=FigSize)

        grid = gridspec.GridSpec(ncols=max_col, nrows=max_row, figure=self.Figure)

        Ax = numpy.full(shape=(max_row, max_col), fill_value=None)

        for axis in self._Axis:
            subplot = self.Figure.add_subplot(grid[axis.row, axis.col], projection=axis.projection)
            Ax[axis.row, axis.col] = subplot

        self.Figure.suptitle(self.title)

        for ax in self._Axis:
            ax._ax = Ax[ax.row, ax.col]

        self.AxisGenerated = True

        return self

    def _render_(self):
        for ax in self.Axis:
            ax._render_()

        if self.tight_layout:
            plt.tight_layout()

        return self

    def Close(self):
        plt.close(self.Figure)

    def Show(self, SaveDir: str = None, **kwargs):
        self._render_()
        if SaveDir is not None:
            plt.savefig(fname=SaveDir, **kwargs)

        plt.show()

        return self


@dataclass
class Axis:
    row: int
    col: int
    x_label: str = None
    y_label: str = None
    title: str = ''
    show_grid: bool = True
    show_legend: bool = False
    x_scale: str = 'linear'
    y_scale: str = 'linear'
    x_limits: list = None
    y_limits: list = None
    equal_limits: bool = False
    equal: bool = False
    colorbar: ColorBar = None
    water_mark: str = ''
    Figure: Scene2D = None
    projection: str = None
    font_size: int = 10
    tick_size: int = 10

    def __post_init__(self):
        self._ax = None
        self.Artist = []

    def AddArtist(self, *Artist):
        for art in Artist:
            self.Artist.append(art)

    def _render_(self):
        logging.debug("Rendering Axis...")

        for art in self.Artist:
            art._render_(self)

        if self.x_limits is not None:
            self._ax.set_xlim(self.x_limits)

        if self.y_limits is not None:
            self._ax.set_ylim(self.y_limits)

        if self.equal_limits:
            x_max = max(self._ax.get_xlim())
            x_min = min(self._ax.get_xlim())
            y_max = max(self._ax.get_ylim())
            y_min = min(self._ax.get_ylim())

            max_lim = x_max if x_max > y_max else y_max
            min_lim = x_min if x_min > y_min else y_min

            self._ax.set_xlim([min_lim, max_lim])
            self._ax.set_ylim([min_lim, max_lim])

        self._decorate_ax_()

    def _decorate_ax_(self):
        if self.show_legend:
            self._ax.legend(fancybox=True, facecolor='white', edgecolor='k')

        if self.x_label is not None:
            self._ax.set_xlabel(self.x_label, fontsize=self.font_size)

        if self.y_label is not None:
            self._ax.set_ylabel(self.y_label, fontsize=self.font_size)

        if self.title is not None:
            self._ax.set_title(self.title, fontsize=self.font_size)

        if self.x_scale is not None:
            self._ax.set_xscale(self.x_scale)

        if self.y_scale is not None:
            self._ax.set_yscale(self.y_scale)

        if self.tick_size is not None:
            self._ax.tick_params(labelsize=self.tick_size)

        if self.equal:
            self._ax.set_aspect("equal")

        if self.show_grid:
            self._ax.grid(self.show_grid)

        if self.water_mark is not None:
            self._ax.text(0.5, 0.1, self.water_mark, transform=self._ax.transAxes,
                    fontsize=30, color='white', alpha=0.2,
                    ha='center', va='baseline')


def Multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)

    for fig in figs:
        fig.Figure.savefig(pp, format='pdf')

    pp.close()


# -
