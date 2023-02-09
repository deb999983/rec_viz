from common.visualizer.tracer import Tracer
from common.visualizer.call import Call

tracer = Tracer.get_instance("recur_fibo")
tracer.run(
"""
def recur_fibo(n):
    if n <= 1:
        return n
    else:
        return recur_fibo(n-1) + recur_fibo(n-2)

recur_fibo(5)
"""
)


import json
with open("x.json", mode="w") as fp:
    d = Call.to_dict(tracer.call_tree)
    print(d)
    json.dump(d, fp)

