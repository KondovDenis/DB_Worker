import csv
import logging
from DBConnection import DBConnection
from QueryParser import QueryParser
from Sheduler import Sheduler
from EnumsType import FormatType
from collections.abc import Generator





class WorkerDB:

    def __init__(self):
        super().__init__()
        self.__db_app = DBConnection(DB='E2C')
        self.__db_app.connect()
        # self.__db_svfe = DBConnection(DB='SVFE')
        # self.__db_svfe.connect()


    def query_generator(self) -> Generator[str]:
        '''Call all method for build sql-query'''
        s = Sheduler()
        period = s.get_period()
        query = s.get_all_query_sql()
        q = QueryParser(query)
        date = q.extract_data()
        dates = s.get_date_list(date)
        new_query = q.split_data_in_query_on_periods(dates)
        yield new_query

    def sync_execute_sql(self):
        '''Send sql-query to DB and write result in .csv file'''
#       try:
        for sql in next(self.query_generator()):
            logging.info("Generating SQL query.")
            logging.info("Sending SQL query.")
            print("Sending SQL query:")
            print("---------------------------------------------------")
            print(sql)
            print("---------------------------------------------------")
            result = self.__db_app.query(str(sql))
            columns = [col[0] for col in result.description]
            result.rowfactory = lambda *args: dict(zip(columns, args))
            for row in result:
                values = dict(row).values()
                with open("..\\Sheduler\\result.csv", 'a', encoding='utf-8') as fp:
                    writer = fp.write(';'.join(map(str,values))+'\r\n')
#        except Exception as exc:
#            with open("..\\Sheduler\\error.csv", 'a', encoding='utf-8') as fp1:
#                writer = fp1.write(str(query))
#            error, = exc.args
#            print(error.message) 
#            logger.error("		Error-Code: %s" % error.code)
#            logger.error("		Error-Message: %s" % error.message)