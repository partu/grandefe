import sqlite3
import os
from catalog import Catalog
from table import Table


class DBConnector(object):
	def __init__(self, db_name):
		self.db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),db_name)
		self.conn = sqlite3.connect(self.db_name)

	def execute_query(self, query):
		_cursor = self.conn.cursor()
		_cursor.execute(query)
		return _cursor

	def commit(self):
		self.conn.commit()

	def query_create_table(self, table):
		query = "CREATE TABLE {} ({})".format(table.name, table.format_columns_for_create_query())
		self.execute_query(query)

	def init_db_with_catalog(self, catalog):
		if os.path.isfile(self.db_name):
			os.rename(self.db_name, self.db_name + '.old')
			self.conn = sqlite3.connect(self.db_name)
		for table in catalog.tables:
			self.query_create_table(table)

		for query in catalog.queries_for_init():
			self.execute_query(query)









	

