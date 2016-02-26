#!/usr/bin/python

from dbconnector import DBConnector
from catalog import DefeCatalog


if __name__ == '__main__':

	catalog = DefeCatalog()
	connector = DBConnector(catalog)
	connector.initialize_catalog()
