#!/usr/bin/python

import sqlite3
from catalog import Catalog
from table import Table


class DBConnector(object):
	def __init__(self, catalog):
		self.catalog = catalog
		self.conn = sqlite3.connect(catalog.db_name)

	def execute_query(self, query):
		_cursor = self.conn.cursor()
		_cursor.execute(query)

	def query_create_table(self, table):
		query = "CREATE TABLE {} ({})".format(table.name, table.format_columns_for_query())
		print query
		self.execute_query(query)

	def initialize_catalog(self):
		self.catalog.initialize()
		for table in self.catalog.tables:
			self.query_create_table(table)






	

