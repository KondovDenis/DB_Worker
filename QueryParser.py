import Sheduler
import logging
from strenum import StrEnum
from EnumsType import FormatType
from collections.abc import Generator






class QueryParser:

    data_type = None

    def __init__(self, query: list):
        self.query = query
    

    def extract_data(self) -> list[str]:
        ''' Extract date  from SQL query '''
        logging.info('Extracting date from SQL query.')
        array = self.query[0].split(' ')
        new_arr = list(filter(lambda x: x != '', array))
        if 'between' in new_arr:
            index = new_arr.index('between')
            self.data_type = str(new_arr[index+3] + ' ' + new_arr[index+4].replace(')','').replace('r','').replace('n','').replace('/','').strip().rstrip('\''))
            self.data_type = self.data_type.replace(self.data_type[0],'')
            if self.data_type == FormatType.FORMAT1:
                data1 = new_arr[index+1] + ' ' + new_arr[index+2] + new_arr[index+3] + ' ' + new_arr[index+4].replace('r','').replace('n','').replace('/','').strip()
                data2 = new_arr[index+6] + ' ' + new_arr[index+7] + new_arr[index+8] + ' ' + new_arr[index+9].replace('r','').replace('n','').replace('/','').strip()
                data2 = data2[:len(data1)]
                return [data1, data2[:len(data1)]]
            self.data_type = str(new_arr[index+2].replace(')','').replace('r','').replace('n','').replace('/','').strip().rstrip('\''))
            self.data_type = self.data_type.replace(self.data_type[0],'')
            if self.data_type == FormatType.FORMAT2:
                data1 = new_arr[index+1] + ' ' + new_arr[index+2]
                data2 = new_arr[index+4].replace('r','').replace('n','').replace('/','').strip()  + ' ' + new_arr[index+5].replace('r','').replace('n','').replace('/','').strip() 
                return [data1, data2[:len(data1)]]

    
    def split_data_in_query_on_periods(self, date_beetwen_dates:list[str]) -> Generator[str]:
        ''' Generator function split date inside query on days and return  query in string format with period - day '''
        logging.info('Split date inside query SQL query.')
        array = self.query[0].split(' ')
        new_arr = list(filter(lambda x: x != '', array))
        if 'between' in new_arr:
            index = new_arr.index('between')
            self.data_type = str(new_arr[index+3] + ' ' + new_arr[index+4].replace(')','').replace('r','').replace('n','').replace('/','').strip().rstrip('\''))
            self.data_type = self.data_type.replace(self.data_type[0],'')

            if self.data_type == FormatType.FORMAT1:
                del new_arr[index+2:index+7]
                if new_arr[index+4] == "HH24:MI:SS')" or new_arr [index+4] == "yyyy-mm-dd')":
                    del new_arr[index+4]

                for item  in range(len(date_beetwen_dates)-1):
                    new_arr[index+1] = f"""to_date('{date_beetwen_dates[item]}', '{FormatType.FORMAT1}')\r\n"""
                    new_arr[index+2] = f' and '
                    new_arr[index+3] = f"""to_date('{date_beetwen_dates[item+1]}', '{FormatType.FORMAT1}')\r\n"""
                    new_arr[index+4] = new_arr[index+4].replace(r"HH24:MI:SS')\r\n", '').replace(r"yyyy-mm-dd')\r\n", '').replace(r'HH24:MI:SS")', '').replace(r"HH24:MI:SS)", '')
                    new_arr[index+4] = new_arr[index+4].split()[1] if len (new_arr[index+4].split()) > 1  else  new_arr[index+4].split()[0]
                    sql = ' '.join(new_arr)
                    yield sql

            self.data_type = str(new_arr[index+2].replace(')','').replace(r'\r','').replace(r'\n','').replace('/','').strip().rstrip('\''))
            self.data_type = self.data_type.replace(self.data_type[0],'')
            
            if self.data_type == FormatType.FORMAT2:
                del new_arr[index+2:index+7]
                if new_arr [index+3] == "yyyy-mm-dd')":
                    del new_arr[index+3]

                for item  in range(len(date_beetwen_dates)-1):
                    new_arr[index+1] = f"""to_date('{date_beetwen_dates[item].replace("'", '"')}', '{FormatType.FORMAT2}')\r\n""".replace(' 00:00:00','')
                    new_arr[index+2] = f' and '
                    new_arr[index+3] = f"""to_date('{date_beetwen_dates[item+1].replace("'", '"')}', '{FormatType.FORMAT2}')\r\n""".replace(' 00:00:00','')
                    sql = ' '.join(new_arr)
                    yield sql



