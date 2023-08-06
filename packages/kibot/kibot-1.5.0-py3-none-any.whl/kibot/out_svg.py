# -*- coding: utf-8 -*-
# Copyright (c) 2020 Salvador E. Tropea
# Copyright (c) 2020 Instituto Nacional de Tecnología Industrial
# Copyright (c) 2018 John Beard
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
# Adapted from: https://github.com/johnbeard/kiplot
from pcbnew import (PLOT_FORMAT_SVG, FromMM, ToMM)
from .out_any_layer import AnyLayer
from .drill_marks import DrillMarks
from .gs import GS
from .macros import macros, document, output_class  # noqa: F401


class SVGOptions(DrillMarks):
    def __init__(self):
        super().__init__()
        with document:
            self.line_width = 0.25
            """ [0.02,2] For objects without width [mm] (KiCad 5) """
            self.mirror_plot = False
            """ Plot mirrored """
            self.negative_plot = False
            """ Invert black and white """
            self.svg_precision = 4
            """ [0,6] Scale factor used to represent 1 mm in the SVG (KiCad 6).
                The value is how much zeros has the multiplier (1 mm = 10 power `svg_precision` units).
                Note that for an A4 paper Firefox 91 and Chrome 105 can't handle more than 5 """
        self._plot_format = PLOT_FORMAT_SVG

    def _configure_plot_ctrl(self, po, output_dir):
        super()._configure_plot_ctrl(po, output_dir)
        po.SetMirror(self.mirror_plot)
        if GS.ki5:
            po.SetLineWidth(FromMM(self.line_width))
        po.SetNegative(self.negative_plot)
        if GS.ki6:
            po.SetSvgPrecision(self.svg_precision, False)

    def read_vals_from_po(self, po):
        super().read_vals_from_po(po)
        if GS.ki5:
            self.line_width = ToMM(po.GetLineWidth())
        self.negative_plot = po.GetNegative()
        self.mirror_plot = po.GetMirror()


@output_class
class SVG(AnyLayer):
    """ SVG (Scalable Vector Graphics)
        Exports the PCB to a format suitable for 2D graphics software.
        Unlike bitmaps SVG drawings can be scaled without losing resolution.
        This output is what you get from the File/Plot menu in pcbnew.
        The `pcb_print` is usually a better alternative. """
    def __init__(self):
        super().__init__()
        with document:
            self.options = SVGOptions
            """ *[dict] Options for the `svg` output """
        self._category = 'PCB/docs'
