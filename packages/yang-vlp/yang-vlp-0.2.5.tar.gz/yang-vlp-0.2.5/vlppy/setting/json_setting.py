import os,sys
import re
import json

# 参数设置
class Settings(object):
    # set default json file path 
    _default_dirname = os.path.abspath(os.path.dirname(__file__)) # current file dir
    _file_name = "settings.json"
    
    # INIT SETTINGS
    def __init__(self,settings_path:str=...):
        """set file path
        settings_path: .json file path or directory(include settings.json)
                        default: settings.json file in the directory where the current file resides
        """
        super(Settings, self).__init__()
        # set file path
        self.set_settings_path(settings_path)

        # DICTIONARY WITH SETTINGS
        # Just to have objects references
        self.items = {}

        # DESERIALIZE
        self.deserialize() # 从文件中加载json数据,转为dict型数据,赋值给self.items

    def set_settings_path(self,settings_path:str=...):
        """set file path
        settings_path: settings.json file path or directory
        """
        settings_path = settings_path if settings_path != Ellipsis else self._default_dirname
        settings_path = os.path.abspath(os.path.normpath(settings_path)) #规范路径中'//'为'/'

        if settings_path.endswith(".json"):
            self._settings_path = settings_path
        else:
            self._settings_path = os.path.join(settings_path,self._file_name)
        
        if not os.path.exists(self._settings_path):
            sys.exit(f"WARNING: \".json\" file not found! check in the path \"{self._settings_path}\"")
    
    def get_settings_path(self) -> str: 
        return self._settings_path

    # 去除json中注释 "//"、"/**/"
    def _parse_json(self,json_raw):
        """Remove json comments "//", "/* */"
        json_raw: raw json
        """
        try:
            json_str1 = re.sub(re.compile('(//[\\s\\S]*?\n)'),'',json_raw)
            json_str2 = re.sub(re.compile('(/\*[\\s\\S]*?\*/)'),'',json_str1)
            return json.loads(json_str2)
        except:
            raise Exception("Remove json comments error!")

    # 序列化:将字典型数据转为json，并保存到文件
    def serialize(self):
        # WRITE JSON FILE
        with open(self._settings_path, "w", encoding='utf-8') as fd:
            json.dump(self.items, fd, indent=4)

    # 反序列化:从文件中加载json数据，并转为dict型数据
    def deserialize(self):
        # READ JSON FILE
        with open(self._settings_path, "r", encoding='utf-8') as fd:
            self.items = self._parse_json(fd.read())


