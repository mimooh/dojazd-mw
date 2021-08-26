from collections import OrderedDict
import inspect
import json
import sqlite3

class Dump:# {{{
    def __init__(self,*args):
        '''debugging function, much like print but handles various types better'''
        print()
        for struct in args:
            if isinstance(struct, list):
                for i in struct:
                    print(i)
            elif isinstance(struct, tuple):
                for i in struct:
                    print(i)
            elif isinstance(struct, dict):
                for k, v in struct.items():
                    print (str(k)+':', v)
            else:
                print(struct)
# }}}
class Json: # {{{
    def read(self,path): 
        try:
            f=open(path, 'r')
            dump=json.load(f, object_pairs_hook=OrderedDict)
            f.close()
            return dump
        except:
            raise SystemExit("include.py: Missing or invalid json: {}.".format(path)) 

    def write(self, data, path, pretty=0): 
        try:
            if pretty==1:
                pretty=json.dumps(data, indent=4)
                with open(path, "w") as f: 
                    json.dump(pretty, f)
            else:
                with open(path, "w") as f: 
                    json.dump(data, f)
        except:
            raise SystemExit("include.py: Cannot write json: {}.".format(path)) 


# }}}
class Sqlite: # {{{

    def __init__(self, handle, must_exist=0):
        '''
        must_exist=0: we are creating the database
        must_exist=1: Exception if there's no such file
        '''

        if must_exist == 1:
            assert os.path.exists(handle), "Expected to find an existing sqlite file at: {}.\nCWD: {}".format(handle, os.getcwd())


        self.SQLITE = sqlite3.connect(handle)
        self.SQLITE.row_factory=self._sql_assoc
        self.sqlitedb=self.SQLITE.cursor()

    def _sql_assoc(self,cursor,row):
        ''' Query results returned as dicts. '''
        d = OrderedDict()
        for id, col in enumerate(cursor.description):
            d[col[0]] = row[id]
        return d

    def query(self,query,data=tuple()):
        ''' Query sqlite, return results as dict. '''
        self.sqlitedb.execute(query,data)
        self.SQLITE.commit()
        if query[:6] in("select", "SELECT"):
            return self.sqlitedb.fetchall() 

    def dict_insert(self, table, named_records):
        columns = ', '.join(named_records.keys())
        placeholders = ':'+', :'.join(named_records.keys())
        query='INSERT INTO {} ({}) VALUES ({})'.format(table, columns, placeholders)
        self.query(query, named_records)

    def executemany(self,query,data=tuple()):
        ''' Query sqlite, return results as dict. '''
        self.sqlitedb.executemany(query,data)
        self.SQLITE.commit()

    def querydd(self,query,data=tuple()):
        ''' Debug query, instead of connecting shows the exact query and params. '''
        print(query)
        print(data)

    def dump(self):
        print("dump() from caller: {}, {}".format(inspect.stack()[1][1], inspect.stack()[1][3]))
        print("project: {}".format(os.environ['AAMKS_PROJECT']))
        print()
        for i in self.query('SELECT * FROM aamks_geom order by floor,type_pri,global_type_id'):
            print(i)
# }}}
class Segments_maps:# {{{
    def __init__(self):
        self.maps={}
        self.maps['segments']={
            '0000000000000001': 'wewn_poziom_dym0',
            '0000000000000011': 'wewn_poziom_dym1',
            '0000000000000101': 'wewn_pion_dym0',
            '0000000000000111': 'wewn_pion_dym1',
            '0000010100000000': 'zewn_drabina_przystawna',
            '0000100100000000': 'zewn_drabina_mechaniczna',
            '0000000100000000': 'zewn_pion',
            '0000001100000000': 'zewn_poziom',
            '0000000000010101': 'wewn_dym0_hydrant',
            '0000000000010001': 'wewn_dym0_hydrant',
            '0000000000010011': 'wewn_dym1_hydrant',
            '0000000000100001': 'wewn_dym0_lina_elewacja',
            '0000000000100011': 'wewn_dym1_lina_elewacja',
            '0000000000001001': 'wewn_dzwig',
            '0000000000001011': 'wewn_dzwig'
        }

        self.maps['wariants']={
            '0000000000000011': 'Wewnętrzne rozwinięcie gaśnicze od nasady tłocznej pompy',
            '0000000000001001': 'Rozwinięcie gaśnicze od hydrantu wewnętrznego',
            '0000000000000100': 'Działanie gaśnicze sprzętem podręcznym z wykorzystaniem dźwigu ratowniczego',
            '0000000000000000': 'Działanie gaśnicze sprzętem podręcznym',
            '0000000000010001': 'Rozwinięcie gaśnicze z wciąganiem linii wężowej po elewacji',
            '0000000000010101': 'Rozwinięcie gaśnicze z wciąganiem linii wężowej po elewacji z wykorzystaniem dźwigu ratowniczego',
            '0000001100000000': 'Gaszenie z poziomu ziemi',
            '0000010100000000': 'Gaszenie z drabiny przystawnej',
            '0000100100000000': 'Gaszenie z kosza drabiny lub podnośnika',
            '0000010100000001': 'Rozwinięcie gaśnicze z dostępem z drabiny przystawnej',
            '0000100100000001': 'Rozwinięcie gaśnicze z dostępem z kosza drabiny lub podnośnika',
            '0000000100000000': 'Podejrzane działania 0000000100000000',
            '0000000100000001': 'Podejrzane działania 0000000100000001'
        }
# }}}

dd=Dump
JSON=Json()
