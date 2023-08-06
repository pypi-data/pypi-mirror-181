from bot_common.exceptions.exception_model import ExceptionObj, exception_headers as headers
from bot_common.utils.utils import catch_exception, get_time_now, clean_string, validate_time, datetime_to_str
from bot_common.utils.db_utils import DbConfig, create_table_if_not_exists, db_connect, insert_into_table
from bot_common.utils.logging_conf import logger
from bot_common.lib_conf import table_name_exceptions
from typing import List
import json

int_fields = []
clean_str_fields = ['error_message']


class ExceptionSession(ExceptionObj):
    def extract_data(self):
        data = self.__dict__.copy()
        data['timestamp'] = self.timestamp if validate_time(self.timestamp) else get_time_now()
        for field in int_fields:
            data[field] = int(data[field])
        for field in clean_str_fields:
            data[field] = clean_string(data[field])
        return data

    @catch_exception
    def write(self, db_config: DbConfig):
        tab_name = table_name_exceptions
        session_db, session_cursor = db_connect(db_config)
        create_table_if_not_exists(session_db, session_cursor, tab_name, headers)
        data_dict = self.extract_data()
        insert_into_table(session_db, session_cursor, data_dict, tab_name)
        logger.info(f'Writing exception success')
        session_db.close()


class ExceptionManager:
    @catch_exception
    def __init__(self, tmp: str, db_config: DbConfig):
        self.tmp = tmp
        self.tab_name = table_name_exceptions
        self.session_db, self.session_cursor = db_connect(db_config)
        create_table_if_not_exists(self.session_db, self.session_cursor, self.tab_name, headers)

    @catch_exception
    def delete(self):
        delete_session_query = f"DELETE FROM {self.tab_name} WHERE timestamp <= '{self.tmp}';"
        self.session_cursor.execute(delete_session_query)
        self.session_db.commit()
        logger.info(f'delete exceptions success')
        self.session_db.close()

    @catch_exception
    def get(self) -> List[ExceptionObj]:
        get_session_query = f"SELECT * FROM {self.tab_name} WHERE timestamp <= '{self.tmp}' ORDER BY timestamp DESC;"
        self.session_cursor.execute(get_session_query)
        myresult = self.session_cursor.fetchall()
        self.session_db.close()
        out_ls = []
        for res in myresult:
            # res[1:] because we need to remove the pk auto_increment element
            out_dict = dict(zip(headers, res[1:]))
            out_dict['timestamp'] = datetime_to_str(out_dict['timestamp'])
            out_ls.append(ExceptionObj.parse_obj(out_dict))
        return out_ls
