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

    def retrieve_data(self, cur, element, listing):
        cur.execute(f''' 
                    SELECT {element}
                    FROM {self.table_name} ''')
        # cur.execute('SELECT width FROM "PygameMove"')
        for record in cur.fetchall():
            listing.append(record[element])
        return listing

    def retrieve(self, name_string):
        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pwd,
                    port=self.port_id) as self.conn:

                with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    for i in name_string:
                        listing = []
                        result = self.retrieve_data(cur, i, listing)
                        self.lister.append(result)
        except Exception as error:
            print(f'{error}namor')
        finally:
            if self.conn is not None:
                self.conn.close()
        return self.lister

if __name__ == '__main__':
    test = DataBaseModel('localhost', 'test', 'postgres', 'KAYN', 5432, '"Music_Database"')
    test.retrieve(['name', 'file_name'])
    print(test.lister)
