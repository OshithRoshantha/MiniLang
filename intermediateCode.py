from lexer import Lexer
from parser import Parser
from semanticAnalyzer import SemanticAnalyzer
import sys

class IntermediateCodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def generate(self):
        ast = self.ast
        self.visit(ast)
        return self.code

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def visit(self, node):
        method_name = 'visit_' + node['type']
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def visit_string(self, node):
        return f'"{node["value"]}"'

    def generic_visit(self, node):
        raise Exception(f'No visit_{node["type"]} method')

    def visit_program(self, node):
        for statement in node['body']:
            self.visit(statement)

    def visit_declaration(self, node):
        pass

    def visit_assignment(self, node):
        expr_result = self.visit(node['expr'])
        self.code.append(f"{node['var_name']} = {expr_result}")

    def visit_if(self, node):
        condition = self.visit(node['condition'])
        false_label = self.new_label()
        end_label = self.new_label()
        
        self.code.append(f"if not {condition} goto {false_label}")
        for statement in node['true_block']:
            self.visit(statement)
        self.code.append(f"goto {end_label}")
        self.code.append(f"{false_label}:")
        for statement in node['false_block']:
            self.visit(statement)
        self.code.append(f"{end_label}:")

    def visit_while(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.code.append(f"{start_label}:")
        condition = self.visit(node['condition'])
        self.code.append(f"if not {condition} goto {end_label}")
        for statement in node['body']:
            self.visit(statement)
        self.code.append(f"goto {start_label}")
        self.code.append(f"{end_label}:")

    def visit_print(self, node):
        expr_result = self.visit(node['expr'])
        self.code.append(f"print {expr_result}")

    def visit_binop(self, node):
        left = self.visit(node['left'])
        right = self.visit(node['right'])
        temp = self.new_temp()
        self.code.append(f"{temp} = {left} {node['op']} {right}")
        return temp

    def visit_comparison(self, node):
        left = self.visit(node['left'])
        right = self.visit(node['right'])
        temp = self.new_temp()
        self.code.append(f"{temp} = {left} {node['op']} {right}")
        return temp

    def visit_integer(self, node):
        return str(node['value'])

    def visit_variable(self, node):
        return node['name']

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python intermediateCode.py <source_file.mini>")
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
        sys.exit(1)
    generator = IntermediateCodeGenerator(ast)
    intermediate_code = generator.generate()
    print("Generated Intermediate Code:")
    for instruction in intermediate_code:
        print(instruction)
