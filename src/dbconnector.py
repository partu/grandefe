import sqlite3
from catalog import Catalog
from table import Table


class DBConnector(object):
	def __init__(self, db_name):
		self.conn = sqlite3.connect(db_name)

	def execute_query(self, query):
		_cursor = self.conn.cursor()
		_cursor.execute(query)
		self.conn.commit()
		return _cursor

	def query_create_table(self, table):
		query = "CREATE TABLE {} ({})".format(table.name, table.format_columns_for_create_query())
		self.execute_query(query)

	def init_db_with_catalog(self, catalog):
		for table in catalog.tables:
			self.query_create_table(table)

		for query in catalog.queries_for_init():
			self.execute_query(query)








	

