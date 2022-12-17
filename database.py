import psycopg2.extras


class Retrieval:
    def __init__(self):
        pass


class DataBaseModel:
    def __init__(self, hostname, database, username, pwd, port_id, table_name):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.pwd = pwd
        self.port_id = port_id
        self.table_name = table_name
        self.conn = None
        self.lister = []

    def retrieve(self, name_string):
        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pwd,
                    port=self.port_id) as self.conn:

                with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute(f''' 
                                SELECT {name_string}
                                FROM {self.table_name} ''')
                    # cur.execute('SELECT width FROM "PygameMove"')
                    for record in cur.fetchall():
                        self.lister.append(record[name_string])
        except Exception as error:
            print(f'{error}namor')
        finally:
            if self.conn is not None:
                self.conn.close()
        return self.lister

