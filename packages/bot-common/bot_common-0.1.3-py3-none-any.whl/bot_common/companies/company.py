from bot_common.companies.company_model import config_headers as headers
from bot_common.utils.utils import catch_exception, get_time_now
from bot_common.utils.db_utils import DbConfig, db_connect, create_table_if_not_exists
from bot_common.utils.logging_conf import logger
from bot_common.lib_conf import table_name_company_configurations, table_prefix_conversational_flow, table_prefix_responses
from pydantic import BaseModel
import json
import pandas as pd


@catch_exception
def dict_parser(d: dict):
    parsed_dict = dict()
    for key, val in d.items():
        try:
            val_p = json.loads(val) if isinstance(val, str) else val
        except json.JSONDecodeError:
            val_p = val
        parsed_dict[key] = val_p
    return {k: v for k, v in parsed_dict.items() if v is not None}


class GenericObj(BaseModel):
    def __init__(self, d: dict):
        self.__dict__.update(dict_parser(d))


class Company:
    def __init__(self, field: str, value, db_config: DbConfig):
        self.field = field
        self.value = value
        self.tab_name = table_name_company_configurations
        self.db, self.cursor = db_connect(db_config)
        create_table_if_not_exists(self.db, self.cursor, self.tab_name, headers)

    @catch_exception
    def get_config(self, opened=True):
        where_active_field = 'AND is_active = 1' if opened else ''
        get_config_query = f"SELECT * FROM {self.tab_name} WHERE {self.field} LIKE '%{self.value}%' {where_active_field};"
        self.cursor.execute(get_config_query)
        conf_vals = self.cursor.fetchall()
        if not conf_vals:
            self.db.close()
            raise Exception(f'get company configuration - {self.field} {self.value} not found')
        elif len(conf_vals) > 1:
            self.db.close()
            raise Exception(f'get company configuration - {self.field} {self.value} ambiguous or duplicated')

        # get config structure
        get_structure_query = f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self.tab_name}' ORDER BY ordinal_position;"
        self.cursor.execute(get_structure_query)
        structure = self.cursor.fetchall()
        self.db.close()
        # flatten the structure list
        structure = list(sum(structure, ()))
        # remove duplicates from structure_result while keeping the order
        structure = list(dict.fromkeys(structure))
        config_dict = dict(zip(structure[1:], conf_vals[0][1:]))
        return GenericObj(config_dict)

    @catch_exception
    def delete_config(self):
        get_config_query = f"SELECT company FROM {self.tab_name} WHERE {self.field} LIKE '%{self.value}%';"
        self.cursor.execute(get_config_query)
        conf_vals = self.cursor.fetchall()
        if not conf_vals:
            self.db.close()
            raise Exception(f'delete company configuration - {self.field} {self.value} not found')
        elif len(conf_vals) > 1:
            self.db.close()
            raise Exception(f'delete company configuration - {self.field} {self.value} ambiguous or duplicated')

        company = conf_vals[0][0]
        delete_config_query = f"DELETE FROM {self.tab_name} WHERE {self.field} LIKE '%{self.value}%';"
        delete_flow_query = f"DROP TABLE {table_prefix_conversational_flow}{company}"
        delete_responses_query = f"DROP TABLE {table_prefix_responses}{company}"
        self.cursor.execute(delete_config_query)
        self.db.commit()
        self.cursor.execute(delete_flow_query)
        self.db.commit()
        self.cursor.execute(delete_responses_query)
        self.db.commit()
        logger.info(f'>> deleted configuration for company {company}')
        self.db.close()


class CompanyManager:
    def __init__(self, db_config: DbConfig):
        self.tab_name = table_name_company_configurations
        self.db, self.cursor = db_connect(db_config)
        create_table_if_not_exists(self.db, self.cursor, self.tab_name, headers)

    @catch_exception
    def get_companies(self, opened: bool = True):
        where_active_field = 'WHERE is_active = 1' if opened else ''
        get_companies_query = f"SELECT company FROM {self.tab_name} {where_active_field};"
        self.cursor.execute(get_companies_query)
        companies = self.cursor.fetchall()
        self.db.close()
        return [el[0] for el in companies]

    @catch_exception
    def disable_company(self, company: str):
        get_company_query = f"SELECT company FROM {self.tab_name} WHERE company = '{company}';"
        self.cursor.execute(get_company_query)
        if not self.cursor.fetchall():
            self.db.close()
            raise Exception(f'disable company - {company} not found')

        disable_config_query = f"UPDATE {self.tab_name} SET is_active = 0, is_active_switch_tmp = '{get_time_now()}' WHERE company = '{company}';"
        self.cursor.execute(disable_config_query)
        self.db.commit()
        logger.info(f'>> disabled {company} company')
        self.db.close()

    @catch_exception
    def activate_company(self, company: str):
        get_company_query = f"SELECT company FROM {self.tab_name} WHERE company = '{company}';"
        self.cursor.execute(get_company_query)
        if not self.cursor.fetchall():
            self.db.close()
            raise Exception(f'activate company - {company} not found')

        activate_config_query = f"UPDATE {self.tab_name} SET is_active = 1, is_active_switch_tmp = '{get_time_now()}' WHERE company = '{company}';"
        self.cursor.execute(activate_config_query)
        self.db.commit()
        logger.info(f'>> activated {company} company')
        self.db.close()


class CompanyTables:
    def __init__(self, db_config: DbConfig, company: str):
        self.company = company
        self.tab_name = ''
        self.db, self.cursor = db_connect(db_config)

    @catch_exception
    def get_flow_filtered_by_input_ctx(self, in_ctx: str):
        self.tab_name = table_prefix_conversational_flow + self.company
        get_table_query = f"SELECT * FROM {self.tab_name} WHERE in_ctx = '{in_ctx}';"
        df = pd.read_sql(get_table_query, self.db)
        self.db.close()
        df = df.drop(columns=['pk'])
        if len(df) == 0:
            raise Exception(f'Invalid input context {in_ctx}')
        return df

    @catch_exception
    def get_responses_csv(self):
        self.tab_name = table_prefix_responses + self.company
        get_table_query = f"SELECT * FROM {self.tab_name};"
        df = pd.read_sql(get_table_query, self.db)
        self.db.close()
        return df.drop(columns=['pk'])
