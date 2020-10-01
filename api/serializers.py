from rest_framework import serializers


class RecursionTreeSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	func = serializers.CharField()
	called_with = serializers.DictField()
	caller = serializers.CharField()
	return_value = serializers.CharField()

	def to_representation(self, instance):
		ret = super().to_representation(instance)
		ret["func"] = str(instance)

		for child in instance.children:
			ret['children'] = ret.get('children', [])
			ret['children'].append(RecursionTreeSerializer(child).data)
		return ret


class ArgumentSerializer(serializers.Serializer):
	value = serializers.CharField(allow_blank=True)
	type = serializers.ChoiceField(choices=('int', 'str', 'list', 'tuple', 'set', 'dict',))


class KeyWordArgumentSerializer(ArgumentSerializer):
	name = serializers.CharField()


class VisualizeFunctionSerializer(serializers.Serializer):
	func_name = serializers.CharField()
	code = serializers.CharField()
	args = ArgumentSerializer(many=True)
	kwargs = KeyWordArgumentSerializer(many=True, required=False)

	def validate(self, attrs):
		args_list = attrs['args']
		args = []
		builtins = globals()['__builtins__']
		for arg in args_list:
			arg_type = builtins[arg['type']]
			args.append(arg_type(arg['value']))
		attrs['args'] = args

		kwargs_list = attrs.get('kwargs', [])
		kwargs = {}
		for kwarg in kwargs_list:
			arg_type = builtins[kwarg['type']]
			kwargs[kwarg['name']] = arg_type(kwarg['value'])
		attrs['kwargs'] = kwargs
		return attrs



