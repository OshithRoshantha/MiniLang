from lexer import Lexer
from parser import Parser
import sys

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = set()
        self.errors = []

    def analyze(self):
        self.visit(self.ast) 
        return self.ast, self.errors

    def add_error(self, message, line):
        self.errors.append({"message": message, "line": line})

    def visit(self, node):
        method_name = 'visit_' + node['type']
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{node["type"]} method')

    def visit_program(self, node):
        for statement in node['body']:
            self.visit(statement)

    def visit_declaration(self, node):
        var_name = node['var_name']
        if var_name in self.symbol_table:
            self.add_error(f"Variable '{var_name}' already declared", node.get('line', 0))
        else:
            self.symbol_table.add(var_name)

    def visit_assignment(self, node):
        var_name = node['var_name']
        if var_name not in self.symbol_table:
            self.add_error(f"Variable '{var_name}' not declared", node.get('line', 0))
        self.visit(node['expr'])

    def visit_if(self, node):
        self.visit(node['condition'])
        for statement in node['true_block']:
            self.visit(statement)
        for statement in node['false_block']:
            self.visit(statement)

    def visit_while(self, node):
        self.visit(node['condition'])
        for statement in node['body']:
            self.visit(statement)

    def visit_print(self, node):
        self.visit(node['expr'])
        
    def visit_string(self, node):
        pass
    
    def visit_binop(self, node):
        self.visit(node['left'])
        self.visit(node['right'])

    def visit_comparison(self, node):
        self.visit(node['left'])
        self.visit(node['right'])

    def visit_integer(self, node):
        pass

    def visit_variable(self, node):
        if node['name'] not in self.symbol_table:
            self.add_error(f"Variable '{node['name']}' not declared", node.get('line', 0))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python semanticAnalyzer.py <source_file.mini>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        source_code = f.read()
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    ast = parser.parse()           
    analyzer = SemanticAnalyzer(ast) 
    ast, errors = analyzer.analyze()
    if errors:
        print("Semantic Errors:")
        for error in errors:
            print(f"Line {error['line']}: {error['message']}")