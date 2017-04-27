from loader import generate
from pathlib import Path
from final import Peeker
from final import SyntaxError
import fsmgui

mapping = {'repeat': {'S': {'REPEAT': '1'},
                      '1': {'разделитель': 'r1'},
                      'r1': {'оп_присв': '2'},
                      '2': {'UNTIL': '3'},
                      '3': {'разделитель': 'r3'},
                      'r3': {'условие': '4'},
                      '4': {';': 'F'}},
           'оп_присв': {'S': {'лев_ч': '1'},
                        '1': {'разделитель': 'r1', ':': '2'},
                        'r1': {':': '2'},
                        '2': {'=': '3'},
                        '3': {'разделитель': 'r3', 'прав_ч': 'F'},
                        'r3': {'прав_ч': 'F'}},
           'условие': {'S': {'отношение': 'F', '(': '1'},
                       '1': {'разделитель': 'r1', 'отношение': '2'},
                       'r1': {'отношение': '2'}, '2': {')': '3'},
                       '3': {'разделитель': 'r3', 'логич_оп': '4', '⊥': 'F'},
                       'r3': {'логич_оп': '4', '⊥': 'F'},
                       '4': {'разделитель': 'r4', '(': '5'},
                       'r4': {'(': '5'},
                       '5': {'разделитель': 'r5', 'отношение': '6'},
                       'r5': {'отношение': '6'},
                       '6': {')': '7'},
                       '7': {'разделитель': 'F', '⊥': 'F'}},
           'лев_ч': {'S': {'идентификатор': '1'},
                     '1': {'[': '2', '⊥': 'F'},
                     '2': {'разделитель': 'r2', 'константа': '3', 'идентификатор': '3'},
                     'r2': {'константа': '3', 'идентификатор': '3'},
                     '3': {'разделитель': 'r3', ']': 'F'},
                     'r3': {']': 'F'}},
           'прав_ч': {'S': {'операнд': '1'},
                      '1': {'разделитель': '3', '+': '4', '-': '4', '*': '4', '/': '4'},
                      '3': {'+': '4', '-': '4', '*': '4', '/': '4', 'DIV': '5', 'MOD': '5', '⊥': 'F'},
                      '4': {'разделитель': '2', 'операнд': '6'},
                      '5': {'разделитель': '2'},
                      '2': {'операнд': '6'},
                      '6': {'разделитель': 'F'}},
           'отношение': {'S': {'операнд': '1'},
                         '1': {'разделитель': 'r1', 'отношения_оп': '2', '⊥': 'F'},
                         'r1': {'отношения_оп': '2', '⊥': 'F'},
                         '2': {'разделитель': 'r2', 'операнд': '3'},
                         'r2': {'операнд': '3'},
                         '3': {'разделитель': 'F', '⊥': 'F'}},
           'идентификатор': {'S': {'буква': '1', '_': '1'},
                             '1': {'буква': '1', 'цифра': '1', '_': '1', '⊥': 'F'}},
           'константа': {'S': {'1': '1', '2': '1', '3': '1', '4': '1', '5': '1', '6': '1', '7': '1', '8': '1', '9': '1', '-': '2', '0': 'F'},
                         '2': {'1': '1', '2': '1', '3': '1', '4': '1', '5': '1', '6': '1', '7': '1', '8': '1', '9': '1'},
                         '1': {'цифра': '1', '⊥': 'F'}},
           'операнд': {'S': {'константа_любая': 'F', 'идентификатор': '1'},
                       '1': {'[': '2', '⊥': 'F'},
                       '2': {'разделитель': 'r2', 'константа': '3', 'идентификатор': '3'},
                       'r2': {'константа': '3', 'идентификатор': '3'},
                       '3': {'разделитель': 'r3', ']': 'F'},
                       'r3': {']': 'F'}},
           'константа_любая': {'S': {'1': '1', '2': '1', '3': '1', '4': '1', '5': '1', '6': '1', '7': '1', '8': '1', '9': '1', '-': '3', '0': '6'},
                               '3': {'1': '1', '2': '1', '3': '1', '4': '1', '5': '1', '6': '1', '7': '1', '8': '1', '9': '1', '0': '4'},
                               '1': {'цифра': '1', '⊥': 'F', '.': '2'},
                               '2': {'цифра': '5'},
                               '5': {'цифра': '5', '⊥': 'F'},
                               '6': {'⊥': 'F', '.': '2'},
                               '4': {'.': '2'}},
           'логич_оп': {'S': {'AND': 'F', 'OR': 'F', 'XOR': 'F'}},
           'отношения_оп': {'S': {'=': 'F', '<': '1', '>': '2'},
                            '1': {'=': 'F', '>': 'F', '⊥': 'F'},
                            '2': {'=': 'F', '⊥': 'F'}},
           'разделитель': {'S': {' ': '1'},
                           '1': {' ': '1', '⊥': 'F'}},
           'буква': {'S': {'a': 'F', 'b': 'F', 'c': 'F', 'd': 'F', 'e': 'F', 'f': 'F', 'g': 'F', 'h': 'F', 'i': 'F', 'j': 'F', 'k': 'F', 'l': 'F', 'm': 'F', 'n': 'F', 'o': 'F', 'p': 'F', 'q': 'F', 'r': 'F', 's': 'F', 't': 'F', 'u': 'F', 'v': 'F', 'w': 'F', 'x': 'F', 'y': 'F', 'z': 'F', 'A': 'F', 'B': 'F', 'C': 'F', 'D': 'F', 'E': 'F', 'F': 'F', 'G': 'F', 'H': 'F', 'I': 'F', 'J': 'F', 'K': 'F', 'L': 'F', 'M': 'F', 'N': 'F', 'O': 'F', 'P': 'F', 'Q': 'F', 'R': 'F', 'S': 'F', 'T': 'F', 'U': 'F', 'V': 'F', 'W': 'F', 'X': 'F', 'Y': 'F', 'Z': 'F'}},
           'цифра': {'S': {'0': 'F', '1': 'F', '2': 'F', '3': 'F', '4': 'F', '5': 'F', '6': 'F', '7': 'F', '8': 'F', '9': 'F'}},
           'REPEAT': {'S': {'R': '1'},
                      '1': {'E': '2'},
                      '2': {'P': '3'},
                      '3': {'E': '4'},
                      '4': {'A': '5'},
                      '5': {'T': 'F'}},
           'UNTIL': {'S': {'U': '1'},
                     '1': {'N': '2'},
                     '2': {'T': '3'},
                     '3': {'I': '4'},
                     '4': {'L': 'F'}},
           'DIV': {'S': {'D': '1'},
                   '1': {'I': '2'},
                   '2': {'V': 'F'}},
           'MOD': {'S': {'M': '1'},
                   '1': {'O': '2'},
                   '2': {'D': 'F'}},
           'AND': {'S': {'A': '1'},
                   '1': {'N': '2'},
                   '2': {'D': 'F'}},
           'OR': {'S': {'O': '1'},
                  '1': {'R': 'F'}},
           'XOR': {'S': {'X': '1'},
                   '1': {'O': '2'},
                   '2': {'R': 'F'}}}

machines = generate(mapping)
# print(machines)
for name, mach in machines.items():
	mach.submachines = machines

main = machines['repeat']

class SemanticError(Exception):
	def __init__(self, start, end, msg):
		self.start = start
		self.end = end
		self.msg = msg
	def __str__(self):
		return 'Semantic error at position %s-%s: %s' % (self.start, self.end, self.msg)

text = ''
idns = []
consts = []
consts_any = []

def process(_text):
	global text
	text = _text
	w.reset()
	state = None
	peeker = Peeker(text)
	idns.clear()
	consts.clear()
	consts_any.clear()
	try:
		state = main(peeker)
	except SyntaxError as ex:
		w.set_status(str(ex))
		w.set_error(ex.pos)
	except Exception as ex:
		w.set_status(repr(ex))
	else:
		if state == main.F and peeker.pos == len(text):
			try:
				semantics()
			except SemanticError as ex:
				w.set_status(str(ex))
				w.set_error(ex.start, ex.end)
			else:
				w.set_status('Success')
			semantics_str = 'Identifiers:\n'
			for idn in set(x for x, start, end in idns):
				semantics_str += idn
				semantics_str += '\n'
			semantics_str += 'Constants:\n'
			for const in set(x for x, start, end in consts):
				semantics_str += const
				semantics_str += '\n'
			semantics_str += 'Float constants:\n'
			for const in set(x for x, start, end in consts_any):
				semantics_str += const
				semantics_str += '\n'
			w.set_semantics(semantics_str)
		elif state == main.F:
			w.set_status(str(SyntaxError(peeker.pos, ['NOTHING'])))
			w.set_error(peeker.pos)
		else:
			w.set_status('SMTH STRANGE WTF?')

invalid_idns = {'REPEAT', 'UNTIL', 'DIV', 'MOD', 'XOR', 'AND', 'OR'}
def semantics():
	for idn, start, end in idns:
		if idn in invalid_idns:
			raise SemanticError(start, end, 'Invalid identifier: reserved word')
		if len(idn) > 8:
			raise SemanticError(start, end, 'Invalid identifier: too long')
	for const, start, end in consts:
		if len(const) > 6 or int(const) > 32767 or int(const) < -32768:
			raise SemanticError(start, end, 'Invalid constant: overflow')

idn_start_pos = -1
def idn_start(peeker):
	global idn_start_pos
	idn_start_pos = peeker.pos
def idn_end(peeker):
	idn = text[idn_start_pos:peeker.pos]
	idns.append((idn, idn_start_pos, peeker.pos))
machines['идентификатор'].on_enter = idn_start
machines['идентификатор'].on_leave = idn_end

const_start_pos = -1
def const_start(peeker):
	global const_start_pos
	const_start_pos = peeker.pos
def const_end(peeker):
	const = text[const_start_pos:peeker.pos]
	consts.append((const, const_start_pos, peeker.pos))
machines['константа'].on_enter = const_start
machines['константа'].on_leave = const_end

const_any_start_pos = -1
def const_any_start(peeker):
	global const_any_start_pos
	const_any_start_pos = peeker.pos
def const_any_end(peeker):
	const = text[const_any_start_pos:peeker.pos]
	consts_any.append((const, const_any_start_pos, peeker.pos))
machines['константа_любая'].on_enter = const_any_start
machines['константа_любая'].on_leave = const_any_end

w = fsmgui.Window(process)
w.mainloop()
