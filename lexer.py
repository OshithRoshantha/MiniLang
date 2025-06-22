#Author: PS/2020/007

import re
import sys

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []
        self.line_num = 1
        self.token_specification = [
            ('SKIP',       r'\s+|//.*'),         
            ('INTEGER',    r'\d+'),              
            ('ASSIGN',     r'='),               
            ('EQ',         r'=='),               
            ('NE',         r'!='),              
            ('LE',         r'<='),               
            ('GE',         r'>='),               
            ('LT',         r'<'),                
            ('GT',         r'>'),                
            ('PLUS',       r'\+'),                
            ('MINUS',      r'-'),                
            ('TIMES',      r'\*'),              
            ('DIVIDE',     r'/'),                 
            ('SEMI',       r';'),                
            ('LPAREN',     r'\('),               
            ('RPAREN',     r'\)'),                
            ('LBRACE',     r'\{'),                
            ('RBRACE',     r'\}'),                
            ('INT',        r'int\b'),            
            ('IF',         r'if\b'),              
            ('ELSE',       r'else\b'), 
            ('STRING',     r'"[^"\n]*"'),           
            ('WHILE',      r'while\b'),           
            ('PRINT',      r'print\b'),           
            ('ID',         r'[a-zA-Z_]\w*'),     
            ('ERROR',      r'.'),               
        ]
        
        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        self.pattern = re.compile(self.token_regex)

    def tokenize(self):
        pos = 0
        while pos < len(self.source):
            match = self.pattern.match(self.source, pos)
            if match:
                kind = match.lastgroup
                value = match.group()
                pos = match.end()

                if kind == 'SKIP':
                    self.line_num += value.count('\n')
                    continue
                elif kind == 'ERROR':
                    raise SyntaxError(f"Invalid character '{value}' at line {self.line_num}")

                self.tokens.append((kind, value, self.line_num))
                self.line_num += value.count('\n')
            else:
                raise SyntaxError(f"Lexer error at position {pos} (line {self.line_num})")

        self.tokens.append(('EOF', '', self.line_num))
        return self.tokens

    def print_tokens(self):
        print(f"{'TOKEN':<10} {'VALUE':<15} {'LINE':<5}")
        print("-" * 30)
        for token in self.tokens:
            kind, value, line = token
            print(f"{kind:<10} {repr(value):<15} {line:<5}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lexer.py <source_file.mini>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        source_code = f.read()
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    lexer.print_tokens()