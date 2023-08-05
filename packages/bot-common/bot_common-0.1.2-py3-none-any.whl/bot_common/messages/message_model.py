from pydantic import BaseModel


class DmMessageLightObj(BaseModel):
    session_id: str
    company_contact: str


class NewMessageDbObj(BaseModel):
    company_contact: str
    user_contact: str
    user_key: str = ''
    user_message: str = ''
    start_context: str = ''
    token: str = ''


class MessageDbObj(BaseModel):
    company_contact: str
    user_contact: str
    timestamp: str
    processed: int
    user_message: str
    start_context: str
    user_key: str


# '<U_IDX>' flags all the fields that cannot be simultaneously duplicated,
# '<IDX>' flags all the fields that are used in the queries
message_headers = {
    'company_contact': 'VARCHAR(250) NOT NULL <U_IDX>',
    'user_contact': 'VARCHAR(250) NOT NULL <U_IDX>',
    'timestamp': 'VARCHAR(50) NOT NULL <U_IDX>',
    'processed': 'TINYINT NOT NULL <IDX>',
    'user_message': 'TEXT',
    'start_context': 'TEXT',
    'user_key': 'TEXT',
    }
