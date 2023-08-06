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

import json
import logging
from itertools import count

from mako.template import Template

import padrick
from padrick.Model.Constants import MANIFEST_VERSION, SYSTEM_VERILOG_IDENTIFIER, \
    OLD_MANIFEST_VERSION_COMPATIBILITY_TABLE, MANIFEST_VERSION_COMPATIBILITY
from padrick.Model.PadDomain import PadDomain
from pydantic import BaseModel, constr, conint, conlist, validator
from typing import List, Optional, Dict, Union

from padrick.Model.PadSignal import PadSignal, Signal
from padrick.Model.SignalExpressionType import SignalExpressionType
from padrick.Model.UserAttrs import UserAttrs

logger = logging.getLogger("padrick.Configparser")

class Padframe(BaseModel):
    """
    Padframe class that represents the padframe configuration parsed from the configuration file.

    Attributes:
        manifest_version (int): The manifest version used by the parsed configuration file.
        name (str): Name of the pad_frame module.
        description (str): An optional short description of the padframes.
        pad_domains (List[PadDomain): A list of PadDomains within this padframe.
    """
    manifest_version: int
    name: constr(regex=SYSTEM_VERILOG_IDENTIFIER)
    description: Optional[str]
    pad_domains: conlist(PadDomain, min_items=1)
    user_attr: Optional[UserAttrs]

    #Pydantic Model Config
    class Config:
        title =  "Padframe Config"
        json_encoders = {
            Template: lambda v: v.source,
            SignalExpressionType: lambda v: v.expression,
            PadSignal: lambda v: v.name,
            Signal: lambda  v: v.name
        }
        underscore_attrs_are_private = True


    @validator('manifest_version')
    def check_manifest_version(cls, version):
        """ Verifies that the configuration file has the right version number for the current version of padrick."""
        if version != MANIFEST_VERSION:
            if version in MANIFEST_VERSION_COMPATIBILITY:
                logger.warning(
                    f"Your padframe config file is using the outdated manifest version {version}. This version of padrick "
                    f"is still compatible but newer versions of padrick might eventually drop support for it. "
                    f"Consider upgrading your config files to version {MANIFEST_VERSION}.")
            else:
                if version > MANIFEST_VERSION:
                    raise ValueError(f"Manifest version {version} of the padframe config file is newer than this version "
                                     f"of padrick support. Either upgrade to the latest padrick version or change to an"
                                     f" older manifest version. This padrick version supports the following Manifests versions: "
                                     f"{', '.join([str(v) for v in MANIFEST_VERSION_COMPATIBILITY])}")
                if version < MANIFEST_VERSION:
                    raise ValueError(f"Manifest version {version} of the padframe config file is incompatible with the current version of padrick ({padrick.__version__}.\n"
                                     f"Please use Padrick version {OLD_MANIFEST_VERSION_COMPATIBILITY_TABLE[version]} instead.")
        return version
