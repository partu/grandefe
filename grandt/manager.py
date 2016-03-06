#!/usr/bin/python
import json

from src.csvparser import CSVParser
from argparse import ArgumentParser

from src.granDT import GranDT
from src.catalog import DefeCatalog
from src.utils import Player, TeamInfo
from src.constants import ROUND_NUMBER, STATS, NAME, CATEGORY, POSITION, VALUES, ACTIONS

def contract_players(csv_row):
	#The first player is in 3rd position (starting from 0).
	res = csv_row[:3]
	i = 3  
	while i < (len(csv_row) -1) :
		new_player = Player(csv_row[i], csv_row[i+1], csv_row[i+2])
		res.append(new_player)
		i += 3
	return res


def add_team(rows, granDT):
	rows = rows[1:] # this is because the first one is only names of the columns
	new_teams = []
	for row in rows:
		team = TeamInfo(*contract_players(row))	
		new_teams.append(team)
	try:
		granDT.add_teams(new_teams)
	except Exception, e:
		raise Exception("Error when adding teams: {}".format(e))



def add_players(rows, granDT):
	rows = rows[1:] # this is because the first one is only names of the columns
	new_players = []
	for row in rows:
		new_player = Player(*row)
		new_players.append(new_player)
	try:
		granDT.add_players(new_players)
	except Exception, e:
		raise Exception("Error when adding players: {}".format(e))


def add_round(rows, granDT):
	res = {ROUND_NUMBER:rows[0][1]}
	rows = rows[2:] #The first one and the seond one names of columns or already been used.
	
	#In this method we must crate a particular json
	stats = []
	for row in rows:
		player_stats = {NAME: row[0], POSITION: row[1], CATEGORY: row[2]}
		values = dict(zip(ACTIONS, row[3:]))
		values = {k:int(v) for k,v in values.iteritems()}
		player_stats.update({VALUES:values})
		stats.append(player_stats)

	res.update({STATS:stats})

	granDT.add_round(json.dumps(res))



if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('-f',dest='filename', help="The absolute path to the CSV file.")
	parser.add_argument('-t',dest='task', choices= ['AgregarJugadores','AgregarEquipos', 'AgregarFecha','NuevoGranDT'], help="The task to be done (Please select one of the three options).")

	args = parser.parse_args()


	if not args.task:
		parser.error('Missing arguments')


	#GranDt
	catalog = DefeCatalog()
	granDT = GranDT(catalog)

	if args.task == 'NuevoGranDT':
		granDT.init_db()

	else:
		#CSV file parser
		csvparser = CSVParser(args.filename)
		rows = csvparser.get_rows()

		if args.task == 'AgregarEquipos':
			add_team(rows, granDT)
		elif args.task == 'AgregarJugadores':
			add_players(rows, granDT)
		elif args.task == 'AgregarFecha':
			add_round(rows, granDT)
		else:
			raise Exception("Impossible")
		
	print 'Task accomplished.'		



