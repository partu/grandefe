class Table(object):
	def __init__(self, name, columns):
		self.name = name
		self.columns = columns


	def format_columns_for_query(self):
		print 
		return [" ".join(elem) for elem in self.columns]
		 