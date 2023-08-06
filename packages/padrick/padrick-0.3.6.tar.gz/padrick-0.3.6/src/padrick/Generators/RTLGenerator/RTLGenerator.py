# Manuel Eggimann <meggimann@iis.ee.ethz.ch>
#
# Copyright (C) 2021-2022 ETH Zürich
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib.resources as resources
import logging
import os
from pathlib import Path
from typing import Tuple, Mapping

import click_log
import hjson
from padrick.Generators.PadrickTemplate import PadrickTemplate
from padrick.Generators.GeneratorSettings import RTLTemplates
from padrick.Model import Constants
from padrick.Model.Padframe import Padframe
from reggen import gen_rtl as reggen_gen_rtl
from reggen import validate as reggen_validate
from reggen.ip_block import IpBlock

logger = logging.getLogger("padrick.RTLGenerator")
click_log.basic_config(logger)

template_package = 'padrick.Generators.RTLGenerator.Templates'

class RTLGenException(Exception):
    pass

def generate_rtl(templates: RTLTemplates, padframe: Padframe, dir: Path, header_text: str, vlnv=None, **extra_template_kwargs):
    os.makedirs(dir/"src", exist_ok=True)
    os.makedirs(dir/"include"/padframe.name, exist_ok=True)
    templates.toplevel_sv_package.render(dir/"src", logger=logger, padframe=padframe, header_text=header_text)

    next_pad_domain_reg_offset = 0 # Offset of the first register of the current pad_frame's register file. All
    address_ranges: Mapping[str, Tuple[int, int]] = {} # dictionary of pad_domain to start- end-address tupple
    # mappings. The end address is inclusive
    # registers in the padframe are mapped to a contiguous address space.
    for pad_domain in padframe.pad_domains:
        templates.pad_domain_top.render(dir /"src", logger=logger, padframe=padframe, pad_domain=pad_domain, header_text=header_text, **extra_template_kwargs)
        templates.pad_inst_module.render(dir /"src", logger=logger, padframe=padframe, pad_domain=pad_domain, header_text=header_text, **extra_template_kwargs)
        templates.internal_pkg.render(dir /"src", logger=logger, padframe=padframe, pad_domain=pad_domain, header_text=header_text, **extra_template_kwargs)
        templates.pad_mux_module.render(dir /"src", logger=logger, padframe=padframe, pad_domain=pad_domain, header_text=header_text, **extra_template_kwargs)
        templates.regfile_hjson.render(dir /"src", logger=logger, padframe=padframe, pad_domain=pad_domain,
                                       start_address_offset=hex(next_pad_domain_reg_offset), header_text=header_text, hw_version=Constants.HARDWARE_VERSION, **extra_template_kwargs)


        # Generate Register file using lowRisc reg_tool
        logger.debug("Invoking reggen to generate register file from Register file description")
        hjson_reg_file = dir/"src"/f"{padframe.name}_{pad_domain.name}_regs.hjson"
        try:
            obj = IpBlock.from_path(str(hjson_reg_file), [])
        except ValueError as e:
            logger.error(f"Fatal error while parsing auto generated register file for pad_domain {pad_domain.name}.")
            raise RTLGenException(f"Error parsing regfile.") from e
        address_ranges[pad_domain.name] = (next_pad_domain_reg_offset, obj.reg_blocks[None].offset)
        next_pad_domain_reg_offset = obj.reg_blocks[None].offset
        return_code = reggen_gen_rtl.gen_rtl(obj, (dir/"src").as_posix())
        if return_code != 0 and not (return_code is None):
            logger.error(f"Regtool template rendering of register file for pad domain {pad_domain.name} failed")
            raise RTLGenException("Reggen Rendering failed")

    templates.toplevel_module.render(dir / "src", logger=logger, padframe=padframe, address_ranges=address_ranges,
                                     address_space_size=next_pad_domain_reg_offset, header_text=header_text, **extra_template_kwargs)
    templates.assign_header_file.render(dir / "include" / padframe.name, logger=logger, padframe=padframe, header_text=header_text, **extra_template_kwargs)

    templates.bender_project_file.render(dir, logger=logger, padframe=padframe, header_text=header_text, templates=templates, **extra_template_kwargs)
    # Skip generation of FuseSoC core file if the config file does not contain a VLNV and we do not supply it externally
    if vlnv:
        templates.fusesoc_core_file.render(dir, logger=logger, padframe=padframe, header_text=header_text, templates=templates, vlnv=vlnv,  **extra_template_kwargs)
    templates.ipapprox_src_files_yml.render(dir, logger=logger, padframe=padframe, header_text=header_text, templates=templates, **extra_template_kwargs)
    templates.ipapprox_ips_list_yml.render(dir, logger=logger, padframe=padframe, header_text=header_text, **extra_template_kwargs)





