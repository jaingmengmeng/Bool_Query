import os
import pymysql

class MySQL:
    """Connection to a MySQL"""
    connection = None
    cursor = None

    def __init__(self, user='root', password='18810877326', database='BOOL_QUERY', charset='utf-8', port=3306, host='localhost'):
        self.connection = pymysql.connect(
            host = host,
            port = port,
            user = user,
            passwd = password,
            db = database,
            cursorclass = pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
        return self.cursor

    def fetchone(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except:
            print("Error: unable to fetch data")
            return
    
    def fetchall(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            print("Error: unable to fetch data")
            return

    def close(self):
        if (self.cursor):
            self.cursor.close()
        self.connection.commit()
        self.connection.close()

def get_documents(dir):
    document_list = []
    for dirpath, dirnames, filenames in os.walk(dir):
        for file in filenames:
            document_list.append(file)
            # document_list.append(os.path.join(dirpath, file))
    return document_list

def get_dictionary(path):
    dictionary = []
    if os.path.exists(path):
        file = open(path)
        for line in file:
            if line != '\n':
                word = line.split('\t')[0]
                if word != '':
                    file_list = [ {
                        'url' : each.split(':')[0],
                        'count' : int(each.split(':')[1])
                    } for each in line.split('\t')[1].split(';')]
                    dictionary.append({
                            'word' : word,
                            'file_list' : file_list
                        })
    return dictionary

if __name__ == '__main__':
    # connect to mysql
    mysql = MySQL()

    # insert documents
    document_list = get_documents(os.path.join(os.getcwd(), 'docs', 'Shakespeare'))
    for document in document_list:
        insert_document = 'INSERT INTO document (url) VALUES ("%s");' % (document)
        mysql.execute(insert_document)

    # insert dictionary
    dictionary = get_dictionary(os.path.join(os.getcwd(), 'output', 'Shakespeare.txt'))
    for item in dictionary:
        for file in item['file_list']:
            select_document = 'SELECT * FROM document WHERE url = "%s";' % (file['url'])
            results = mysql.fetchone(select_document)
            if results != None:
                insert_dictionary = 'INSERT INTO dictionary (word, document_id, count) VALUES ("%s", %d, %d);' % (item['word'], results['id'], file['count'])
                mysql.execute(insert_dictionary)

    # close database
    mysql.close()