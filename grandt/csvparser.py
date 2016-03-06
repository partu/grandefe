import csv

class CSVParser(object):
	def __init__(self, filename):
		self.filename = filename

	def get_rows(self):
		res = [] 
		with open(self.filename, 'rb') as f:
			spamreader = csv.reader(f)
			for row in spamreader:
				res.append(row)
		return res #The first row is the name of the columns

