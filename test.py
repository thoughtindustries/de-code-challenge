import etl
import uuid
from datetime import datetime
from datetime import timezone

etl.init_rethinkdb()


def test_rdb_init():
  etl.init_rethinkdb()

  with etl.rdb_connect() as conn:
    table_list = etl.r.table_list().run(conn)

  assert table_list == sorted(etl.RDB_TABLES)


def test_rdb_reset():
  counts = []

  etl.init_rethinkdb()
  etl.reset_rethinkdb('companies', 'companies')
  conn = etl.rdb_connect()
  etl.r.table('companies').insert({'name': 'test'}).run(conn)
  counts.append(etl.r.table('companies').count().run(conn))
  etl.reset_rethinkdb('companies')
  counts.append(etl.r.table('companies').count().run(conn))
  conn.close()

  assert counts == [1, 0]


def test_pg_reset():
  counts = []

  etl.reset_postgres('users')
  with etl.pg_connect() as conn:
    cursor = conn.cursor()
    cursor.execute(f"insert into users values ('{uuid.uuid4()}')")
    cursor.execute("select count(*) from users")
    result = cursor.fetchall()[0][0]
    counts.append(result)
    etl.reset_postgres('users', 'companies')
    cursor.execute("select count(*) from users")
    result = cursor.fetchall()[0][0]
    counts.append(result)

  assert counts == [1, 0]


class TestCompanies:
  etl.reset_rethinkdb('companies')
  etl.reset_postgres('companies')

  def test_insert(self):
    with etl.rdb_connect() as conn:
      etl.r.table('companies').insert([
        {
          'id': str(uuid.uuid5(etl.UUID_NAMESPACE, 'testco')),
          'name': 'testco',
          'updatedAt': datetime(2021, 6, 1, 0, 0).replace(tzinfo=timezone.utc)
        }
      ]).run(conn)

    etl.load(etl.extract('companies'))

    with etl.pg_connect() as conn:
      with conn.cursor(cursor_factory=etl.psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute("select * from companies")
        result = cursor.fetchall()

    assert result == [
      {
        'id': str(uuid.uuid5(etl.UUID_NAMESPACE, 'testco')),
        'name': 'testco',
        'updatedAt': datetime(2021, 6, 1, 0, 0)
      }
    ]


class TestUsers:
  etl.reset_rethinkdb('users')
  etl.reset_postgres('users', 'users_purchasedCourses')

  def test_insert(self):
    with etl.rdb_connect() as conn:
      etl.r.table('users').insert([
        {
          'id': str(uuid.uuid5(etl.UUID_NAMESPACE, 'user1')),
          'name': 'user1',
          'client': None,
          'company': str(uuid.uuid5(etl.UUID_NAMESPACE, 'testco')),
          'purchasedCourses':
            [
              {
                'id': str(uuid.uuid5(uuid.uuid5(etl.UUID_NAMESPACE, 'user1'), 'course-1')),
                'course': str(uuid.uuid5(etl.UUID_NAMESPACE, 'course-1')),
                'status': 'started'
              }
            ],
          'updatedAt': datetime(2021, 6, 1, 0, 0).replace(tzinfo=timezone.utc)
        }
      ]).run(conn)

    etl.load(etl.extract('users'))

    result = {}
    with etl.pg_connect() as conn:
      with conn.cursor(cursor_factory=etl.psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute("select * from users")
        result['users'] = cursor.fetchall()
        cursor.execute("select * from \"users_purchasedCourses\"")
        result['users_purchasedCourses'] = cursor.fetchall()

    assert result == {
      "users": [
        {
          'id': str(uuid.uuid5(etl.UUID_NAMESPACE, 'user1')),
          'name': 'user1',
          'company': str(uuid.uuid5(etl.UUID_NAMESPACE, 'testco')),
          'client': None,
          'updatedAt': datetime(2021, 6, 1, 0, 0)
        }
      ],
      "users_purchasedCourses": [
        {
          'id': str(uuid.uuid5(uuid.uuid5(etl.UUID_NAMESPACE, 'user1'), 'course-1')),
          'user': str(uuid.uuid5(etl.UUID_NAMESPACE, 'user1')),
          'course': str(uuid.uuid5(etl.UUID_NAMESPACE, 'course-1')),
          'company': str(uuid.uuid5(etl.UUID_NAMESPACE, 'testco')),
          'status': 'started',
          'updatedAt': datetime(2021, 6, 1, 0, 0)
        }
      ]
    }

  def test_upsert(self):
    with etl.rdb_connect() as conn:
      etl.r.table('users').get(str(uuid.uuid5(etl.UUID_NAMESPACE, 'user1'))).update({
        'name': 'user-upsert'
      }).run(conn)

    etl.load(etl.extract('users'))

    with etl.pg_connect() as conn:
      with conn.cursor(cursor_factory=etl.psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute("select * from users")
        result = cursor.fetchall()

    assert result == [
      {
        'id': str(uuid.uuid5(etl.UUID_NAMESPACE, 'user1')),
        'name': 'user-upsert',
        'company': str(uuid.uuid5(etl.UUID_NAMESPACE, 'testco')),
        'client': None,
        'updatedAt': datetime(2021, 6, 1, 0, 0)
      }
    ]


class TestClients:
  etl.reset_rethinkdb('clients')
  etl.reset_postgres('clients')

  def test_insert(self):
    with etl.rdb_connect() as conn:
      etl.r.table('clients').insert([
        {
          'id': str(uuid.uuid5(etl.UUID_NAMESPACE, 'testclient')),
          'company': str(uuid.uuid5(etl.UUID_NAMESPACE, 'testco')),
          'name': 'testclient',
          'updatedAt': datetime(2021, 6, 1, 0, 0).replace(tzinfo=timezone.utc)
        }
      ]).run(conn)

    etl.load(etl.extract('clients'))

    with etl.pg_connect() as conn:
      with conn.cursor(cursor_factory=etl.psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute("select * from clients")
        result = cursor.fetchall()

    assert result == [
      {
        'id': str(uuid.uuid5(etl.UUID_NAMESPACE, 'testclient')),
        'name': 'testclient',
        'company': str(uuid.uuid5(etl.UUID_NAMESPACE, 'testco')),
        'updatedAt': datetime(2021, 6, 1, 0, 0).replace()
      }
    ]
