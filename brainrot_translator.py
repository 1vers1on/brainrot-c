import re
import argparse
import sys

keywords = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double',
    'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'inline', 'int', 'long',
    'register', 'restrict', 'return', 'short', 'signed', 'sizeof', 'static', 'struct',
    'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
}

token_specification = [
    ('PREPROCESSOR', r'#\s*include\s*<[^>]+>'),
    ('COMMENT',    r'//[^\n]*|/\*[\s\S]*?\*/'),
    ('KEYWORD',    r'\b(?:' + '|'.join(keywords) + r')\b'),
    ('NUMBER',     r'[+-]?(\d+(\.\d*)?|\.\d+)'),
    ('IDENTIFIER', r'\b[A-Za-z_][A-Za-z0-9_]*\b'),
    ('STRING',     r'"([^"\\]*(\\.[^"\\]*)*)"'),
    ('CHAR',       r"'([^'\\]*(\\.[^'\\]*)*)'"),
    ('OPERATOR',   r'\+\+|--|[+\-*/%=&|^<>!~]=?|[<>]=?|&&|\|\|'),
    ('PUNCTUATOR', r'[{}()\[\],.;:]'),
    ('WHITESPACE', r'\s+'),
    ('MISMATCH',   r'.'),
]

brainrot_keywords = {
    "if": "rizzing",
    "else": "sussy",
    "switch": "sigma",
    "case": "edge",
    "default": "drip",
    "break": "goon",
    "continue": "clap",
    "return": "mew",
    "goto": "yeet",

    "while": "ohio",
    "do": "diddy", 
    "for": "grimace",

    "enum": "aura",
    "typedef": "swag",

    "long": "chungus",
    "unsigned": "glizzy",
    "signed": "gyatt", 
    "short": "alpha",
    "int": "omega",
    "char": "blud",
    "double": "amongus",
    "float": "thug",

    "void": "fein",
    "volatile": "bussin",
    "const": "nocap",
    "register": "fortnite",
    "static": "cringe",
    "extern": "based",

    "union": "gang",
    "struct": "mafia",

    "sizeof": "hawktuah",
    "inline": "poggers",
    "auto": "sigma",
    "restrict": "yoinked"
}

brainrot_identifiers = {
    "printf": "yap",
    "malloc": "grind",
    "free": "dip",
    "calloc": "grindset", 
    "memcpy": "cap",
    "strlen": "measure",
    "strcpy": "cp",
    "strcat": "bro",
    "getchar": "snatch",
    "puts": "announce",

    "i": "rizz",
    "j": "swag",
    "k": "drip",
    "temp": "sus",
    "count": "sigma-count",
    "index": "gigachad"
}

token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

class CLexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
    
    def tokenize(self):
        for match in re.finditer(token_regex, self.code):
            kind = match.lastgroup
            value = match.group()
            if kind == 'WHITESPACE' or kind == 'COMMENT':
                continue
            elif kind == 'MISMATCH':
                print(f"Unrecognized character: {value}", file=sys.stderr)
                continue
            self.tokens.append((kind, value))
        return self.tokens

def reverse_tokens_to_code(tokens):
    code = []
    indent_level = 0
    prev_token = None
    in_typedef = False
    was_typedef = False
    in_parentheses = False
    
    tokens = [(kind, value) for kind, value in tokens if kind not in {'WHITESPACE', 'COMMENT'}]

    def need_space(prev, curr, next_tok):
        if not prev:
            return False
        prev_kind, prev_val = prev
        curr_kind, curr_val = curr
        if prev_kind == 'PUNCTUATOR' and prev_val in '{};':
            return False
        if curr_kind == 'PUNCTUATOR' and curr_val in ',;})':
            return False
        if prev_kind == 'PUNCTUATOR' and prev_val == '(':
            return False
        if curr_kind == 'OPERATOR' or prev_kind == 'OPERATOR':
            return True
        if prev_kind == 'KEYWORD' and prev_val == 'return' or prev_val == 'mew':
            return True
        if curr_kind in {'KEYWORD', 'IDENTIFIER'} and prev_kind in {'KEYWORD', 'IDENTIFIER', 'NUMBER'}:
            return True

        if next_tok:
            next_kind, next_val = next_tok
            if curr_kind == 'KEYWORD' and curr_val == 'int' or curr_val == 'omega' and next_kind == 'IDENTIFIER':
                return True
        return False

    i = 0
    while i < len(tokens):
        kind, value = tokens[i]
        next_token = tokens[i + 1] if i + 1 < len(tokens) else None
        if kind == 'WHITESPACE' or kind == 'COMMENT':
            i += 1
            continue
        if prev_token and prev_token[1] in {';', '{', '}'} and not (prev_token[1] == '}' and kind == 'PUNCTUATOR' and value == ';') and not in_parentheses and not was_typedef and next_token and next_token[1] != ';':
            code.append('\n' + '    ' * indent_level)
        elif was_typedef:
            code.append(' ')
        was_typedef = False
        
        if kind == 'PUNCTUATOR' and value == '(':
            in_parentheses = True
        if kind == 'PUNCTUATOR' and value == ')':
            in_parentheses = False
            
        if in_typedef and kind == 'PUNCTUATOR' and value == '}':
            was_typedef = True
            in_typedef = False

        if kind == 'KEYWORD' and (value == 'typedef' or value == 'swag'):
            in_typedef = True

        if kind == 'PUNCTUATOR':
            if value == '{':
                if not code[-1].endswith(' '):
                    code.append(' ')
                code.append(value)
                indent_level += 1
                code.append('\n' + '    ' * indent_level)
                prev_token = (kind, value)
                i += 1
                continue
            elif value == '}':
                indent_level = max(0, indent_level - 1)
                if not code[-1].endswith('\n'):
                    code.append('\n')
                code.append('    ' * indent_level + value)
                prev_token = (kind, value)
                i += 1
                continue
            elif value == ':':
                code.append(value + '\n' + '    ' * indent_level)
                prev_token = (kind, value)
                i += 1
                continue

        curr_token = (kind, value)
        if need_space(prev_token, curr_token, next_token):
            code.append(' ')

        if kind == 'PREPROCESSOR':
            code.append(value + '\n')
        else:
            code.append(value)

        prev_token = curr_token
        i += 1

    return re.sub(r'\n\s*\n', '\n', ''.join(code).strip())

def transform_tokens(tokens):
    transformed_tokens = []
    for kind, value in tokens:
        if kind == "KEYWORD" and value in brainrot_keywords:
            value = brainrot_keywords[value]
        elif kind == "IDENTIFIER" and value in brainrot_identifiers:
            value = brainrot_identifiers[value]
        
        transformed_tokens.append((kind, value))
            
    return transformed_tokens

def reverse_transform(tokens):
    transformed_tokens = []
    for kind, value in tokens:
        if kind == "KEYWORD" and value in brainrot_keywords.values():
            value = list(brainrot_keywords.keys())[list(brainrot_keywords.values()).index(value)]
        elif kind == "IDENTIFIER" and value in brainrot_identifiers.values():
            value = list(brainrot_identifiers.keys())[list(brainrot_identifiers.values()).index(value)]
        
        transformed_tokens.append((kind, value))
    
    return transformed_tokens

def main():
    parser = argparse.ArgumentParser(description='Transform C code to Brainrot and back.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--transform', action='store_true', help='Transform C code to Brainrot.')
    group.add_argument('--reverse', action='store_true', help='Reverse Brainrot code back to C.')

    parser.add_argument('input_file', help='Input file containing the code.')
    parser.add_argument('-o', '--output', help='Output file to write the transformed code.')
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        code = f.read()

    lexer = CLexer(code)
    tokens = lexer.tokenize()

    if args.transform:
        transformed_tokens = transform_tokens(tokens)
        transformed_code = reverse_tokens_to_code(transformed_tokens)
    elif args.reverse:
        reversed_tokens = reverse_transform(tokens)
        transformed_code = reverse_tokens_to_code(reversed_tokens)
    else:
        parser.error("Must specify either --transform or --reverse.")

    if args.output:
        with open(args.output, 'w') as f:
            f.write(transformed_code)
    else:
        print(transformed_code)

if __name__ == '__main__':
    main()
