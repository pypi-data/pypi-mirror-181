from pydantic import BaseModel


class ExceptionObj(BaseModel):
    timestamp: str = ''
    state: str = ''
    error_message: str = ''


# '<U_IDX>' flags all the fields that cannot be simultaneously duplicated,
# '<IDX>' flags all the fields that are used in the queries
exception_headers = {'timestamp': 'DATETIME(6) NOT NULL <IDX>',
                     'state': 'TEXT',
                     'error_message': 'TEXT',
                     }
