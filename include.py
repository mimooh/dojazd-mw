from collections import OrderedDict
import inspect
import json

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

dd=Dump
JSON=Json()

