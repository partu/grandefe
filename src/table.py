class Table(object):
	def __init__(self, name, columns):
		self.name = name
		self.columns = columns



	def column_names(self):
		return [name for name,_type in columns]


	def format_columns_for_query(self):
		return ", ".join([" ".join(column) for column in self.columns])
		 