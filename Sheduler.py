from DBConnection import DBConnection
from EnumsType import Params
from EnumsType import FormatType
from datetime import date, timedelta
import logging
import string
import random
import os
import sys
import datefinder







class Sheduler:

    __QUERY_PATH = 'SQL'
    __SHEDULER_FILE_PATH = os.getcwd()
    mode = Params.SYNCHRO
    period = None

    
    


    def get_all_query_sql(self) -> list[str]:
        ''' Parsing from  directory ..\SQL all *.sql and return array of querys''' 
        list_str_sql = []
        if os.path.exists(self.__QUERY_PATH):
            name_of_querys = os.listdir(self.__QUERY_PATH)
            for item in name_of_querys:
                with open(self.__SHEDULER_FILE_PATH + '\\' +  self.__QUERY_PATH + '\\' + item, 'rb') as srf:
                    _buf_query_sql_str = srf.read().decode('ANSI')
                    list_str_sql.append(_buf_query_sql_str)
        if len(list_str_sql) == 0:
            raise FileNotFoundError(f'query SQL file {file_name} not found or empty')
        return list_str_sql

    def get_execution_mode(self) -> str:
        '''Get parameters --async from terminal'''
        params = sys.argv
        self.mode = Params.SYNCHRO
        if Params.ASYNC in params:
            self.mode = Params.ASYNC
            return self.mode
        return self.mode
        

    
    def get_period(self) -> str:
        ''' Get period for share SQL query on small partition'''
        params = sys.argv
        if (Params.WEEK in params) and (Params.DAY in params):
            pass
        elif Params.WEEK in params:
            self.period = Params.WEEK
        elif Params.DAY in params:
            self.period = Params.DAY
            
        

    def get_date_list(self, date:list[str]) -> list[str]:
        ''' Get all date beetwen two dates '''
        try:
            arr_date = []
            date_beetwen_dates = []
            date1 = datefinder.find_dates(date[0].replace("'",''))
            date2 = datefinder.find_dates(date[1].replace("'",''))
            for first in date1:
                arr_date.append(first)
            for second in date2:
                arr_date.append(second)
            delta = arr_date[1] - arr_date[0]
            if self.period == Params.DAY or self.period == None:
                for i in range(delta.days + 1):
                    day = arr_date[0] + timedelta(days=i)
                    date_beetwen_dates.append(str(day))
                return date_beetwen_dates        
            elif self.period == Params.WEEK:
                for i in range(delta.days + 1):
                    day = arr_date[0] + timedelta(weeks=i)
                    date_beetwen_dates.append(str(day))
                return date_beetwen_dates
        except TypeError as e:
            print(e)
            print('')
            print("!!!!!!!!WARNING!!!!!!!! TRY TO CHECK DATE'S FORMAT. IT'S MUST BE 'yyyy-mm-dd' OR 'YYYY-MM-DD HH24:MI:SS'")        



