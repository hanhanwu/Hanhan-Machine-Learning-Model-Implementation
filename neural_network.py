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
        
        self.con.execute('create index if not exists hidden_nodeidx on hidden_node(create_key)')
        self.con.execute('create index if not exists ih_fromidx on input_hidden(fromid)')
        self.con.execute('create index if not exists ih_toidx on input_hidden(toid)')
        self.con.execute('create index if not exists ho_fromidx on hidden_output(fromid)')
        self.con.execute('create index if not exists ho_toidx on hidden_output(toid)')
        self.con.commit()
        
    
    def get_strength(self, fromid, toid, layer):
        if layer == 0: tb = 'input_hidden'
        else: tb = 'hidden_output'
        
        cur = self.con.execute("""
        select strength from %s where fromid=%d and toid=%d
        """ % (tb, fromid, toid)).fetchone()
        if cur == None:
            if layer == 0: return -0.2
            elif layer == 1: return 0
        return cur[0]


def main():
    dbname = ''
    my_nn = onehidden_nn(dbname)
    
if __name__ == '__main__':
    main()
