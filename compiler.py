import sys
from lexer import Lexer
from parser import Parser
from sematicAnalyzer import SemanticAnalyzer
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
    parser = Parser(lexer)
    analyzer = SemanticAnalyzer(parser)
    generator = IntermediateCodeGenerator(analyzer)

    tokens = lexer.scan_tokens()
    ast = parser.parse()
    analyzed_ast, semantic_errors = analyzer.analyze()
    
    if semantic_errors:
        print("\nSemantic Errors:")
        for error in semantic_errors:
            print(error)
        return

    intermediate_code, code_errors = generator.generate()
    
    print("\nTokens:")
    for token in tokens:
        print(token)
    
    print("\nAbstract Syntax Tree:")
    import json
    print(json.dumps(ast, indent=2))
    
    print("\nIntermediate Code:")
    for instruction in intermediate_code:
        print(instruction)

if __name__ == "__main__":
    main()