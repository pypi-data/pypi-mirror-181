import os
from Datapyck.errors import *

class Datapack:
  def __init__(self, name="New Datapack", description="A datapack created using the Datapyck Python module.", version="1.19", directory=""):
    if type(name) is not str:
      raise ArgTypeError("Datapack", name, 1, str)
    if type(description) is not str:
      raise ArgTypeError("Datapack", description, 2, str)
    if type(version) is not str:
      raise ArgTypeError("Datapack", version, 3, str)
    if type(directory) is not str:
      raise ArgTypeError("Datapack", directory, 4, str)
    if version not in ["1.17", "1.17.1", "1.18", "1.18.1", "1.18.2", "1.19", "1.19.1", "1.19.2", "1.19.3"]:
      raise ValueError(f"not supported version \'{version}\'")
    if not os.path.exists(directory) and directory != "":
      raise FileNotFoundError(f"no such directory: \'{directory}\'")
    self.name = name
    self.description = description
    self.version = version
    self.directory = directory
    self.namespace = name.lower().replace(" ", "_")
    #Make the datapack
    def checkpath(name):
      if os.path.exists(os.path.join(self.directory, name)):
        try:
          os.rename(os.path.join(self.directory, name), name + "_original")
        except:
          checkpath(name + "_original")
    def pathtry():
      try:
        os.mkdir(os.path.join(self.directory, self.name))
      except:
        checkpath(self.name)
        pathtry()
    pathtry()
    pack = open(os.path.join(self.directory, self.name, "pack.mcmeta"), "w")
    if self.version.startswith("1.17"):
      pack.write("{\n  \"pack\": {\n    \"pack_format\": 7,\n    \"description\": \"" + description + "\"\n  }\n}")
    if self.version.startswith("1.18") and not version == "1.18.2":
      pack.write("{\n  \"pack\": {\n    \"pack_format\": 8,\n    \"description\": \"" + description + "\"\n  }\n}")
    if self.version == "1.18.2":
      pack.write("{\n  \"pack\": {\n    \"pack_format\": 9,\n    \"description\": \"" + description + "\"\n  }\n}")
    if self.version.startswith("1.19"):
      pack.write("{\n  \"pack\": {\n    \"pack_format\": 10,\n    \"description\": \"" + description + "\"\n  }\n}")
    os.mkdir(os.path.join(self.directory, self.name, "data"))
    os.mkdir(os.path.join(self.directory, self.name, "data", "minecraft"))
    os.mkdir(os.path.join(self.directory, self.name, "data", "minecraft", "tags"))
    os.mkdir(os.path.join(self.directory, self.name, "data", "minecraft", "tags", "functions"))
    loadjson = open(os.path.join(self.directory, self.name, "data", "minecraft", "tags", "functions", "load.json"), "w")
    loadjson.write("{\n	\"values\": [\n		\"" + self.namespace + ":load\"\n	]\n}")
    tickjson = open(os.path.join(self.directory, self.name, "data", "minecraft", "tags", "functions", "tick.json"), "w")
    tickjson.write("{\n	\"values\": [\n		\"" + self.namespace + ":tick\"\n	]\n}")
    os.mkdir(os.path.join(self.directory, self.name, "data", self.namespace))
    os.mkdir(os.path.join(self.directory, self.name, "data", self.namespace, "functions"))
    open(os.path.join(self.directory, self.name, "data", self.namespace, "functions", "load.mcfunction"), "x")
    open(os.path.join(self.directory, self.name, "data", self.namespace, "functions", "tick.mcfunction"), "x")
  def write(self, function, command):
    if type(function) is not str:
      raise ArgTypeError("write", function, 1, str)
    file = open(os.path.join(self.directory, self.name, "data", self.namespace, "functions", f"{function}.mcfunction"), "a")
    file.write(str(command) + "\n")