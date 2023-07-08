from dotenv import load_dotenv, find_dotenv
from datetime import timedelta, date, datetime
import os
import sys
import time
import logging
logger = logging.getLogger(__name__)
load_dotenv(find_dotenv(), verbose=True)
libs = r''.join([os.getcwd(), r'\lib\instantclient_19_9'])

try:
    import cx_Oracle
    cx_Oracle.init_oracle_client(lib_dir=libs)
except ImportError:
    logger.info("No cx_Oracle module available.\nTo install, run:\n"
                "\tpip install cx_Oracle")
    sys.exit(1)




class DBConnection():
    __connection = None
    __cursorobj = None

    DB_MODE = os.getenv("DB_MODE")
    if DB_MODE == 'TEST':
        DB_IP = os.getenv("DB_IP_TEST")
        DB_PORT = os.getenv("DB_PORT_TEST")
        DB_SID = os.getenv("DB_SID_TEST")
        DB_LOGIN = os.getenv("E2C_db_login_test")
        DB_PASS = os.getenv("E2C_db_password_test")
    elif DB_MODE == 'PROD':
        DB_IP = os.getenv("DB_IP_prod")
        DB_PORT = os.getenv("DB_PORT_prod")
        DB_SID = os.getenv("DB_SID_prod")
        DB_LOGIN = os.getenv("E2C_db_login_prod")
        DB_PASS = os.getenv("E2C_db_password_prod")
    elif DB_MODE == 'UNION':
        DB_IP_BUSTER = os.getenv("DB_IP_BUSTER")
        DB_PORT_BUSTER = os.getenv("DB_PORT__BUSTER")
        DB_SID_BUSTER = os.getenv("DB_SID_BUSTER")
        DB_LOGIN_BUSTER = os.getenv("DB_LOGIN_BUSTER")
        DB_PASS_BUSTER = os.getenv("DB_PASS_BUSTER")
    else:
        raise Exception(
            'Select the DB in .env file. Either TEST or PROD. Example: DB_MODE=TEST')
    DB_IP_SVFE = os.getenv("SVFE_DB_IP")
    DB_PORT_SVFE = os.getenv("SVFE_DB_PORT")
    DB_SID_SVFE = os.getenv("SVFE_DB_SID")
    DB_LOGIN_SVFE = os.getenv("svfe_db_login")
    DB_PASS_SVFE = os.getenv("svfe_db_password")


    def __init__(self, DB:str):
        if DB == 'E2C':
            self._ip = self.DB_IP
            self._port = self.DB_PORT
            self._SID = self.DB_SID
            self._login = self.DB_LOGIN
            self._passwd = self.DB_PASS

        elif DB == 'SVFE':
            self._ip = self.DB_IP_SVFE
            self._port = self.DB_PORT_SVFE
            self._SID = self.DB_SID_SVFE
            self._login = self.DB_LOGIN_SVFE
            self._passwd = self.DB_PASS_SVFE
        
        elif DB == 'BUSTER':
            self._ip = self.DB_IP_BUSTER
            self._port = self.DB_PORT_BUSTER
            self._SID = self.DB_SID_BUSTER
            self._login = self.DB_LOGIN_BUSTER
            self._passwd = self.DB_PASS_BUSTER


    def connect(self) -> None:
        if self.__connection is None:
            dsn_tns = cx_Oracle.makedsn(self._ip, self._port, self._SID)
            try:
                logger.info('-------------------------------------------------------')
                logger.info('Program create connection with DB:')
                logger.info('-------------------------------------------------------')
                
                logger.info('Trying to connect to: {}'.format(
                    ''.join([str(self._SID), '@', self._ip, ':', str(self._port)])))
                self.__connection = cx_Oracle.connect(
                    self._login, self._passwd, dsn_tns, encoding="UTF8")
                self.__cursorobj = self.__connection.cursor()
            except cx_Oracle.DatabaseError:
                sys.stderr.write(
                    "Unable to connect (server: {0}; SID: {1}; login: {2}): {3}\n".format(self._ip,self._SID,self._login,sys.exc_info()[1]))
                sys.exit(1)
            else:
                logger.info('Connection establised.')

    def query(self, query:str) -> None:
        try:
            return self.__cursorobj.execute(query)
        except cx_Oracle.DatabaseError as exc:
            with open("..\\Sheduler\\error.csv", 'a', encoding='utf-8') as fp1:
                writer = fp1.write(str(query))
            error, = exc.args
            print(error.message)
#            logger.info("		Oracle-Query-String: %s" % query)
            logger.error("		Oracle-Error-Code: %s" % error.code)
            logger.error("		Oracle-Error-Message: %s" % error.message)
            exit(1)
