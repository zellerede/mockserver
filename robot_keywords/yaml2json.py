import json
import yaml

class yaml2json(object):
    """ robot helper just to avoid km long json's with escaped quotes within json's """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    
    def get_json_from_yaml(self, _yaml):
        with open(_yaml) as yaml_file:
             content = yaml.load(yaml_file)
        return json.dumps(content)
    
