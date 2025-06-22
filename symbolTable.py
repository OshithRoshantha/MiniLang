#Author: PS/2020/007

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare(self, name, symbol_type):
        if name in self.scopes[-1]:
            return False  
        self.scopes[-1][name] = {'type': symbol_type}
        return True

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def update(self, name, attributes):
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name].update(attributes)
                return True
        return False