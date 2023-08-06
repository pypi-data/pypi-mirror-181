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

from padrick.Model.TemplatedIdentifier import TemplatedIdentifierType


class TemplatedPortIdentifierType(str):
    def __init__(self, expression: str):
        super().__init__()
        if len(str(self).split(".")) != 2:
            raise ValueError(f"Illegal templated port identifier '{str(self)}':\n"
                             f"Must be of the form <templated_identifier>.<templated_identifier>")
        port_group_str, port_str = str(self).split(".", maxsplit=1)

        try:
            self._port_group = TemplatedIdentifierType(port_group_str)
            self._port = TemplatedIdentifierType(port_str)
        except ValueError as e:
            raise ValueError(f"Illegal templated port identifier '{str(self)}':\n{str(e)}")

    @property
    def identifier(self) -> str:
        return str(self)

    def evaluate_template(self, i):
        return self._port_group.evaluate_template(i)+"."+self._port.evaluate_template(i)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            expr = cls(v)
        except ValueError as e:
            raise ValueError(f'Error while parsing expression: {v}.\nError {str(e)}')
        return expr

    def __repr__(self):
        return self.__str__()
