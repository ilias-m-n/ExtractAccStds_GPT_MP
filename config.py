"""
Meta file
If empty new meta file created with empty schedule
"""
_meta = ""

"""
"gpt-3.5-turbo-0125"
"gpt-4-0125-preview"
"""
_model = "gpt-4-0125-preview"

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
_file_fs_examples = "fs_examples.csv"
_file_input_file_ids = "input.csv"

"""
Schedule
"""
_schedule_batch_size = 2

"""
Maximum tokens allowed per example
"""
_max_tokens_allowed = 85_000

"""
GPT Prompting Settings
"""
_gpt_source_keys = ['audit', 'notes']
_gpt_answer_keys = ['sentence', 'term']