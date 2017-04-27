from enum import Enum
from collections import defaultdict
from itertools import tee

class Peeker:
	def __init__(self, it):
		self.it = iter(it)
		self.__step()
		self.__pos = 0
	def __step(self):
		try:
			self.data = next(self.it)
		except StopIteration as e:
			self.data = e
	def __next__(self):
		if isinstance(self.data, StopIteration):
			raise self.data
		prev = self.data
		self.__step()
		self.__pos = self.__pos + 1
		return prev
	def __iter__(self):
		return self
	def peek(self):
		if isinstance(self.data, StopIteration):
			raise self.data
		return self.data
	@property
	def pos(self):
		return self.__pos

class SyntaxError(Exception):
	def __init__(self, pos, expected):
		self.pos = pos
		self.expected = set(expected)
	def __str__(self):
		return 'Syntax error at position %s: expected: %s' % (self.pos, self.expected)

class UnsupportedLineError(Exception):
	pass

class State:
	def __init__(self, name, on_enter=None, on_leave=None):
		self.name = name
		self.on_enter = on_enter
		self.on_leave = on_leave
	def __str__(self):
		return '<State %s>' % self.name
	def __repr__(self):
		return 'State(%r, %r, %r)' % (self.name, self.on_enter, self.on_leave)

class Transition:
	EOS = '⊥'
	def __init__(self, key, next_state):
		self.key = key
		self.next_state = next_state
	def __call__(self, state, peeker):
		if state.on_leave is not None:
			state.on_leave(peeker)
		if self.key != self.EOS and len(self.key) == 1:
			char = next(peeker)
		state = self.next_state
		if state.on_enter is not None:
			state.on_enter(peeker)
		return state
	def __str__(self):
		return '<Transition %s -> %s>' % (self.key, self.next_state)
	def __repr__(self):
		return 'Transition(%r, %r)' % (self.key, self.next_state)


class Machine:
	def __init__(self, name, on_enter=None, on_leave=None, mapping=None):
		self.name = name
		self.S = State('S')
		self.F = State('F')
		self.E = State('E')
		self.on_enter = on_enter
		self.on_leave = on_leave
		self.mapping = mapping if mapping is not None else {}
		self.submachines = {}
		self.state = self.S

	@property
	def on_enter(self):
		return self.S.on_enter
	@on_enter.setter
	def on_enter(self, value):
		self.S.on_enter = value
	@property
	def on_leave(self):
		return self.F.on_enter
	@on_leave.setter
	def on_leave(self, value):
		self.F.on_enter = value

	def append(self, state, trans):
		if state not in self.mapping:
			self.mapping[state] = {}
		self.mapping[state][trans.key] = trans

	def step_char(self, peeker):
		key = peeker.peek()
		if key in self.mapping[self.state]:
			trans = self.mapping[self.state][key]
			return trans(self.state, peeker)
		return None
	def step_submachine(self, peeker):
		for key, trans in self.mapping[self.state].items():
			if len(key) == 1 or key not in self.submachines:
				continue
			try:
				self.submachines[key](peeker)
			except UnsupportedLineError:
				pass
			else:
				return trans(self.state, peeker)
		return None
	def step_EOS(self, peeker):
		if Transition.EOS in self.mapping[self.state]:
			trans = self.mapping[self.state][Transition.EOS]
			return trans(self.state, peeker)
		return None
	def step_E(self, peeker):
		trans = Transition(Transition.EOS, self.E)
		return trans(self.state, peeker)
	def step_S(self, peeker):
		trans = Transition(Transition.EOS, self.S)
		return trans(self.state, peeker)

	def __call__(self, peeker):
		self.state = self.step_S(peeker)
		try:
			while self.state not in [self.F, self.E]:
				next_state = self.step_char(peeker)
				if next_state is None:
					next_state = self.step_submachine(peeker)
				if next_state is None:
					next_state = self.step_EOS(peeker)
				if next_state is None:
					next_state = self.step_E(peeker)
				if next_state == self.E:
					prev_state, self.state = self.state, next_state
					if prev_state == self.S:
						raise UnsupportedLineError()
					raise SyntaxError(peeker.pos, self.mapping[prev_state].keys())
				# print('%s: %s -> %s' % (self.name, self.state, next_state))
				self.state = next_state
		except StopIteration:
			raise SyntaxError(peeker.pos, self.mapping[self.state].keys())
		return self.state
	def __str__(self):
		return '<Machine %s>' % self.name
	def __repr__(self):
		return 'Machine(%r, %r, %r, %r, {...%s elements...})' % (self.name, self.on_enter, self.on_leave, len(self.mapping))
