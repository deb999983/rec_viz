def quicksort(items):
	if len(items) <= 1:
		return items
	else:
		pivot = items[0]
		lesser = quicksort([x for x in items[1:] if x < pivot])
		greater = quicksort([x for x in items[1:] if x >= pivot])
		return lesser + [pivot] + greater


i = quicksort([5,4,3,2,1])
print(i)
