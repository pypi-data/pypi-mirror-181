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

from copy import deepcopy

from lark import Token
from lark.exceptions import UnexpectedInput
from lark.lark import Lark
from lark.tree import Tree
from lark.visitors import Transformer, v_args
from padrick.Model.TemplatedIndexGrammar import TemplatedIdxToStringTransformer, TemplatedIdxEvaluator, templated_index_grammar

grammar = r"""
?start: (idx_template | TEXT)*
TEXT: /[^{}]+/ 
"""

templated_string_parser = Lark(grammar + templated_index_grammar, parser='lalr')

class TemplatedStringType(str):
    _expression: str
    ast: Tree

    def __init__(self, expression: str):
        super().__init__()
        if expression == None:
            expression = ""
        self._ast = templated_string_parser.parse(str(expression))

    @property
    def identifier(self) -> str:
        return str(self)

    @property
    def ast(self):
        return self._ast

    def evaluate_template(self, i):
        if not isinstance(self.ast, Token):
            return TemplatedStringType((TemplatedIdxEvaluator(i) * TemplatedIdxToStringTransformer()).transform(self.ast))
        else:
            return self

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            expr = cls(v)
        except UnexpectedInput as e:
            raise ValueError(f'Error while parsing expression: {v}.\nError {str(e)}')
        return expr

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    expr = TemplatedStringType.validate("This is a test <i+10> !!!")
    print(expr.evaluate_template(42))
