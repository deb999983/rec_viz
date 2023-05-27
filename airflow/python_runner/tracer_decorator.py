import json
import sys
import traceback


def kwargs_string(**kwargs):
	return ','.join([f'{key}={str(value)}' for key, value in kwargs.items()])


class Call:
	_root = None
	fields = ['id', 'func', 'caller', 'called_with', 'return_value']

	def __init__(self, call_id, func, caller, called_with, ret=None):
		self.id = call_id
		self.func = func
		self.caller = caller
		self.called_with = called_with
		self.return_value = ret
		self.children = []

		if not caller:
			Call._root = self
		else:
			caller.children.append(self)

	def __str__(self):
		kwargs = kwargs_string(**self.called_with["kwargs"])
		return f'{self.func}({kwargs})'

	@classmethod
	def to_dict(cls, root):
		d = {}
		if not root:
			return d

		d = {field: str(getattr(root, field)) for field in cls.fields}
		children = []
		for child in root.children:
			children.append(cls.to_dict(child))
		d['children'] = children
		return d


def string_vals(**kwargs):
	return {key: str(value) for key, value in kwargs.items()}


class Tracer:
	def __init__(self, func_name: str) -> None:
		self.func_name = func_name
		self.call_stack = []
		self.call_tree = None
		self.call_id = 1
		self.error = None

	def trace_calls(self, frame, event, arg):
		if frame.f_code.co_name != self.func_name:
			return

		if event == 'call':
			call = Call(
				self.call_id, func=self.func_name,
				caller=self.call_stack[-1] if self.call_stack else None,
				called_with={"args":[], "kwargs": string_vals(**frame.f_locals)}
			)
			self.call_id = self.call_id + 1
			if not self.call_tree:
				self.call_tree = call
			self.call_stack.append(call)

		if event == "return" and self.call_stack:
			c: Call = self.call_stack.pop()
			c.return_value = arg

	@classmethod
	def get_instance(cls, func_name: str):
		return Tracer(func_name)

	def run(self, file_name):
		try:
			with open(file_name, 'rb') as f:
				code = compile(f.read(), file_name, 'exec')

				# Trace calls.
				sys.setprofile(self.trace_calls)
				exec(code, {})
				sys.setprofile(None)
		except Exception as e:
			self.error = traceback.format_exc()
			return e

	def save_output(self, file_name="output.json"):
		t = Call.to_dict(self.call_tree)
		# print(f"Output: ============ {t} ===========")
		with open(file_name, mode='w') as fp:
			json.dump(t, fp)

	def save_error(self, file_name="output.json"):
		with open(file_name, mode='w') as fp:
			json.dump(self.error, fp)


def trace_calls(*args):
	if frame.f_code.co_name != self.func_name:
		return

	if event == 'call':
		call = Call(
			self.call_id, func=self.func_name,
			caller=self.call_stack[-1] if self.call_stack else None,
			called_with={"args":[], "kwargs": string_vals(**frame.f_locals)}
		)
		self.call_id = self.call_id + 1
		if not self.call_tree:
			self.call_tree = call
		self.call_stack.append(call)

	if event == "return" and self.call_stack:
		c: Call = self.call_stack.pop()
		c.return_value = arg
