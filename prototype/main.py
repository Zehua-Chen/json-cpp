from lexer import Lexer, Token, LexerException


# json = "{ 'a': true, 'b': false, 'c': null, 'd': -12.22e-2, 'e': 'as we can' }"
json = "{ 'abc': 'ee\\\\e' }"
lexer = Lexer(json)

print(json)

while not lexer.is_finished:
    lexer.extract_token()
    print(lexer.token)