import sys
from lexer import Lexer
from parser import Parser
from semanticAnalyzer import SemanticAnalyzer
from intermediateCode import IntermediateCodeGenerator

def main():
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <filename.mini>")
        return

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            source = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return

    lexer = Lexer(source)
    try:
        tokens = lexer.tokenize()
    except SyntaxError as e:
        print(f"Lexical Error: {e}")
        return

    parser = Parser(lexer)
    try:
        ast = parser.parse()
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return

    analyzer = SemanticAnalyzer(parser)
    analyzed_ast, semantic_errors = analyzer.analyze()
    if semantic_errors:
        print("\nSemantic Errors:")
        for error in semantic_errors:
            print(f"Line {error['line']}: {error['message']}")
        return

    generator = IntermediateCodeGenerator(analyzer)
    intermediate_code, code_errors = generator.generate()
    if code_errors:
        print("\nCode Generation Errors:")
        for error in code_errors:
            print(error)
        return

    print("\n=== TOKENS ===")
    for token in tokens:
        print(f"{token[0]:<10} {repr(token[1]):<15} Line {token[2]}")

    print("\n=== ABSTRACT SYNTAX TREE ===")
    import json
    print(json.dumps(ast, indent=2))

    print("\n=== INTERMEDIATE CODE ===")
    for instruction in intermediate_code:
        print(instruction)

if __name__ == "__main__":
    main()