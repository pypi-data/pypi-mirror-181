from pydantic import BaseModel


class LogObject(BaseModel):
    id_session: str
    company: str
    company_contact: str
    user_key: str = ""
    start_context: str = ""
    current_context: str = ""
    conversation_platform: str = ""
    start_conversation_timestamp: str = ""
    timestamp: str = ""
    conv_duration_sec: int = 0
    detected_intent: str = ""
    intent_confidence: float = 0
    conv_step_num: int = 0
    closed_formality: bool = False
    unclosed_success: bool = False
    solicit: bool = False
    fallback: bool = False
    handover: bool = False
    handover_incomprehension: bool = False
    closed: bool = False
    hangup: bool = False
    redirect: bool = False
    expired: bool = False
    state: str = ""
    message_id: str = ""
    bot_message: str = ""
    current_user_utterance: str = ""
    log_transcript: str = ""
    other_logs: dict = {}
    extracted_data: dict = {}


# '<U_IDX>' flags all the fields that cannot be simultaneously duplicated,
# '<IDX>' flags all the fields that are used in the queries
log_headers = {'timestamp': 'DATETIME(6) NOT NULL <U_IDX>',
               'id_session': 'VARCHAR(250) NOT NULL <U_IDX>',
               'company': 'VARCHAR(250) NOT NULL <IDX>',
               'company_contact': 'VARCHAR(250) NOT NULL <IDX>',
               'user_key': 'VARCHAR(250) <IDX>',
               'start_context': 'VARCHAR(250) <IDX>',
               'current_context': 'TEXT',
               'conversation_platform': 'VARCHAR(50)',
               'start_conversation_timestamp': 'VARCHAR(50)',
               'conv_duration_sec': 'INT',
               'detected_intent': 'TEXT',
               'intent_confidence': 'DOUBLE(3,2)',
               'conv_step_num': 'TINYINT <IDX>',
               'closed_formality': 'TINYINT <IDX>',
               'unclosed_success': 'TINYINT <IDX>',
               'solicit': 'TINYINT <IDX>',
               'fallback': 'TINYINT <IDX>',
               'handover': 'TINYINT <IDX>',
               'handover_incomprehension': 'TINYINT <IDX>',
               'closed': 'TINYINT <IDX>',
               'hangup': 'TINYINT <IDX>',
               'redirect': 'TINYINT <IDX>',
               'expired': 'TINYINT <IDX>',
               'state': 'VARCHAR(250)',
               'message_id': 'TEXT',
               'bot_message': 'TEXT',
               'current_user_utterance': 'TEXT',
               'log_transcript': 'TEXT',
               'other_logs': 'TEXT',
               'extracted_data': 'TEXT',
               }
