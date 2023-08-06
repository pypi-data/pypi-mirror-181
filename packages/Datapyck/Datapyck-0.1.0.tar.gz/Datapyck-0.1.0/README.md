# Datapyck
A small package for creating simple Minecraft datapacks for 1.17+.
This package is NOT made for people unexperienced in either Python or Minecraft datapack creation.

### Installation
```
pip install Datapyck
```

### Get started
How to create a simple datapack that welcomes you once the world is reloaded:
```Python
from Datapyck import Datapack, Tellraw

# Instantiate a Datapack object
datapack = Datapack(
    name="My Datapack",
    description="A simple demo to Datapyck.",
    version="1.19.3"
)

# Instantiate a Tellraw object
welcome_message = Tellraw(
    selector="everyone",
    text="Hello there! The datapack has just loaded!",
    color="green",
    underline=True
)

# Write the Tellraw to the load function
datapack.write("load", welcome_message)
```