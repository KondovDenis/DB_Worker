#!python

import logging
from QueryParser import QueryParser
from Sheduler import Sheduler
from EnumsType import FormatType
from WorkerDB import WorkerDB


def main():
    logging.basicConfig(level=logging.INFO, filename="..\\Sheduler\\logs\\out.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
    logging.info("Start process....")
    worker = WorkerDB()
    worker.sync_execute_sql()


if __name__ == '__main__':
    main()
