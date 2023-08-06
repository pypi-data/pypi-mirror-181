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

import re


def check_sv_literal(literal: str) ->str:
    pattern = re.compile(r"((\d+')?|')?(h[0-9a-fA-F]+|b[01xXzZ]+|(d)\d+|(o)?[0-7]+)")
    if not pattern.match(literal):
        raise ValueError(f"{literal} is not a supported SystemVerilog literal")
    return literal
