'''
Created on Feb 29, 2016
@author: hanhanwu
'''
from sqlite3 import dbapi2 as sqlite


class onehidden_nn:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)
        
        
    def __del__(self):
        self.con.close()
        
        
    def create_tables(self):
        self.con.execute('drop table if exists hidden_node')
        self.con.execute('drop table if exists input_hidden')
        self.con.execute('drop table if exists hidden_output')
        
        self.con.execute('create table hidden_node(create_key)')
        self.con.execute('create table input_hidden(fromid, toid, strength)')
        self.con.execute('create table hidden_output(fromid, toid, strength)')
        self.con.commit()


def main():
    dbname = ''
    my_nn = onehidden_nn(dbname)
    
if __name__ == '__main__':
    main()
