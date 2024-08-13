from utility import prompts

"""
"gpt-3.5-turbo-0125"
"gpt-4-turbo"
"gpt-4o"
"""
_model = "gpt-4o"

"""
Batch Mode Settings
"""
_batchAPI_method = 'POST'
_batchAPI_endpoint = "/v1/chat/completions"
_batchAPI_completion_window = '24h'
_batchAPI_description = 'Batch Job: Extraction Accounting Standards'

"""
Min. term occurrence ratio
"""
_min_ratio = .4

"""
Few shot settings
"""
_flag_incl_sentence = True
_flag_incl_doc_entity = True
_flag_user_assistant = True
_flag_segmented = False # legacy remove later across files
_flag_ext_examples = True

"""
Segmentation Settings
"""
_max_token_num = 15_900
_overlay = 200

"""
Schedule
"""
_schedule_batch_size = 100

"""
Maximum tokens allowed per example
"""
_max_tokens_allowed = 16000

"""
GPT Prompting Settings
"""
_gpt_answer_keys = ['doc', 'sentence', 'term']

_prompt_system = prompts.system_context_basic1
_prompt_instructions = [prompts.task_descr_auditor_12, prompts.instruction_6, prompts.answer_format_split_4]
#_prompt_instructions = [prompts.task_descr_notes_5, prompts.instruction_6, prompts.answer_format_split_4]