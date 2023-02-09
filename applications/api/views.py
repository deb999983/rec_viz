from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.serializers import VisualizeFunctionSerializer, RecursionTreeSerializer
from api.visualizer import Visualize


def create_func_visualizer(func_str, func_name):
	local_scope = {}

	try:
		exec(compile(func_str, '<string>', 'exec'), local_scope)

		function = local_scope[func_name]
		local_scope[func_name] = Visualize(function)
		return local_scope[func_name]
	except KeyError as e:
		raise ValidationError("No function with name {0} found in code".format(func_name))
	except Exception as e:
		raise ValidationError("Compile error {0}".format(str(e)))


def call_visualizer(visualizer, *args, **kwargs):
	visualizer(*args, **kwargs)



class VisualizeRecursionTreeView(CreateAPIView):
	serializer_class = VisualizeFunctionSerializer

	def initial(self, request, *args, **kwargs):
		"""
		Runs anything that needs to occur prior to calling the method handler.
		"""
		self.format_kwarg = self.get_format_suffix(**kwargs)

		# Perform content negotiation and store the accepted info on the request
		neg = self.perform_content_negotiation(request)
		request.accepted_renderer, request.accepted_media_type = neg

		# Determine the API version, if versioning is in use.
		version, scheme = self.determine_version(request, *args, **kwargs)
		request.version, request.versioning_scheme = version, scheme

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		visualizer = self.perform_create(serializer)
		return Response(RecursionTreeSerializer(visualizer.call_tree).data, status=status.HTTP_201_CREATED)

	def perform_create(self, serializer):
		code, func_name = serializer.validated_data['code'], serializer.validated_data['func_name']
		args, kwargs = serializer.validated_data['args'], serializer.validated_data['kwargs']

		visualizer = create_func_visualizer(code, func_name)

		call_visualizer(visualizer, *args, **kwargs)
		return visualizer
