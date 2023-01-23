def fibonacci(n):
	# Taking 1st two fibonacci nubers as 0 and 1
	FibArray = [0, 1]

	while len(FibArray) < n + 1:
		FibArray.append(0)

	if n <= 1:
		return n
	else:
		if FibArray[n - 1] == 0:
			FibArray[n - 1] = fibonacci(n - 1)

		if FibArray[n - 2] == 0:
			FibArray[n - 2] = fibonacci(n - 2)

	FibArray[n] = FibArray[n - 2] + FibArray[n - 1]
	return FibArray[n]



from api.visualizer import Visualize


###################################
# Examples
###################################
@Visualize
def factorial(n):
	if n == 1:
		return n

	return n * factorial(n - 1)


@Visualize
def recur_fibo(n):

	if n <= 1:
		return n
	else:
		return recur_fibo(n-1) + recur_fibo(n-2)


@Visualize
def ackermann(m, n):
	if m == 0:
		return n + 1
	if n == 0:
		return ackermann(m - 1, 1)
	n2 = ackermann(m, n - 1)
	return ackermann(m - 1, n2)


@Visualize
def quicksort(items):
	if len(items) <= 1:
		return items
	else:
		pivot = items[0]
		lesser = quicksort([x for x in items[1:] if x < pivot])
		greater = quicksort([x for x in items[1:] if x >= pivot])
		return lesser + [pivot] + greater


@Visualize
def powerSet(str1, index, curr):
	n = len(str1)

	# base case
	if (index == n):
		return

	print(curr)

	for i in range(index + 1, n):
		curr += str1[i]
		powerSet(str1, i, curr)
		curr = curr.replace(curr[len(curr) - 1], "")

	return


@Visualize
# Fibonacci Series using Dynamic Programming
def fibonacci(n):
	# Taking 1st two fibonacci nubers as 0 and 1
	FibArray = [0, 1]

	while len(FibArray) < n + 1:
		FibArray.append(0)

	if n <= 1:
		return n
	else:
		if FibArray[n - 1] == 0:
			FibArray[n - 1] = fibonacci(n - 1)

		if FibArray[n - 2] == 0:
			FibArray[n - 2] = fibonacci(n - 2)

	FibArray[n] = FibArray[n - 2] + FibArray[n - 1]
	return FibArray[n]


f_str = """
def recur_fibo(n):

	if n <= 1:
		return n
	else:
		return recur_fibo(n-1) + recur_fibo(n-2)


if __name__ == "__main__":
	from api.visualizer import Visualize
	Visualize(function)
"""

# import gc, tracemalloc, functools
# gc.collect()
#
# f = lambda total_size, trace: total_size + trace.size
# tracemalloc.start()
# s0 = tracemalloc.take_snapshot()
# m = [24392029302]*1000
# s1 = tracemalloc.take_snapshot()
# tracemalloc.stop()
#
# s0_size = functools.reduce(f, s0.traces, 0)
# s1_size = functools.reduce(f, s1.traces, 0)
#

