class Table(object):
	def __init__(self, name, columns):
		self.name = name
		self.columns = columns



	def column_names(self):
		return [name for name,_type in columns]

	def format_columns_for_insert_query(self):
		return ", ".join([name for name, _ in self.columns if 'PRIMARY KEY' not in name ])


	def format_columns_for_create_query(self):
		return ", ".join([" ".join(column) for column in self.columns])
		 