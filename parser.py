from lexer import Lexer

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokenize()
        self.current_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = ('EOF', '', self.current_token[2] if self.current_token else 0)
        return self.current_token

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token[0]} at line {self.current_token[2]}")

    def parse(self):
        return self.program()

    def program(self):
        statements = []
        while self.current_token[0] != 'EOF':
            statements.append(self.statement())
        return {'type': 'program', 'body': statements}

    def statement(self):
        if self.current_token[0] == 'INT':
            return self.declaration()
        elif self.current_token[0] == 'ID':
            return self.assignment()
        elif self.current_token[0] == 'IF':
            return self.if_statement()
        elif self.current_token[0] == 'WHILE':
            return self.while_statement()
        elif self.current_token[0] == 'PRINT':
            return self.print_statement()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token[0]} at line {self.current_token[2]}")

    def declaration(self):
        self.eat('INT')
        var_name = self.current_token[1]
        self.eat('ID')
        self.eat('SEMI')
        return {'type': 'declaration', 'var_name': var_name}

    def assignment(self):
        var_name = self.current_token[1]
        self.eat('ID')
        self.eat('ASSIGN')
        expr = self.expression()
        self.eat('SEMI')
        return {'type': 'assignment', 'var_name': var_name, 'expr': expr}

    def if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.expression()
        self.eat('RPAREN')
        self.eat('LBRACE')
        true_block = []
        while self.current_token[0] != 'RBRACE':
            true_block.append(self.statement())
        self.eat('RBRACE')
        
        false_block = []
        if self.current_token[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            while self.current_token[0] != 'RBRACE':
                false_block.append(self.statement())
            self.eat('RBRACE')
            
        return {'type': 'if', 'condition': condition, 'true_block': true_block, 'false_block': false_block}

    def while_statement(self):
        self.eat('WHILE')
        self.eat('LPAREN')
        condition = self.expression()
        self.eat('RPAREN')
        self.eat('LBRACE')
        body = []
        while self.current_token[0] != 'RBRACE':
            body.append(self.statement())
        self.eat('RBRACE')
        return {'type': 'while', 'condition': condition, 'body': body}

    def print_statement(self):
        self.eat('PRINT')
        self.eat('LPAREN')
        expr = self.expression()
        self.eat('RPAREN')
        self.eat('SEMI')
        return {'type': 'print', 'expr': expr}

    def expression(self):
        node = self.term()
        while self.current_token[0] in ('PLUS', 'MINUS'):
            token = self.current_token
            if token[0] == 'PLUS':
                self.eat('PLUS')
                node = {'type': 'binop', 'op': '+', 'left': node, 'right': self.term()}
            elif token[0] == 'MINUS':
                self.eat('MINUS')
                node = {'type': 'binop', 'op': '-', 'left': node, 'right': self.term()}
        return node

    def term(self):
        node = self.factor()
        while self.current_token[0] in ('TIMES', 'DIVIDE'):
            token = self.current_token
            if token[0] == 'TIMES':
                self.eat('TIMES')
                node = {'type': 'binop', 'op': '*', 'left': node, 'right': self.factor()}
            elif token[0] == 'DIVIDE':
                self.eat('DIVIDE')
                node = {'type': 'binop', 'op': '/', 'left': node, 'right': self.factor()}
        return node

    def factor(self):
        token = self.current_token
        if token[0] == 'INTEGER':
            self.eat('INTEGER')
            return {'type': 'integer', 'value': int(token[1])}
        elif token[0] == 'ID':
            self.eat('ID')
            return {'type': 'variable', 'name': token[1]}
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            node = self.expression()
            self.eat('RPAREN')
            return node
        elif token[0] in ('EQ', 'NE', 'LE', 'GE', 'LT', 'GT'):
            self.eat(token[0])
            left = self.expression()
            right = self.expression()
            return {'type': 'comparison', 'op': token[0], 'left': left, 'right': right}
        else:
            raise SyntaxError(f"Unexpected token {token[0]} at line {token[2]}")

if __name__ == "__main__":
    source = """
    int x;
    x = 5;
    if (x > 0) {
        print(x);
    } else {
        print(0);
    }
    """
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    import json
    print(json.dumps(ast, indent=2))