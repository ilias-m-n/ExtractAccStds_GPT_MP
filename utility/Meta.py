class Meta:

    def __init__(self,
                 uuid,
                 model,
                 datetime,
                 flag_incl_sentence,
                 flag_user_assistant,
                 flag_segmented,
                 min_ratio,
                 max_token_num,
                 overlay,
                 file_fs_examples,
                 file_input_file_ids,
                 schedule_batch_size,
                 max_tokens_allowed,
                 gpt_source_keys,
                 gpt_answer_keys,
                 prompt_system,
                 prompt_instructions
                 ):
        # Date and time in string
        self.creation_datetime = datetime.strftime("%Y-%m-%d-%H-%M")
        # ID
        self.meta_id = uuid
        # Meta filename
        self.filename = f"meta_{self.meta_id}_{self.creation_datetime}.pkl"
        # Model (gpt-3.5 vs gpt-4)
        self.model = model
        # Config flags
        self.flag_incl_sentence = flag_incl_sentence
        self.flag_user_assistant = flag_user_assistant
        self.flag_segmented = flag_segmented
        # Min. term occurrence ratio
        self.min_ratio = min_ratio
        # Segmentation settings
        self.max_token_num = max_token_num
        self.overlay = overlay

        # File paths
        self.file_fs_examples = file_fs_examples
        self.file_input_file_ids = file_input_file_ids

        # Schedule
        self.schedule_batch_size = schedule_batch_size
        self.flag_schedule = False
        self.file_macro_schedule = None
        self.file_micro_schedule = None
        self.file_removed_schedule = None

        # Prompt settings
        self.max_tokens_allowed = max_tokens_allowed

        # GPT Prompt Settings
        self.gpt_source_keys = gpt_source_keys
        self.gpt_answer_keys = gpt_answer_keys
        self.prompt_system = prompt_system
        self.prompt_instructions = prompt_instructions

