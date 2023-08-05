"""Interpreter processes knitpass into knitout instructions"""
import os
from typing import List, Tuple, Any

from parglare import Grammar, Parser

from KnitScript.knit_graphs.Knit_Graph import Knit_Graph
from KnitScript.knit_script_interpreter.knit_script_actions import action
from KnitScript.knit_script_interpreter.knit_script_context import Knit_Script_Context
from KnitScript.knit_script_interpreter.statements.Statement import Statement
from KnitScript.knit_script_interpreter.statements.header_statement import Header_Statement


class Knit_Script_Interpreter:
    """
        A class to manage parsing a knit script file with parglare
    """
    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):
        """
        Instantiate
        :param debug_grammar: Will provide full parglare output for grammar states
        :param debug_parser: Will provide full parglare output for parsed file shift reduce status
        :param debug_parser_layout: Will provide layout information from parser
        """
        self._debug_parser_layout = debug_parser_layout
        self._debug_parser = debug_parser
        pg_loc = os.path.join(os.path.dirname(__file__), 'knit_script.pg')
        self._grammar = Grammar.from_file(pg_loc, debug=debug_grammar, ignore_case=True)
        # self._grammar = Grammar.from_string(knitscript_pg(), debug=debug_grammar, ignore_case=True)
        self._parser = Parser(self._grammar, debug=debug_parser, debug_layout=debug_parser_layout, actions=action.all)
        self._knit_pass_context = Knit_Script_Context()

    def _reset_context(self):
        """
        Resets the context of the knit_script_interpreter to a starting state with no set variables or operations on the machine
        """
        header = self._knit_pass_context.header
        self._knit_pass_context = Knit_Script_Context()
        self._knit_pass_context.header = header # resets machine state as well

    def interpret(self, pattern: str, pattern_is_file: bool = False) -> Tuple[List[Header_Statement], List[Statement]]:
        """
        Executes the parsing code for the parglare parser
        :param pattern: either a file or the knitspeak string to be parsed
        :param pattern_is_file: if true, assumes that the pattern is parsed from a file
        :return:
        """
        self._parser = Parser(self._grammar, debug=self._debug_parser, debug_layout=self._debug_parser_layout)
        if pattern_is_file:
            return self._parser.parse_file(pattern, extra=self._knit_pass_context)
        else:
            return self._parser.parse(pattern, extra=self._knit_pass_context)

    def write_knitout(self, pattern: str, out_file_name: str, pattern_is_file: bool = False, reset_context: bool = True) -> Tuple[List[str], Knit_Graph]:
        """
        Writes pattern knitout instructions to the out file
        Parameters
        ----------
        pattern: pattern or pattern file name to turn to knitout
        out_file_name: the output file name
        pattern_is_file: true if the pattern is a file name
        :param pattern_is_file: If true, interpret from file
        :param out_file_name: location to store knitout
        :param pattern: the pattern string or file name to interpret
        :param reset_context: If true, resets context at end of program
        """
        header, statements = self.interpret(pattern, pattern_is_file)
        for header_line in header:
            header_line.execute(self._knit_pass_context)
        for statement in statements:
            statement.execute(self._knit_pass_context)
        self._knit_pass_context.knitout.extend(self._knit_pass_context.machine_state.yarn_manager.cut_all_yarns())
        with open(out_file_name, "w") as out:
            out.writelines(self._knit_pass_context.knitout)
        knitgraph = self._knit_pass_context.machine_state.knit_graph
        knitout = self._knit_pass_context.knitout
        if reset_context:
            self._reset_context()
        return knitout, knitgraph

    def knit_script_evaluate_expression(self, exp) -> Any:
        """
        :param exp: expression to evaluate
        :return: evaluation result
        """
        return exp.evaluate(self._knit_pass_context)
