from utility import prompts

"""
Select OpenAI Model
"gpt-3.5-turbo-0125": 0.00025,  # gpt-3.5-turbo
"gpt-4-turbo-2024-04-09": 0.005,  # gpt-4-turbo
"gpt-4o-2024-08-06": 0.00125,  # gpt-4o
"gpt-4o-mini-2024-07-18": 0.000075,  # gpt-4o-mini
"o1-2024-12-17": 0.0075,  # o1
'o1-pro-2025-03-19': 0.075,  # o1-pro
'o1-mini-2024-09-12': 0.00055,  # o1-mini
"o3-2025-04-16": 0.001,  # o3
'o3-pro-2025-06-10': 0.01,  # o3-pro
'o3-mini-2025-01-31': 0.00055,  # o3-mini
'gpt-4.1-2025-04-14': 0.001,  # gpt-4.1
'gpt-4.1-mini-2025-04-14': 0.0002,  # gpt-4.1-mini
'gpt-4.1-nano-2025-04-14': 0.00005,  # gpt-4.1-nano
"""
_model = "gpt-4.1-2025-04-14"

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
_flag_segmented = False  # legacy remove later across files
_flag_ext_examples = True

"""
Segmentation Settings
"""
_max_token_num = 15_900
_overlay = 200  # legacy remove later across files

"""
Schedule
"""
_schedule_batch_size = 100

"""
Maximum tokens allowed per example for batch control
"""
_max_tokens_allowed = 16000

"""
GPT Prompting Settings
"""
_gpt_answer_keys = ['doc', 'term', 'sentence']

_prompt_system = prompts.system_context_basic1

# _prompt_instructions = [prompts.task_descr_auditor_15, prompts.answer_format_8]
_prompt_instructions = [prompts.task_descr_notes_15, prompts.answer_format_8]

# old
# _prompt_instructions = [prompts.task_descr_auditor_12, prompts.instruction_6, prompts.answer_format_split_4]
# _prompt_instructions = [prompts.task_descr_notes_5, prompts.instruction_6, prompts.answer_format_split_4]

# optimized
# _prompt_instructions = [prompts.task_descr_auditor_13, prompts.instruction_8_audit, prompts.answer_format_split_6]
# _prompt_instructions = [prompts.task_descr_notes_7, prompts.instruction_8_notes, prompts.answer_format_split_6]

# hybrid
# _prompt_instructions = [prompts.task_descr_auditor_14, prompts.instruction_9_audit, prompts.answer_format_split_7]
# _prompt_instructions = [prompts.task_descr_notes_8, prompts.instruction_9_notes, prompts.answer_format_split_7]
