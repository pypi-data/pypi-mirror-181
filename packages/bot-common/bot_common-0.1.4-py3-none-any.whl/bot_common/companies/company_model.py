from pathlib import Path
from pydantic import BaseModel


class ConfigPaths(BaseModel):
    config_file_path: Path
    flow_path: Path
    responses_path: Path


# '<U_IDX>' flags all the fields that cannot be simultaneously duplicated,
# '<IDX>' flags all the fields that are used in the queries
flow_headers = {
                'in_ctx': 'VARCHAR(250) NOT NULL <U_IDX> <IDX>',
                'intent': 'VARCHAR(250) <U_IDX>',
                'entity': 'VARCHAR(250) <U_IDX>',
                'action': 'TEXT',
                'action_out': 'VARCHAR(250) <U_IDX>',
                'out_ctx': 'TEXT NOT NULL',
                'response_id': 'TEXT NOT NULL',
                'response_id_fallback': 'TEXT',
                'hints': 'TEXT',
                'timeout_sec': 'INT',
                'call_reason': 'TEXT'
                }

responses_headers = {'id': 'VARCHAR(250) NOT NULL <U_IDX> <IDX>',
                     'body1': 'TEXT',
                     'body2': 'TEXT',
                     'body3': 'TEXT',
                     'body4': 'TEXT',
                     'body5': 'TEXT'
                     }

config_headers = {
                  'company': 'VARCHAR(250) NOT NULL <U_IDX> <IDX>',
                  'is_active': 'TINYINT NOT NULL <IDX>',
                  'is_active_switch_tmp': 'VARCHAR(50)',
                  'company_port': 'INT NOT NULL',
                  'company_contact': 'VARCHAR(250) NOT NULL <IDX>',
                  'used_conversation_platform': 'TEXT',
                  'redirect_contacts': 'TEXT',
                  'nlu_port': 'INT NOT NULL',
                  'sessions_expiration_mins': 'INT',
                  'unexisting_session_start_ctx': 'TEXT',
                  'preferred_nlu_extractor': 'TEXT',
                  'default_timeout_sec': 'INT',
                  'fallback_counter_max': 'INT',
                  'technical_issue_response_id': 'TEXT',
                  'session_expired_response_id_by_start_ctx': 'TEXT',
                  'handover_incomprehension_response_id': 'TEXT',
                  'end_conversation_formalities_intents': 'TEXT',
                  'preprocessing_messages_contexts': 'TEXT',
                  'preprocessing_messages_bodies': 'TEXT',
                  'hints_mapping': 'TEXT',
                  'solicit_after_mins': 'TEXT',
                  'solicit_action_ls': 'TEXT',
                  'success_other_logs': 'TEXT',
                  'other': 'TEXT'
                  }


