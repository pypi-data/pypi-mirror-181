"""phml.virtual_python

Data strucutures to store the compiled locals and imports from
python source code.
"""
from __future__ import annotations

import ast
from html import escape
from re import finditer, sub
from typing import Any, Optional

from .built_in import built_in_funcs, built_in_types
from .import_objects import Import, ImportFrom

__all__ = ["VirtualPython", "get_vp_result", "process_vp_blocks"]


class VirtualPython:
    """Represents a python string. Extracts the imports along
    with the locals.
    """

    def __init__(
        self,
        content: Optional[str] = None,
        imports: Optional[list] = None,
        exposable: Optional[dict] = None,
    ):
        self.content = content or ""
        self.imports = imports or []
        self.exposable = exposable or {}

        if self.content != "":
            from phml.utilities import normalize_indent  # pylint: disable=import-outside-toplevel

            self.content = normalize_indent(content)
            # Extract imports from content
            for node in ast.parse(self.content).body:
                if isinstance(node, ast.ImportFrom):
                    self.imports.append(ImportFrom.from_node(node))
                elif isinstance(node, ast.Import):
                    self.imports.append(Import.from_node(node))

            # Retreive locals from content
            local_env = {}
            global_env = {**self.exposable, **globals()}
            exec(self.content, global_env, local_env)  # pylint: disable=exec-used
            self.exposable.update(local_env)

    def __add__(self, obj: VirtualPython) -> VirtualPython:
        local_env = {**self.exposable}
        local_env.update(obj.exposable)
        return VirtualPython(
            imports=[*self.imports, *obj.imports],
            exposable=local_env,
        )

    def __repr__(self) -> str:
        return f"VP(imports: {len(self.imports)}, locals: {len(self.exposable.keys())})"


def parse_ast_assign(vals: list[ast.Name | tuple[ast.Name]]) -> list[str]:
    """Parse an ast.Assign node."""

    values = vals[0]
    if isinstance(values, ast.Name):
        return [values.id]

    if isinstance(values, tuple):
        return [name.id for name in values]

    return []


def __validate_kwargs(
    kwargs: dict, expr: str, excludes: Optional[list] = None, safe_vars: bool = False
):
    """Validates the used variables and methods in the expression. If they are
    missing then they are added to the kwargs as None. This means that it will
    give a NoneType error if the method or variable is not provided in the kwargs.

    After validating all variables and methods to be used are in kwargs it then escapes
    all string kwargs for injected html.
    """
    excludes = excludes or []
    exclude_list = [*built_in_funcs, *built_in_types]

    for var in [
        name.id  # Add the non built-in missing variable or method as none to kwargs
        for name in ast.walk(ast.parse(expr))  # Iterate through entire ast of expression
        if isinstance(name, ast.Name)  # Get all variables/names used this can be methods or values
        and name.id not in exclude_list
        and name.id not in excludes
    ]:
        if var not in kwargs:
            kwargs[var] = None

    if not safe_vars:
        escape_args(kwargs)


def get_vp_result(expr: str, **kwargs) -> Any:
    """Execute the given python expression, while using
    the kwargs as the local variables.

    This will collect the result of the expression and return it.
    """
    from phml.utilities import (  # pylint: disable=import-outside-toplevel,unused-import
        ClassList,
        blank,
        classnames,
    )

    safe_vars = kwargs.pop("safe_vars", None) or False
    kwargs.update({"classnames": classnames, "blank": blank})

    avars = []
    result = "phml_vp_result"
    expression = f"phml_vp_result = {expr}\n"

    if len(expr.split("\n")) > 1:
        # Find all assigned vars in expression
        avars = []
        assignment = None
        for assign in ast.walk(ast.parse(expr)):
            if isinstance(assign, ast.Assign):
                assignment = parse_ast_assign(assign.targets)
                avars.extend(parse_ast_assign(assign.targets))

        result = assignment[-1]
        expression = f"{expr}\n"

    __validate_kwargs(kwargs, expr, safe_vars=safe_vars)

    try:
        source = compile(expression, expr, "exec")
        local_env = {}
        exec(source, {**kwargs, **globals()}, local_env)  # pylint: disable=exec-used
        return local_env[result] if result in local_env else None
    except Exception as exception:  # pylint: disable=broad-except
        from teddecor import TED  # pylint: disable=import-outside-toplevel

        TED.print(f"[@F red]*Error[]: {exception}")
        print(expr)

        return False


def escape_args(args: dict) -> dict:
    """Take a dictionary of args and escape the html inside string values.

    Args:
        args (dict): Collection of values to html escape.

    Returns:
        A html escaped collection of arguments.
    """

    for key in args:
        if isinstance(args[key], str):
            args[key] = escape(args[key], quote=False)


def extract_expressions(data: str) -> str:
    """Extract a phml python expr from a string.
    This method also handles multiline strings,
    strings with `\\n`

    Note:
        phml python blocks/expressions are indicated
        with curly brackets, {}.
    """
    results = []

    for expression in finditer(r"\{[^}]+\}", data):
        expression = expression.group().lstrip("{").rstrip("}")
        expression = [expr for expr in expression.split("\n") if expr.strip() != ""]
        results.append(expression[0])

    return results


def process_vp_blocks(pvb_value: str, virtual_python: VirtualPython, **kwargs) -> str:
    """Process a lines python blocks. Use the VirtualPython locals,
    and kwargs as local variables for each python block. Import
    VirtualPython imports in this methods scope.

    Args:
        value (str): The line to process.
        virtual_python (VirtualPython): Parsed locals and imports from all python blocks.
        **kwargs (Any): The extra data to pass to the exec function.

    Returns:
        str: The processed line as str.
    """

    # Bring vp imports into scope
    for imp in virtual_python.imports:
        exec(str(imp))  # pylint: disable=exec-used

    expressions = extract_expressions(pvb_value)
    kwargs.update(virtual_python.exposable)
    if expressions is not None:
        for expr in expressions:
            result = get_vp_result(expr, **kwargs)
            if isinstance(result, bool):
                pvb_value = result
            else:
                pvb_value = sub(r"\{[^}]+\}", str(result), pvb_value, 1)

    return pvb_value
