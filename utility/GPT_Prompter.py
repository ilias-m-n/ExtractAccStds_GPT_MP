import pandas as pd

from . import prompts
from . import utility as util


class GPT_Prompter:
    def __init__(self,
                 path_file_fs_examples,
                 min_ratio,
                 flag_incl_sentence,
                 flag_user_assistant,
                 flag_segmented):

        self.df = pd.read_csv(path_file_fs_examples)

        # Min. term occurrence ratio
        self.min_ratio = min_ratio

        # Flags
        self.flag_incl_sentence = flag_incl_sentence
        self.flag_user_assistant = flag_user_assistant
        self.flag_segmented = flag_segmented

        # Prompts
        self.section_terms_auditor = None
        self.section_terms_notes = None

        # System Prompt
        self.system_prompt = None

        # FS Examples
        self.user_assistant = None
        self.fs_prompt = None

        # Token Length Base Prompt
        self.base_prompt_token_length = 0

    def prep(self):
        self.get_common_terms()
        self.df.drop(['terms_audit', 'terms_notes'], axis=1, inplace=True)
        self.get_fs_examples()
        self.get_system_prompt()

    def get_common_terms(self):
        terms_auditor = util.concat_terms(util.det_commonly_used_terms(self.df['terms_audit']))
        terms_notes = util.concat_terms(util.det_commonly_used_terms(self.df['terms_notes']))
        self.section_terms_auditor = prompts.common_terms_section_auditor.format(terms_auditor=terms_auditor)
        self.section_terms_notes = prompts.common_terms_section_notes.format(terms_notes=terms_notes)

    def get_system_prompt(self):
        system_unsegmented = prompts.system_context_basic + \
                             prompts.task_descr_1 + \
                             self.section_terms_auditor + \
                             self.section_terms_notes + \
                             prompts.instruction_1 + \
                             prompts.answer_format1

        system_segmented = prompts.system_context_basic + \
                           prompts.task_descr_2 + \
                           self.section_terms_auditor + \
                           self.section_terms_notes + \
                           prompts.instruction_2 + \
                           prompts.answer_format2

        self.system_prompt = system_segmented if self.flag_segmented else system_unsegmented
        self.system_prompt += self.fs_prompt

        self.base_prompt_token_length += util.count_tokens(self.system_prompt)
        if self.user_assistant:
            for ua in self.user_assistant:
                self.base_prompt_token_length += util.count_tokens(ua[0]) + util.count_tokens(ua[1])

    def get_fs_examples(self):
        self.user_assistant, self.fs_prompt = util.prep_fs_examples(df=self.df,
                                                                    id_col='filename',
                                                                    source_col='source',
                                                                    paragraph_col='paragraph (context)',
                                                                    sentence_col='sentence',
                                                                    standard_col='term',
                                                                    incl_sentence=self.flag_incl_sentence,
                                                                    flag_user_assistant=self.flag_user_assistant,
                                                                    flag_segmented=self.flag_segmented,
                                                                    base_prompt=prompts.examples_base1)
