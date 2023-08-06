from bot_common.sessions.session_model import SessionObject, session_headers as headers
from bot_common.utils.db_utils import DbConfig, create_table_if_not_exists, db_connect, update_table
from bot_common.utils.utils import catch_exception, get_time_now, clean_string
from bot_common.utils.logging_conf import logger
from bot_common.lib_conf import table_prefix_sessions
from typing import List, Union
import json

# - In "cache" we store some cached_variables for the backend logic
#   and the printable_variables for the responses.
# - In "other_logs" we store some indicators about the performed
#   conversational flow path.
# - In "extracted_data" we store the main features extracted
#   during the conversation.

int_fields = ['timeout_sec', 'bot_message_contains_buttons', 'unclosed_success', 'solicited_times', 'is_closed']
dump_fields = ['cache', 'entities', 'other_logs', 'extracted_data']
str_special_char_fields = ['bot_message']
clean_str_fields = []
float_fields = []


class Session(SessionObject):
    @catch_exception
    def extract_data(self):
        data = self.__dict__.copy()
        data['timestamp'] = get_time_now()
        for field in dump_fields:
            data[field] = clean_string(json.dumps(data[field])).replace('\\', '\\\\')
        for field in str_special_char_fields:
            data[field] = data[field].replace("\\", "\\\\").replace("'", "\\'")
        for field in int_fields:
            data[field] = int(data[field])
        for field in clean_str_fields:
            data[field] = clean_string(data[field])
        for field in float_fields:
            data[field] = round(float(data[field]), 2)
        return data

    @catch_exception
    def set(self, db_config: DbConfig):
        tab_name = table_prefix_sessions + self.company
        session_db, session_cursor = db_connect(db_config)
        create_table_if_not_exists(session_db, session_cursor, tab_name, headers)
        data_dict = self.extract_data()
        update_table(session_db, session_cursor, data_dict, tab_name)
        logger.info(f'set session {self.id_session} success')
        session_db.close()

    @catch_exception
    def delete(self, db_config: DbConfig):
        tab_name = table_prefix_sessions + self.company
        session_db, session_cursor = db_connect(db_config)
        create_table_if_not_exists(session_db, session_cursor, tab_name, headers)
        delete_session_query = f"DELETE FROM {tab_name} WHERE id_session = '{self.id_session}';"
        session_cursor.execute(delete_session_query)
        session_db.commit()
        logger.info(f'delete session {self.id_session} success')
        session_db.close()

    @catch_exception
    def close(self, db_config: DbConfig):
        tab_name = table_prefix_sessions + self.company
        session_db, session_cursor = db_connect(db_config)
        create_table_if_not_exists(session_db, session_cursor, tab_name, headers)
        data_dict = self.extract_data()
        data_dict['is_closed'] = 1
        update_table(session_db, session_cursor, data_dict, tab_name)
        logger.info(f'close session {self.id_session} success')
        session_db.close()


class SessionGet:
    @catch_exception
    def __init__(self, company: str, db_config: DbConfig):
        self.company = company
        self.tab_name = table_prefix_sessions + company
        self.session_db, self.session_cursor = db_connect(db_config)
        create_table_if_not_exists(self.session_db, self.session_cursor, self.tab_name, headers)

    @catch_exception
    def single(self, session_id: str) -> Union[Session, None]:
        get_session_query = f"SELECT * FROM {self.tab_name} WHERE id_session = '{session_id}';"
        self.session_cursor.execute(get_session_query)
        myresult = self.session_cursor.fetchall()
        self.session_db.close()
        if not myresult:
            logger.info(f"session ({session_id}) not found")
            return None
        # myresult[0][1:] because we need to remove the pk auto_increment element
        out_dict = dict(zip(list(headers.keys()), myresult[0][1:]))
        for field in dump_fields:
            out_dict[field] = json.loads(out_dict[field])
        return Session.parse_obj(out_dict)

    @catch_exception
    def existing_all(self) -> List[Session]:
        get_existing_sessions_query = f"SELECT * FROM {self.tab_name};"
        self.session_cursor.execute(get_existing_sessions_query)
        myresult = self.session_cursor.fetchall()
        self.session_db.close()
        parsed_out = []
        for res in myresult:
            # res[1:] is needed to remove the pk auto_increment key
            parsed_dict = dict(zip(list(headers.keys()), res[1:]))
            for field in dump_fields:
                parsed_dict[field] = json.loads(parsed_dict[field])
            parsed_obj = Session.parse_obj(parsed_dict)
            parsed_out.append(parsed_obj)
        return parsed_out

    @catch_exception
    def delete_table(self):
        delete_sessions_table_query = f"DROP TABLE {self.tab_name};"
        self.session_cursor.execute(delete_sessions_table_query)
        self.session_db.commit()
        logger.info(f'drop table {self.tab_name} success')
        self.session_db.close()
