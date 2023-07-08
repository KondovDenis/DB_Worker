from strenum import StrEnum




class FormatType(StrEnum):
    FORMAT1 = "YYYY-MM-DD HH24:MI:SS"
    FORMAT2 = "yyyy-mm-dd"




class Params(StrEnum):
#    ASYNC = '--async' 
    SYNCHRO = '--synchro'
    WEEK = '--week'
    DAY = '--day'