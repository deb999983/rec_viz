#!/usr/bin/env python

import ast
import json
import os
import sys
from visualizer.tracer import Tracer

code_path = os.environ.get("CODE_PATH" ,"/workspaces/rec_viz/data/code/python")
output_path = os.environ.get("OUTPUT_PATH" ,"/workspaces/rec_viz/data/output/python")

def execute(input_file_name: str, output_file_name:str, func_name: str):
    tracer = Tracer.get_instance(func_name)
    error = tracer.run(os.path.join(code_path, os.path.join(code_path, input_file_name)))
    if error:
        tracer.save_error(os.path.join(output_path, output_file_name))
        return 1
    
    tracer.save_output(os.path.join(output_path, output_file_name))
    return 0

if __name__ == "__main__":
    params = ast.literal_eval(sys.argv[1])
    input_file_name, output_file_name, func_name = params["input_file_name"], params["output_file_name"], params["func_name"]
    print(execute(input_file_name, output_file_name, func_name))
