#!/usr/bin/env python

import os
import sys
from visualizer.tracer import Tracer

code_path = os.environ.get("CODE_PATH" ,"/workspaces/rec_viz/data/code/python")
output_path = os.environ.get("OUTPUT_PATH" ,"/workspaces/rec_viz/data/output/python")

def execute(file_name: str, func_name: str):
    tracer = Tracer.get_instance(func_name)
    tracer.run(os.path.join(code_path, os.path.join(code_path, file_name)))
    tracer.save_output(os.path.join(output_path, f"{file_name}.output.json"))

if __name__ == "__main__":
    file_name, func_name = sys.argv[1], sys.argv[2]
    execute(file_name, func_name)
