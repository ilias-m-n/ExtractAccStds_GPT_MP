from utility import prompts

"""
Meta file
If empty new meta file created with empty schedule
"""
_meta = "meta_efb8882d-407a-4123-ad04-bb5e9f3dc839_2024-04-23-13-44.pkl"

"""
"gpt-3.5-turbo-0125"
"gpt-4-0125-preview"
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
_flag_user_assistant = False
_flag_segmented = False

"""
Segmentation Settings
"""
_max_token_num = 15_900
_overlay = 200

"""
Input Files
"""
_file_fs_examples = "fs_examples_auditor.csv"
#_file_input_file_ids = "auditor_gptmeta_2024_04_23_10_07.csv"

"""
Schedule
"""
_schedule_batch_size = 10

"""
Maximum tokens allowed per example
"""
_max_tokens_allowed = 15900

"""
GPT Prompting Settings
"""
_gpt_source_keys = ['auditor']
_gpt_answer_keys = ['sentence', 'term']

_prompt_system = prompts.system_context_basic1
_prompt_instructions = [prompts.task_descr_auditor, prompts.instruction_3, prompts.answer_format_split]