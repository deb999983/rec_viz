import json
import sys
from visualizer.call import Call


def string_vals(**kwargs):
	return {key: str(value) for key, value in kwargs.items()}


class Tracer:
	def __init__(self, func_name: str) -> None:
		self.func_name = func_name
		self.call_stack = []
		self.call_tree = None
		self.call_id = 1
	
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
		with open(file_name, 'rb') as f:
			code = compile(f.read(), file_name, 'exec')

			# Trace calls.
			sys.setprofile(self.trace_calls)   
			exec(code, {})
			sys.setprofile(None)
 
	
	def save_output(self, file_name="output.json"):
		t = Call.to_dict(self.call_tree)
		# print(f"Output: ============ {t} ===========")
		with open(file_name, mode='w') as fp:
			json.dump(t, fp)
		return t
