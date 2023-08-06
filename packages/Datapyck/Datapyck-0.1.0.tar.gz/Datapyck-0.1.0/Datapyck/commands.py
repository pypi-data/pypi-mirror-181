from Datapyck.errors import *


def Tellraw(selector="@a", text="", color="white", bold=False, italic=False, underline=False, strike=False,
            obfuscated=False):
    if type(selector) is not str:
        raise ArgTypeError("Tellraw", selector, 1, str)
    if type(color) is not str:
        raise ArgTypeError("Tellraw", color, 3, str)
    if type(bold) is not bool:
        raise ArgTypeError("Tellraw", bold, 4, bool)
    if type(italic) is not bool:
        raise ArgTypeError("Tellraw", italic, 5, bool)
    if type(underline) is not bool:
        raise ArgTypeError("Tellraw", underline, 6, bool)
    if type(strike) is not bool:
        raise ArgTypeError("Tellraw", strike, 7, bool)
    if type(obfuscated) is not bool:
        raise ArgTypeError("Tellraw", obfuscated, 8, bool)
    selector = selector.lower()
    if selector != "everyone" and not selector.startswith("@a") and selector != "random" and not selector.startswith(
            "@r") and selector != "nearest" and not selector.startswith(
            "@p") and selector != "self" and not selector.startswith("@s"):
        raise ValueError(f"unrecognized selector: \'{selector}\'")
    return "tellraw " + selector.replace("everyone", "@a").replace("random", "@r").replace("nearest", "@p").replace(
        "self", "@s") + " {\"text\":\"" + str(text) + "\", \"color\":\"" + color + "\", \"bold\":" + str(
        bold).lower() + ", \"italic\":" + str(italic).lower() + ", \"underlined\":" + str(
        underline).lower() + ", \"strikethrough\":" + str(strike).lower() + ", \"obfuscated\":" + str(
        obfuscated).lower() + "}"


def SelectorTellraw(selector="@a", textselector="@s", color="white", bold=False, italic=False, underline=False,
                    strike=False, obfuscated=False):
    if type(selector) is not str:
        raise ArgTypeError("SelectorTellraw", selector, 1, str)
    if type(textselector) is not str:
        raise ArgTypeError("SelectorTellraw", textselector, 2, str)
    if type(color) is not str:
        raise ArgTypeError("SelectorTellraw", color, 3, str)
    if type(bold) is not bool:
        raise ArgTypeError("SelectorTellraw", bold, 4, bool)
    if type(italic) is not bool:
        raise ArgTypeError("SelectorTellraw", italic, 5, bool)
    if type(underline) is not bool:
        raise ArgTypeError("SelectorTellraw", underline, 6, bool)
    if type(strike) is not bool:
        raise ArgTypeError("SelectorTellraw", strike, 7, bool)
    if type(obfuscated) is not bool:
        raise ArgTypeError("SelectorTellraw", obfuscated, 8, bool)
    selector = selector.lower()
    textselector = textselector.lower()
    if selector != "everyone" and not selector.startswith("@a") and selector != "random" and not selector.startswith(
            "@r") and selector != "nearest" and not selector.startswith(
            "@p") and selector != "self" and not selector.startswith("@s"):
        raise ValueError(f"unrecognized selector: \'{selector}\'")
    if textselector != "everyone" and not textselector.startswith(
            "@a") and textselector != "random" and not textselector.startswith(
            "@r") and textselector != "nearest" and not textselector.startswith(
            "@p") and textselector != "self" and not textselector.startswith("@s"):
        raise ValueError(f"unrecognized selector: \'{textselector}\'")
    return "tellraw " + selector.replace("everyone", "@a").replace("random", "@r").replace("nearest", "@p").replace(
        "self", "@s") + " {\"selector\":\"" + textselector + "\", \"color\":\"" + color + "\", \"bold\":" + str(
        bold).lower() + ", \"italic\":" + str(italic).lower() + ", \"underlined\":" + str(
        underline).lower() + ", \"strikethrough\":" + str(strike).lower() + ", \"obfuscated\":" + str(
        obfuscated).lower() + "}"


def KeybindTellraw(selector="@a", bind="forward", color="white", bold=False, italic=False, underline=False,
                   strike=False, obfuscated=False):
    if type(selector) is not str:
        raise ArgTypeError("KeybindTellraw", selector, 1, str)
    if type(bind) is not str:
        raise ArgTypeError("KeybindTellraw", bind, 2, str)
    if type(color) is not str:
        raise ArgTypeError("KeybindTellraw", color, 3, str)
    if type(bold) is not bool:
        raise ArgTypeError("KeybindTellraw", bold, 4, bool)
    if type(italic) is not bool:
        raise ArgTypeError("KeybindTellraw", italic, 5, bool)
    if type(underline) is not bool:
        raise ArgTypeError("KeybindTellraw", underline, 6, bool)
    if type(strike) is not bool:
        raise ArgTypeError("KeybindTellraw", strike, 7, bool)
    if type(obfuscated) is not bool:
        raise ArgTypeError("KeybindTellraw", obfuscated, 8, bool)
    selector = selector.lower()
    bind = bind.lower()
    if selector != "everyone" and not selector.startswith("@a") and selector != "random" and not selector.startswith(
            "@r") and selector != "nearest" and not selector.startswith(
            "@p") and selector != "self" and not selector.startswith("@s"):
        raise ValueError(f"unrecognized selector: \'{selector}\'")
    if bind != "forwards" and bind != "backwards" and bind != "left" and bind != "right" and bind != "jump" and bind != "sneak" and bind != "sprint" and bind != "inventory" and bind != "attack" and bind != "use" and bind != "pick" and bind != "drop" and bind != "swap" and bind != "slot1" and bind != "slot2" and bind != "slot3" and bind != "slot4" and bind != "slot5" and bind != "slot6" and bind != "slot7" and bind != "slot8" and bind != "slot9" and bind != "save" and bind != "load" and bind != "list" and bind != "chat" and bind != "command" and bind != "highlight" and bind != "screenshot" and bind != "cinematic" and bind != "fullscreen" and bind != "perspective":
        raise ValueError(f"unrecognized keybind: \'{bind}\'")
    return "tellraw " + selector.replace("everyone", "@a").replace("random", "@r").replace("nearest", "@p").replace(
        "self", "@s") + " {\"keybind\":\"" + bind.replace("forwards", "key.forward").replace("backwards",
                                                                                             "key.back").replace("left",
                                                                                                                 "key.left").replace(
        "right", "key.right").replace("jump", "key.jump").replace("sneak", "key.sneak").replace("sprint",
                                                                                                "key.sprint").replace(
        "inventory", "key.inventory").replace("attack", "key.attack").replace("use", "key.use").replace("pick",
                                                                                                        "key.pickItem").replace(
        "drop", "key.drop").replace("swap", "key.swapHands").replace("slot1", "key.hotbar.1").replace("slot2",
                                                                                                      "key.hotbar.2").replace(
        "slot3", "key.hotbar.3").replace("slot4", "key.hotbar.4").replace("slot5", "key.hotbar.5").replace("slot6",
                                                                                                           "key.hotbar.6").replace(
        "slot7", "key.hotbar.7").replace("slot8", "key.hotbar.8").replace("slot9", "key.hotbar.9").replace("save",
                                                                                                           "key.saveToolbarActivator").replace(
        "load", "key.loadToolbarActivator").replace("list", "key.playerlist").replace("chat", "key.chat").replace(
        "command", "key.command").replace("highlight", "key.spectatorOutines").replace("screenshot",
                                                                                       "key.screenshot").replace(
        "cinematic", "key.smoothCamera").replace("fullscreen", "key.fullscreen").replace("perspective",
                                                                                         "key.togglePerspective") + "\", \"color\":\"" + color + "\", \"bold\":" + str(
        bold).lower() + ", \"italic\":" + str(italic).lower() + ", \"underlined\":" + str(
        underline).lower() + ", \"strikethrough\":" + str(strike).lower() + ", \"obfuscated\":" + str(
        obfuscated).lower() + "}"


def CombineTellraw(selector, *tellraws):
    if type(selector) is not str:
        raise ArgTypeError("CombineTellraw", selector, 1, str)
    selector = selector.lower()
    if selector != "everyone" and not selector.startswith("@a") and selector != "random" and not selector.startswith(
            "@r") and selector != "nearest" and not selector.startswith(
            "@p") and selector != "self" and not selector.startswith("@s"):
        raise ValueError(f"unrecognized selector: \'{selector}\'")

    output = "tellraw " + selector.replace("everyone", "@a").replace("random", "@r").replace("nearest", "@p").replace(
        "self", "@s") + " [\"\""
    for tellraw in tellraws:
        for charnum, char in enumerate(tellraw):
            if char == "{":
                output += ", " + tellraw[charnum:]
                break
    return output + "]"