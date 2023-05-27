import ast
from tracer_decorator import Tracer


def modify_and_execute_script(code_string, func_name, decorator_function):
    # Parse the code string into an AST
    tree = ast.parse(code_string)

    # Modify the AST to add the decorator to the specified function
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            decorator_node = ast.Name(id=decorator_function.__name__, ctx=ast.Load())
            decorator_node.lineno = node.lineno
            decorator_node.col_offset = 0
            node.decorator_list.append(decorator_node)
            break
    else:
        raise ValueError(f"Function '{func_name}' not found in the code string")

    # Compile the modified AST back into code
    modified_code = compile(tree, '<string>', 'exec')

    # Prepare a new namespace for executing the modified code
    global_namespace = {
        'your_decorator_function': decorator_function
    }

    # Execute the modified code in the new namespace
    exec(modified_code, global_namespace, global_namespace)

    return global_namespace


# Example usage
code_string = '''
def some_function():
    print("Hello world")

class A:
    def fibonacci_of(self, n):
        if n in {0, 1}:  # Base case
            return n
        return self.fibonacci_of(n - 1) + self.fibonacci_of(n - 2)  # Recursive case

    @classmethod
    def fibonacci(cls, n):
        a = cls()
        a.fibonacci_of(n)


def another_function():
    print("Another function")

A.fibonacci(5)

# a = A()
# a.fibonacci_of(5)
'''

func_name = 'fibonacci_of'
t = Tracer(func_name)
decorated_functions = modify_and_execute_script(code_string, func_name, t.trace_calls)

# Call the decorated function
# decorated_functions[func_name]()


# def fibonacci_of(n):
#     if n in {0, 1}:  # Base case
#         return n
#     return fibonacci_of(n - 1) + fibonacci_of(n - 2)  # Recursive case
