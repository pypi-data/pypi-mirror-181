from pydantic import BaseModel


class TimeoutObj(BaseModel):
    company_contact: str
    user_contact: str
    timestamp: str = ""
    timeout_sec: int = 0


# '<U_IDX>' flags all the fields that cannot be simultaneously duplicated,
# '<IDX>' flags all the fields that are used in the queries
timeout_headers = {
    'company_contact': 'VARCHAR(250) NOT NULL <U_IDX>',
    'user_contact': 'VARCHAR(250) NOT NULL <U_IDX>',
    'timestamp': 'VARCHAR(50)',
    'timeout_sec': 'INT',
    }
