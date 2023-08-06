import typing

class VLPError(Exception):
    pass

class VLPTypeError(VLPError):
    def __init__(self, value, *typeargv:type):
        self._value = value
        self._type = [str(i).split("\'")[1] for i in list(typeargv)]
    
    def __str__(self):
        s = str(type(self._value)).split("\'")[1]
        return repr(f"the value must be of type {self._type}, but this value is of type {s}.")

class VLPSequenceLenError(VLPError):
    def __init__(self,value:typing.Sequence,length:int):
        self._value = value
        self._len = length
    def __str__(self) -> str:
        return repr(f"the length of the Sequence has to be {self._len}, but this Sequence has length {len(self._value)}.")


class VLPValueError(VLPError):
    def __init__(self,value,*argv):
        self._value = value
        self._argv = list(argv)
    def __str__(self) -> str:
        return repr(f"The value {self._value} is not in {self._argv}.")
 

class VLPValueRangeError(VLPError):
    def __init__(self,value,low,hignt):
        self._value = value
        self._range = (low,hignt)
    def __str__(self) -> str:
        return repr(f"The value {self._value} must be in the range {self._range}.")



