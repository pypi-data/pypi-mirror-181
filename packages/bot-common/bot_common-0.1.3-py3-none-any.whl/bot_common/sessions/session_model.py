from pydantic import BaseModel


class SessionObject(BaseModel):
    id_session: str
    is_closed: int = 0
    company: str
    company_contact: str
    start_conversation_timestamp: str
    user_key: str = ''
    start_context: str = ''
    current_context: str = ''
    state: str = ''
    timestamp: str = ''
    timeout_sec: int = 0
    bot_message_contains_buttons: bool = False
    unclosed_success: bool = False
    solicited_times: int = 0
    message_id: str = ''
    bot_message: str = ''
    other_logs: dict = {}
    extracted_data: dict = {}
    cache: dict = {}
    entities: dict = {}


# '<U_IDX>' flags all the fields that cannot be simultaneously duplicated,
# '<IDX>' flags all the fields that are used in the queries
session_headers = {'id_session': 'VARCHAR(250) NOT NULL <U_IDX>',
                   'is_closed': 'TINYINT NOT NULL <IDX>',
                   'company': 'TEXT NOT NULL',
                   'company_contact': 'TEXT NOT NULL',
                   'user_key': 'TEXT',
                   'start_context': 'TEXT',
                   'current_context': 'TEXT',
                   'state': 'TEXT',
                   'start_conversation_timestamp': 'VARCHAR(50)',
                   'timestamp': 'VARCHAR(50)',
                   'timeout_sec': 'TINYINT',
                   'bot_message_contains_buttons': 'TINYINT',
                   'unclosed_success': 'TINYINT',
                   'solicited_times': 'TINYINT',
                   'message_id': 'TEXT',
                   'bot_message': 'TEXT',
                   'other_logs': 'TEXT',
                   'extracted_data': 'TEXT',
                   'cache': 'TEXT',
                   'entities': 'TEXT'
                   }
