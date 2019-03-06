import enum
from Token import Token


class LexerException(BaseException):

    def __init__(self, letter: str):
        self.letter = letter

    def __str__(self):
        return "unexpected letter: {}".format(self.letter)


class State(enum.Enum):
    START = 0
    STRING = 1
    FALSE = 2
    TRUE = 3
    NULL = 4
    NUMBER = 5


class NumberState(enum.Enum):
    BEFORE_DOT = 0
    AFTER_DOT = 1
    AFTER_E = 2


class NumberParser:

    class State(enum.Enum):
        BEFORE_DEC_POINT = 0
        AFTER_DEC_POINT = 1
        AFTER_E = 2

    def __init__(self, sign):
        self.sign = sign
        self.pre_dot = 0
        self.after_dec_point = 0
        self.distance_after_dec_point = 0
        self.scale = 0
        self.state = NumberParser.State.BEFORE_DEC_POINT

    def to_number(self) -> float:
        return self.sign * (self.pre_dot + self.after_dec_point) * (10 ** self.scale)

    def take_number(self, number: int):

        if self.state == NumberParser.State.BEFORE_DEC_POINT:
            self._add_before_dec_point(number)
        elif self.state == NumberParser.State.AFTER_DEC_POINT:
            self._add_after_dec_point(number)
        elif self.state == NumberParser.State.AFTER_E:
            self._add_scale(number)

    def go_after_dec_point(self):
        self.state = NumberParser.State.AFTER_DEC_POINT
        self.distance_after_dec_point = 1

    def go_after_e(self):
        self.state = NumberParser.State.AFTER_E

    def _add_after_dec_point(self, value: int):
        self.after_dec_point += value * \
            (1 / (10 ** self.distance_after_dec_point))
        self.distance_after_dec_point += 1

    def _add_before_dec_point(self, value: int):
        self.pre_dot *= 10
        self.pre_dot += value

    def _add_scale(self, value: int):
        self.scale *= 10
        self.scale += value


class PrimitiveParser:
    
    def __init__(self, index: int, primtive: str):
        self.index = index
        self.primitive = primtive
        self.completed = False
        
    def take_letter(self, letter: str):
        
        # if not at last letter
        if self.index < len(self.primitive) - 1:
            if self.primitive[self.index] == letter:
                self.index += 1
            else:
                raise LexerException(letter)
        # if at last letter
        else:
            if self.primitive[self.index] == letter:
                self.completed = True
            else:
                raise LexerException(letter)


class Lexer:

    def __init__(self, text: str):
        # current letter and iterator
        self.current_iter = iter(text)
        self.current_letter = next(self.current_iter)
        # used for recording token
        self.token: Token = None
        self.buffer = ""
        # state information
        self.state = State.START
        self.state_data = None
        self.should_continue = True
        # end of file
        self.is_finished = False

    def extract_token(self):
        self.should_continue = True

        while self.should_continue and not self.is_finished:
            self._handle_state()

    def _handle_state(self):

        if self.state == State.START:
            self._start_state()
        elif self.state == State.STRING:
            self._string_state()
        elif self.state == State.TRUE:
            self._true_state()
        elif self.state == State.FALSE:
            self._false_state()
        elif self.state == State.NULL:
            self._null_state()
        elif self.state == State.NUMBER:
            self._number_state()

    def _start_state(self):

        # {
        if self.current_letter == "{":
            self.token = Token("begin object")
            self.should_continue = False
        # }
        elif self.current_letter == "}":
            self.token = Token("end object")
            self.should_continue = False
        # string
        elif self.current_letter == "'" or self.current_letter == "\"":
            self.state = State.STRING
            self.state_data = self.current_letter
        # ,
        elif self.current_letter == ",":
            self.token = Token("value separator")
            self.should_continue = False
        # :
        elif self.current_letter == ":":
            self.token = Token("key value separator")
            self.should_continue = False
        # If matching false
        elif self.current_letter == "f":
            self.state = State.FALSE
            # self.state_data = "false", 1
            self.state_data = PrimitiveParser(1, "false")
        # if matching true
        elif self.current_letter == "t":
            self.state = State.TRUE
            # self.state_data = "true", 1
            self.state_data = PrimitiveParser(1, "true")
        # if matching null
        elif self.current_letter == "n":
            self.state = State.NULL
            # self.state_data = "null", 1
            self.state_data = PrimitiveParser(1, "null")
        elif self.current_letter == " " \
                or self.current_letter == "\t" \
                or self.current_letter == "\n":
            pass
        # negative numbers
        elif self.current_letter == "-":
            self.state = State.NUMBER
            self.state_data = NumberParser(-1)
        # number
        elif self.current_letter.isnumeric():
            self.state = State.NUMBER
            self.state_data = NumberParser(1)
        # unexpected characters
        else:
            raise LexerException(self.current_letter)

        self._iterate()

    def _string_state(self):

        if self.current_letter == self.state_data:
            self.token = Token("string", self.buffer)
            self.should_continue = False
            self.state = State.START
            self.buffer = ""
        else:
            self.buffer += self.current_letter

        # self.current_letter = next(self.current_iter)
        self._iterate()

    def _true_state(self):
        
        self.state_data.take_letter(self.current_letter)
        
        if self.state_data.completed:
            self.state = State.START
            self.should_continue = False
            self.token = Token("boolean", "true")

        self._iterate()

    def _false_state(self):

        self.state_data.take_letter(self.current_letter)
        
        if self.state_data.completed:
            self.state = State.START
            self.should_continue = False
            self.token = Token("boolean", "false")

        self._iterate()

    def _null_state(self):

        self.state_data.take_letter(self.current_letter)
        
        if self.state_data.completed:
            self.state = State.START
            self.should_continue = False
            self.token = Token("null")

        self._iterate()

    def _number_state(self):

        # print("number state, letter = {}".format(self.current_letter))

        # End number
        if self.current_letter == "," \
                or self.current_letter == "}" \
                or self.current_letter == "]" \
                or self.current_letter == " ":
            self.token = Token("number", self.state_data.to_number())
            self.state = State.START
            self.should_continue = False
        # - after e
        elif self.current_letter == "-":
            pass
        # + after e
        elif self.current_letter == "+":
            pass
        # . dot
        elif self.current_letter == ".":
            # self.state_data.state = NumberState.AFTER_DOT
            # self.state_data.distance_after_dot = 1
            self.state_data.go_after_dec_point()
        # e
        elif self.current_letter == "e" or self.current_letter == "E":
            self.state_data.go_after_e()
        # other numbers
        elif self.current_letter.isnumeric():
            self.state_data.take_number(int(self.current_letter))
        # unexpected letter
        else:
            raise LexerException(self.current_letter)

        self._iterate()

    def _iterate(self):
        try:
            self.current_letter = next(self.current_iter)
        except StopIteration as e:
            self.is_finished = True

    def _finish_matching_state_data(self) -> bool:
        literal, index = self.state_data

        # if not at last letter
        if index < len(literal) - 1:
            if self.current_letter != literal[index]:
                raise LexerException(self.current_letter)
        # at last letter
        else:
            if self.current_letter == literal[index]:
                return True
            else:
                raise LexerException(self.current_letter)

        return False
