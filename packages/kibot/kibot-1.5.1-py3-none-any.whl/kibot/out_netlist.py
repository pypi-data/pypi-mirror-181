# -*- coding: utf-8 -*-
# Copyright (c) 2022 Salvador E. Tropea
# Copyright (c) 2022 Instituto Nacional de Tecnología Industrial
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
"""
Dependencies:
  - from: KiAuto
    role: mandatory
    command: eeschema_do
    version: 2.0.0
"""
import os
from .gs import GS
from .optionable import BaseOptions
from .misc import FAILED_EXECUTE
from .kiplot import exec_with_retry, add_extra_options
from .macros import macros, document, output_class  # noqa: F401
from . import log

logger = log.get_logger()


class NetlistOptions(BaseOptions):
    def __init__(self):
        with document:
            self.output = GS.def_global_output
            """ *Filename for the output (%i=netlist/IPC-D-356, %x=net/d356) """
            self.format = 'classic'
            """ *[classic,ipc] The `classic` format is the KiCad internal format, and is generated
                from the schematic. The `ipc` format is the IPC-D-356 format, useful for PCB
                testing, is generated from the PCB """
        super().__init__()

    def config(self, parent):
        super().config(parent)
        if self.format == 'classic':
            self._expand_id = 'netlist'
            self._expand_ext = 'net'
            self._category = 'PCB/export'
        else:
            self._expand_id = 'IPC-D-356'
            self._expand_ext = 'd356'
            self._category = 'PCB/fabrication/verification'

    def get_targets(self, out_dir):
        return [self._parent.expand_filename(out_dir, self.output)]

    def run(self, name):
        command = self.ensure_tool('KiAuto')
        if self.format == 'ipc':
            command = command.replace('eeschema_do', 'pcbnew_do')
            subcommand = 'ipc_netlist'
            file = GS.pcb_file
        else:
            subcommand = 'netlist'
            file = GS.sch_file
        output_dir = os.path.dirname(name)
        # Output file name
        cmd = [command, subcommand, '--output_name', name, file, output_dir]
        cmd, video_remove = add_extra_options(cmd)
        # Execute it
        ret = exec_with_retry(cmd)
        if ret:
            logger.error(command+' returned %d', ret)
            exit(FAILED_EXECUTE)
        # Remove the video if needed
        if video_remove:
            video_name = os.path.join(self.expand_filename_pcb(GS.out_dir), command[:-3]+'_'+subcommand+'_screencast.ogv')
            if os.path.isfile(video_name):
                os.remove(video_name)


@output_class
class Netlist(BaseOutput):  # noqa: F821
    """ Netlist
        Generates the list of connections for the project.
        The netlist can be generated in the classic format and in IPC-D-356 format,
        useful for board testing """
    def __init__(self):
        super().__init__()
        with document:
            self.options = NetlistOptions
            """ *[dict] Options for the `netlist` output """

    @staticmethod
    def get_conf_examples(name, layers, templates):
        gb1 = {}
        gb1['name'] = 'classic_'+name
        gb1['comment'] = 'Schematic netlist in KiCad format'
        gb1['type'] = name
        gb1['dir'] = 'Export'
        gb2 = {}
        gb2['name'] = 'ipc_'+name
        gb2['comment'] = 'IPC-D-356 netlist for testing'
        gb2['type'] = name
        gb2['dir'] = 'Export'
        gb2['options'] = {'format': 'ipc'}
        return [gb1, gb2]
