import functools
import inspect
import tracemalloc
from datetime import datetime

from rest_framework.exceptions import ValidationError


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
		arg_str = ', '.join(map(str, self.called_with["args"]))

		kwargs = self.called_with["kwargs"]
		kwarg_str = ""
		for param in kwargs:
			kwarg_str = kwarg_str + ", {0}={1}".format(param, str(kwargs[param]))

		return self.func.__name__ + "(" + arg_str + kwarg_str + ")"

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

	def __init__(self, wrapped_func, time_limit=5):
		self.call_id = 0
		self.call_stack = []
		self.wrapped_func = wrapped_func
		self.call_tree = None

		self.start_time = None
		self.time_limit = time_limit
		self.total_memory = 0

	def __call__(self, *args, **kwargs):
		# if not self.start_time:
		# 	self.start_time = datetime.now()
		#
		# if (datetime.now() - self.start_time).seconds >= self.time_limit:
		# 	raise ValidationError("Time limit exceeded.")

		call = self.handle_stackframe_without_leak()
		self.call_stack.append(call)

		ret = self.wrapped_func(*args, **kwargs)
		call.return_value = ret

		self.call_stack.pop()
		return ret

	def handle_stackframe_without_leak(self):
		frame = inspect.currentframe()
		wrapper_frame = frame.f_back
		try:
			called_function = wrapper_frame.f_locals['self'].wrapped_func
			args = wrapper_frame.f_locals['args']
			kwargs = wrapper_frame.f_locals.get('kwargs', {})

			self.call_id = self.call_id + 1
			call = Call(self.call_id, called_function, self.call_stack[-1] if self.call_stack else None, {"args": args, "kwargs": kwargs}, None)
			if not self.call_tree:
				self.call_tree = call
			return call
		finally:
			del frame
			del wrapper_frame


