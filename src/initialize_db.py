#!/usr/bin/python

import sqlite3

#Create database if doesn't existed before




class DBConnector(object):
	def __init__(self, db_name):
		self.conn = sqlite3.connect(db_name)

	def execute_query(self, query):
		_cursor = self.conn.cursor()
		_cursor.execute(query)

	def query_create_table(self,table_name,columns):
		''' columns is a dictionary with name as key and type as value ''' 
		columns = [name+' '+_type	for name, _type in columns.iteritems()]
		self.execute_query("CREATE TABLE {} ({})".format(table_name, ", ".join(columns)))


	def initialize_db(self):
		conn.create_users_table()
		conn.create_teams_table()
		conn.create_players_table()





	def create_history_of_players_by_date(self):
		#query = "CREATE TABLE history (player_id INTEGER PRIMARY KEY, round INTEGER PRIMARY KEY, present INTEGER, not-present INTEGER, mvp INTEGER, goal_pen INTEGER, goals INTEGER,  "
		pass	

	def create_users_table(self):
		table_name = 'users'
		columns = {'email': 'TEXT PRIMARY KEY',
				   'user_name':'TEXT',
				   'team_name':'TEXT'}

		self.query_create_table(table_name,columns)


	def create_teams_table(self):
		table_name = 'teams'			
		columns = {'user_id':'INTEGER',
				   'team_name':'TEXT',
				   'player1_id':'INTEGER',
				   'player2_id':'INTEGER',
				   'player3_id':'INTEGER',
				   'player4_id':'INTEGER',
				   'player5_id':'INTEGER'}

		self.query_create_table(table_name,columns)


	def create_players_table(self):
		table_name = 'players'
		columns = {'player_id':'INTEGER PRIMARY KEY ASC',
				   'nombre':'TEXT',
				   'posicion':'TEXT',
				   'categoria':'TEXT'}

		self.query_create_table(table_name,columns)


if __name__ == '__main__':

	db_name = 'defe.db'
	conn = DBConnector(db_name)

	

