import inspect
from sys import stdout

def _should_dump_repr(obj):
	return inspect.ismethod(obj) or inspect.isfunction(obj) or inspect.isgenerator(obj) or inspect.istraceback(obj)

def dump(obj, indent=0, visited=set()):
	if id(obj) in visited:
		stdout.write('\x1b[31mRecursion on %s with id=%i\x1b[0m' % (type(obj).__name__, id(obj)))
	elif obj is None:
		stdout.write('\x1b[3mNone\x1b[0m')
	elif isinstance(obj, str):
		stdout.write('\x1b[32m%s\x1b[0m' % repr(obj))
	elif isinstance(obj, bytes):
		stdout.write('b\x1b[32m%s\x1b[0m' % repr(obj)[1:])
	elif isinstance(obj, bool):
		stdout.write('\x1b[35m%s\x1b[0m' % obj)
	elif isinstance(obj, int) or isinstance(obj, float):
		stdout.write('\x1b[34m%s\x1b[0m' % obj)
	elif _should_dump_repr(obj):
		stdout.write('\x1b[36m%s\x1b[0m' % repr(obj))
	elif isinstance(obj, dict):
		if not obj:
			stdout.write('{}')
		else:
			stdout.write('{\n')
			for key, value in obj.items():
				stdout.write(' ' * 2 * (indent + 1))
				dump(key, indent + 1, visited | {id(obj)})
				stdout.write(': ')
				dump(value, indent + 1, visited | {id(obj)})
				stdout.write(',\n')

			stdout.write('%s}' % (' ' * 2 * indent))

	elif isinstance(obj, set):
		if not obj:
			stdout.write('set()')
		else:
			stdout.write('{\n')
			for value in obj:
				stdout.write(' ' * 2 * (indent + 1))
				dump(value, indent + 1, visited | {id(obj)})
				stdout.write(',\n')

			stdout.write('%s}' % (' ' * 2 * indent))

	elif isinstance(obj, list):
		if not obj:
			stdout.write('[]')
		else:
			stdout.write('[\n')
			for value in obj:
				stdout.write(' ' * 2 * (indent + 1))
				dump(value, indent + 1, visited | {id(obj)})
				stdout.write(',\n')

			stdout.write('%s]' % (' ' * 2 * indent))
	elif isinstance(obj, tuple):
		if not obj:
			stdout.write('tuple()')
		else:
			stdout.write('(\n')
			for value in obj:
				stdout.write(' ' * 2 * (indent + 1))
				dump(value, indent + 1, visited | {id(obj)})
				stdout.write(',\n')

			stdout.write('%s)' % (' ' * 2 * indent))
	else:
		stdout.write(str(type(obj)))
		attrs = {}

		for name in dir(obj):
			if name[:2] == name[-2:] == '__' and len(name) > 4:
				continue

			value = getattr(obj, name)
			if inspect.ismethod(value):
				continue

			attrs[name] = value

		if attrs:
			stdout.write(' {\n')
			for key, value in attrs.items():
				stdout.write('%s\x1b[4m%s\x1b[0m: ' % (' ' * 2 * (indent + 1), key))
				dump(value, indent + 1, visited | {id(obj)})
				stdout.write(',\n')

			stdout.write('%s}' % (' ' * 2 * indent))

	if indent == 0:
		stdout.write('\n')
