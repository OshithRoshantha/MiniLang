from lexer import Lexer
from parser import Parser
from sematicAnalyzer import SemanticAnalyzer

class IntermediateCodeGenerator:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.code = []
        self.temp_count = 0

    def generate(self):
        ast, errors = self.analyzer.analyze()
        if errors:
            return None, errors
        self.visit(ast)
        return self.code, []

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

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
        pass  

    def visit_assignment(self, node):
        expr_result = self.visit(node['expr'])
        self.code.append(f"{node['var_name']} = {expr_result}")

    def visit_if(self, node):
        condition = self.visit(node['condition'])
        label_else = f"L{self.temp_count}"
        label_end = f"L{self.temp_count + 1}"
        self.temp_count += 2
        
        self.code.append(f"if not {condition} goto {label_else}")
        for statement in node['true_block']:
            self.visit(statement)
        self.code.append(f"goto {label_end}")
        self.code.append(f"{label_else}:")
        for statement in node['false_block']:
            self.visit(statement)
        self.code.append(f"{label_end}:")

    def visit_while(self, node):
        label_start = f"L{self.temp_count}"
        label_end = f"L{self.temp_count + 1}"
        self.temp_count += 2
        
        self.code.append(f"{label_start}:")
        condition = self.visit(node['condition'])
        self.code.append(f"if not {condition} goto {label_end}")
        for statement in node['body']:
            self.visit(statement)
        self.code.append(f"goto {label_start}")
        self.code.append(f"{label_end}:")

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
    source = """
    int x;
    x = 5;
    int y;
    y = 10;
    if (x > y) {
        print(x);
    } else {
        print(y);
    }
    while (x < y) {
        x = x + 1;
    }
    """
    lexer = Lexer(source)
    parser = Parser(lexer)
    analyzer = SemanticAnalyzer(parser)
    generator = IntermediateCodeGenerator(analyzer)
    code, errors = generator.generate()
    
    print("Intermediate Code:")
    for line in code:
        print(line)
    print("\nErrors:")
    for error in errors:
        print(error)