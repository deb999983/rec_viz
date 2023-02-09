class Solution:
	def recur_fibo(self, n):

		if n <= 1:
			return n
		else:
			return self.recur_fibo(n-1) + self.recur_fibo(n-2)
	
	def __str__(self) -> str:
		return "Solution"

s = Solution()
r = s.recur_fibo(10)
print(r)
