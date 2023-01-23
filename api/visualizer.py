from datetime import datetime

def kwargs_string(**kwargs):
	return ','.join([f'{key}={str(value)}' for key, value in kwargs.items()])


class Call:
	_root = None

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
	def display(cls, root):
		if not root:
			return {}

		display_dict = {}
		for child_call in root.children:
			h = str(root.id) + ":" + str(root)
			ch = str(child_call.id) + ":" + str(child_call)

			display_dict[h] = display_dict.get(h, [])
			display_dict[str(h)].append(ch)

			display_dict.update(cls.display(child_call))

		return display_dict


class Visualize:

	def __init__(self, wrapped_func):
		self.call_id = 0
		self.call_stack = []
		self.wrapped_func = wrapped_func
		self.call_tree = None

	def __call__(self, *args, **kwargs):
		call = self.create_call(*args, **kwargs)
		self.call_stack.append(call)

		ret = self.wrapped_func(*args, **kwargs)
		call.return_value = ret

		self.call_stack.pop()
		return ret

	def create_call(self, *args, **kwargs):
		called_function = self.wrapped_func
		self.call_id = self.call_id + 1
		call = Call(
			self.call_id, 
			called_function, 
			self.call_stack[-1] if self.call_stack else None, 
			{"args": args, "kwargs": kwargs}, 
			None
		)
		if not self.call_tree:
			self.call_tree = call
		return call

