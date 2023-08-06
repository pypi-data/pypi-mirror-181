def ArgTypeError(function, argument, pos, *maintypes):
    if type(function) is not str:
        raise TypeError(f"ArgTypeError expected str, not {repr(type(function))[8:-2]} (pos 1)")
    if type(pos) is not int:
        raise TypeError(f"ArgTypeError expected int, not {repr(type(function))[8:-2]} (pos 3)")
    length = len(maintypes)
    if length == 1:
        return TypeError(f"{function} expected {repr(maintypes[0])[8:-2]}, not {repr(type(argument))[8:-2]} (pos {str(pos)})")
    elif length > 1:
        error = f"{function} expected "
        for value, maintype in enumerate(maintypes):
            if value == 0:
                error += f"{repr(maintype)[8:-2]}"
            elif value + 1 == length:
                if length == 2:
                    error += f" or {repr(maintype)[8:-2]}"
                else:
                    error += f", or {repr(maintype)[8:-2]}"
            else:
                error += f", {repr(maintype)[8:-2]}"
        error += f", not {repr(type(argument))[8:-2]} (pos {str(pos)})"
        return TypeError(error)
    else:
        raise TypeError("ArgTypeError missing required argument \'maintypes\' (pos 4)")