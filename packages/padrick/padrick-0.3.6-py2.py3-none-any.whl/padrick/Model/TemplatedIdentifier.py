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
from functools import lru_cache

from lark import Token, Transformer
from lark.exceptions import UnexpectedInput
from lark.lark import Lark
from lark.tree import Tree

from padrick.Model.TemplatedIndexGrammar import TemplatedIdxToStringTransformer, TemplatedIdxEvaluator, \
    templated_index_grammar

expression_language = r"""
?start: identifier

identifier: (UNDERSCORE|LETTER) (UNDERSCORE|LETTER|DIGIT|idx_template)*

// It would be cleaner to import those rules from Lark common grammar but this prevents pyoxidized binary creation 
// due to stupid package resource importing scheme used in lark
// Basic terminals for common use

//
// Numbers
//

DIGIT: "0".."9"
HEXDIGIT: "a".."f"|"A".."F"|DIGIT

INT: DIGIT+
SIGNED_INT: ["+"|"-"] INT
DECIMAL: INT "." INT? | "." INT

// float = /-?\d+(\.\d+)?([eE][+-]?\d+)?/
_EXP: ("e"|"E") SIGNED_INT
FLOAT: INT _EXP | DECIMAL _EXP?
SIGNED_FLOAT: ["+"|"-"] FLOAT

NUMBER: FLOAT | INT
SIGNED_NUMBER: ["+"|"-"] NUMBER

//
// Strings
//
_STRING_INNER: /.*?/
_STRING_ESC_INNER: _STRING_INNER /(?<!\\)(\\\\)*?/

ESCAPED_STRING : "\"" _STRING_ESC_INNER "\""


//
// Names (Variables)
//
LCASE_LETTER: "a".."z"
UCASE_LETTER: "A".."Z"

LETTER: UCASE_LETTER | LCASE_LETTER
WORD: LETTER+

CNAME: ("_"|LETTER) ("_"|LETTER|DIGIT)*

//
// Whitespace
//
WS_INLINE: (" "|/\t/)+
WS: /[ \t\f\r\n]/+

CR : /\r/
LF : /\n/
NEWLINE: (CR? LF)+


// Comments
SH_COMMENT: /#[^\n]*/
CPP_COMMENT: /\/\/[^\n]*/
C_COMMENT: "/*" /(.|\n)*?/ "*/"
SQL_COMMENT: /--[^\n]*/

"""

templated_identifier_parser = Lark(expression_language + templated_index_grammar, parser="lalr")

# class TokenMerger(Transformer):
#     def identifier(self, children):
#         merged_children = []
#         tokens_to_merge = []
#         for child in children:
#             if isinstance(child, str):
#                 tokens_to_merge.append(child)
#             else:
#                 if tokens_to_merge:
#                     merged_children.append("".join(tokens_to_merge))
#                     tokens_to_merge = []
#                 merged_children.append(child)
#         if tokens_to_merge:
#             merged_children.append("".join(tokens_to_merge))
#         if len(merged_children)

#@lru_cache()
def parse_expression(expression: str):
    return templated_identifier_parser.parse(str(expression))

class TemplatedIdentifierType(str):
    def __init__(self, expression: str):
        super().__init__()
        if expression == None:
            self._ast = ""
        else:
            try:
                self._ast = parse_expression(str(self))
            except UnexpectedInput as e:
                raise ValueError("Illegal identifier: "+str(e))


    @property
    def identifier(self) -> str:
        return str(self)

    @property
    def ast(self):
        return self._ast

    def evaluate_template(self, i):
        if not isinstance(self.ast, Token):
            return (TemplatedIdxEvaluator(i) * TemplatedIdxToStringTransformer()).transform(self._ast)
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
    expr = TemplatedIdentifierType.validate("test_{i+2:3d}")
    print(expr.evaluate_template(32))
