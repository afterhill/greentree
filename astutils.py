import ast

def run(*nodes):
    mod = ast.Module(body=list(nodes), lineno=1, col_offset=0)
    mod = ast.fix_missing_locations(mod)
    exec(compile(mod, "<ast>", "exec"))
