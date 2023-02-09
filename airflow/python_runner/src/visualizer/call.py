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
