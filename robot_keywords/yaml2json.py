import json
import yaml
from StringIO import StringIO

class yaml2json(object):
    """ robot helper just to avoid km long json's with escaped quotes within json's """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    
    def get_json_from_yaml(self, _yaml):
        """ inputs the yaml data string (not a file)
            and returns it in json format string """
        content = yaml.load( StringIO(_yaml) )
        return json.dumps(content)
    
