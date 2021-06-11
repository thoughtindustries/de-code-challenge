"""
etl.py

File containing helper functions for performing ETL tasks.

The methods to be implemented are extract and load.

This file is utilized and tested by test.py.
"""
import psycopg2
import psycopg2.extras
from rethinkdb import RethinkDB
import logging
import uuid
import sys
import pandas

r = RethinkDB()
UUID_NAMESPACE = uuid.UUID('bfb3eb2d-4312-4606-82a8-31bf794af10a')
LOG_FORMAT = "%(asctime)s - %(threadName)s - %(module)s - %(levelname)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
TIMESTAMP_FORMAT_TZ = "%Y-%m-%d %H:%M:%S %Z"
RDB_TABLES = ['companies', 'users', 'clients']
RDB_TABLE_MAP = {
  'companies': {
    'record': 'companies'
  },
  'clients': {
    'record': 'clients'
  },
  'users': {
    'record': 'users',
    'singular': 'user',
    'attributes': {
      'purchasedCourses': 'users_purchasedCourses'
    }
  }
}


def rdb_connect():
  """
  Wrapper for getting a RethinkDB connection
  :return:
  """
  return r.connect(**{'host': 'rethinkdb', 'port': '28015', 'db': 'test'})


def pg_connect():
  """
  Wrapper for getting a PostgreSQL connection
  :return:
  """
  conn = psycopg2.connect(dbname='postgres', user='postgres', port=5432, host='postgres')
  conn.set_session(autocommit=True)
  return conn


def setup_logger(name):
  """
  Sets up a simple logger
  :param name: Name to associate with logger
  :return: logger
  """
  new_logger = logging.getLogger(name)
  new_logger.setLevel(logging.DEBUG)
  ch = logging.StreamHandler(sys.stdout)
  ch.setLevel(logging.DEBUG)
  ch.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
  new_logger.addHandler(ch)
  return new_logger


logger = setup_logger('etl')


def init_rethinkdb():
  """
  Initializes the RethinkDB instance
  :return:
  """
  with rdb_connect() as conn:
    logger.info('Initializing RethinkDB...')
    for table in RDB_TABLES:
      logger.info(f'Creating {table}')
      try:
        r.table_create(table).run(conn)
      except Exception as e:
        logger.warning(f"{table} already exists")
      try:
        r.table(table).index_create('updatedAt').run(conn)
      except Exception as e:
        logger.warning(f"updatedAt index already exists in {table}")


def init_postgres():
  """
  Initializes the PostgreSQL instance
  :return:
  """
  with pg_connect() as conn:
    logger.info("Initializing PostgreSQL...")
    cursor = conn.cursor()
    cursor.execute(open('pg_schema.sql', 'r').read())


def reset_rethinkdb(*tables):
  """
  Resets one or more tables in RethinkDB
  :param tables: One or more table name strings to be reset
  :return:
  """
  with rdb_connect() as conn:
    for table in tables:
      logger.info(f"Resetting {table} in RethinkDB")
      r.table(table).delete().run(conn)


def reset_postgres(*tables):
  """
  Resets one or more table in PostgreSQL
  :param tables: One or more table name strings to be reset
  :return:
  """
  with pg_connect() as conn:
    cursor = conn.cursor()
    for table in tables:
      logger.info(f"Resetting {table} in PostgreSQL")
      cursor.execute(f"truncate \"{table}\" cascade")


def extract(table):
  """
  Extracts all records from the specified table from RethinkDB, returning a dictionary of lists whose keys
  represent the destination tables in PostgreSQL.
  :param table: String representing the name of the table to extract from
  :return: Dictionary of lists whose keys represent the destination tables in PostgreSQL
  """
  record_collection = {}
  # TODO Implement extract function
  return record_collection


def load(record_collection):
  """
  Loads records from a record collection dictionary into PostgreSQL. This function should upsert records, meaning if
  a record exists, it get's updated and if it does not, it gets inserted.
  :param record_collection: Dictionary of lists whose keys represent the destination tables in PostgreSQL
  """
  # TODO Implement load function
  return None
