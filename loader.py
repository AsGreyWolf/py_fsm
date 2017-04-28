import re

digr = re.compile('digraph (\w+)_gr\W*{([^}]*)}')
it = re.compile('(\S+)->(\S+)\[label=\"([^\"]+)\"\]')

def fill_chars(chars):
	prev = '_'
	for i, char in enumerate(chars):
		if char == '..':
			start = ord(chars[i - 1]) + 1
			end = ord(chars[i + 1])
			for pos in range(start, end):
				yield chr(pos)
		else:
			yield char

def load_mapping(data):
	mapping = {}
	for name, content in digr.findall(data):
		mapping[name] = {}
		for parent, child, char_list in it.findall(content):
			if parent not in mapping[name]:
				mapping[name][parent] = {}
			mapping[name][parent][char_list] = child
	# print('Loaded mapping ' + str(mapping))
	return mapping

import final

def state_name_to_state(state_name, mach, states):
	if state_name == 'S':
		return mach.S
	elif state_name == 'E':
		return mach.E
	elif state_name == 'F':
		return mach.F
	else:
		return states[state_name]

def generate(mapping):
	result = {}
	state_names = set(state for graph_name, graph in mapping.items() for state in graph)
	state_names |= set(dir for graph_name, graph in mapping.items() for state, value in graph.items() for char, dir in value.items())
	states = {state_name: final.State(state_name) for state_name in state_names}

	for graph_name, graph in mapping.items():
		mach = final.Machine(graph_name)
		for parent, value in graph.items():
			parent = state_name_to_state(parent, mach, states)
			for char_list, child in value.items():
				child = state_name_to_state(child, mach, states)
				for char in fill_chars(char_list.split('|')):
					trans = final.Transition(char, child)
					mach.append(parent, trans)
		result[graph_name] = mach
	return result

def load_dot(data):
	mapping = load_mapping(data)
	return generate(mapping)
