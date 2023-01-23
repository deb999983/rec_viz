import json
import sys
from api.visualizer import Call

call_tree = None
call_stack = []
call_id = 1

return_val_map = {}

def string_vals(**kwargs):
	return {key: str(value) for key, value in kwargs.items()}

def kwargs_string(**kwargs):
	return ','.join([f'{key}={str(value)}' for key, value in kwargs.items()])

def trace_lines(frame, event, arg):
    print(frame.f_lineno)

def trace_calls(frame, event, arg):	
	if frame.f_code.co_name != "recur_fibo":
		return

	if event == 'call':
		global call_id, call_tree
		call = Call(call_id, func='recur_fibo', caller=call_stack[-1] if call_stack else None, called_with={"args":[], "kwargs": string_vals(**frame.f_locals)})
		call_id = call_id + 1
		if not call_tree:
			call_tree = call
		call_stack.append(call)

	if event == "return" and call_stack:
		c: Call = call_stack.pop()
		c.return_value = arg


sys.setprofile(trace_calls)
class Solution:
	def recur_fibo(self, n):

		if n <= 1:
			return n
		else:
			return self.recur_fibo(n-1) + self.recur_fibo(n-2)
	
	def __str__(self) -> str:
		return "Solution"

s = Solution()
r = s.recur_fibo(5)
sys.setprofile(None)


from api.serializers import RecursionTreeSerializer
print(
	json.dumps(RecursionTreeSerializer(call_tree).data)
)
