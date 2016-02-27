#!/usr/bin/python
from dbconnector import DBConnector
from catalog import DefeCatalog


if __name__ == '__main__':
	catalog = DefeCatalog()
	connector = DBConnector(catalog.db_name)
	connector.init_db_with_catalog(catalog)
