class ElmList():
	def __init__(self, value=None, next=None):
		self.value = value
		self.next = next

class ChainedList()
	def __init__(self):
		self.first = None
		self.last = None
		
	def add_first(self, obj):
		new = ElmList(obj, self.first)
		self.first = new
		
	def add_last(self, obj):
		new = ElmList(obj, None)
		self.last.next = new
		self.last = self.last.next
		
	def get(self, n):
		current = self.first
		while(n > 0):
			current = current.next
			n -= 1
		return current
	
