from utility import prompts

"""
Meta file
If empty new meta file created with empty schedule
"""
#_meta = ""

"""
"gpt-3.5-turbo-0125"
"gpt-4-turbo"
"gpt-4o"
"""
_model = "gpt-3.5-turbo-0125"

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
_flag_segmented = False

"""
Segmentation Settings
"""
_max_token_num = 15_900
_overlay = 200

"""
Schedule
"""
_schedule_batch_size = 20

"""
Maximum tokens allowed per example
"""
_max_tokens_allowed = 15900

"""
GPT Prompting Settings
"""
#_gpt_source_keys = ['auditor']
_gpt_answer_keys = ['sentence', 'term']

_prompt_system = prompts.system_context_basic1
_prompt_instructions = [prompts.task_descr_notes_3, prompts.instruction_4, prompts.answer_format_split_2]