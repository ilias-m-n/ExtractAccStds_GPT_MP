import os
import sys
import pandas as pd

pd.set_option('display.width', None)
from multiprocessing import Pool, Manager
from openai import OpenAI

import utility.utility as util
from utility import prompts


class Controller():
    def __init__(self, meta, path_meta):
        # Meta
        self.meta = meta
        self.path_meta = path_meta

        # Directory paths
        self.path_cwd = os.getcwd()
        self.path_data = os.path.join(self.path_cwd, 'data')
        self.path_schedules = os.path.join(self.path_data, 'schedules')
        self.path_input_file_ids = os.path.join(self.path_data, 'input_file_ids')
        self.path_fs_examples = os.path.join(self.path_data, 'fs_examples')
        self.path_raw_files = os.path.join(self.path_data, 'raw_files')
        self.path_outputs = os.path.join(self.path_data, 'outputs')
        self.path_results = os.path.join(self.path_outputs,
                                         f"results_{self.meta.meta_id}_{self.meta.creation_datetime}")
        if not os.path.exists(self.path_results):
            os.makedirs(self.path_results)

        # Schedules
        self.macro_schedule = None
        self.path_macro_schedule = None
        self.micro_schedule = None
        self.removed_schedule = None

        # Aux. Info
        cost_per_1k_tokens = {"gpt-3.5-turbo-0125": 0.0005, "gpt-4-turbo": 0.01, "gpt-4o": 0.005}
        self.price = cost_per_1k_tokens[self.meta.model]

        # GPT Prompt Settings
        self.base_prompt_token_length = None
        self.system_prompt = None
        self.user_assistant = None

        # Parallelization settings
        self.num_workers = None
        self.manager = Manager()
        self.unprocessed_batch_ids = None
        self.processed_batch_ids = None
        self.lock = None

        # Number of batches to run
        self.num_batches_to_run = None

        # JSON Output Format Keys
        #self.gpt_source_keys = self.meta.gpt_source_keys
        self.gpt_answer_keys = self.meta.gpt_answer_keys
        #self.answer_labels = [f"{s}_{a}" for s in self.gpt_source_keys for a in self.gpt_answer_keys]
        self.answer_labels = [f"{a}" for a in self.gpt_answer_keys]
        self.answer_labels += ['answer_code']

    def run(self):
        print('Starting controller...\n')
        print('Generating GPT framework...\n')
        self.prep_GPT_framework()
        print('Loading schedule...')
        self.load_schedule()
        print('Preprocessing and configuration...\n')
        self.preprocessing_and_configure()
        print('Processing batches...\n')
        self.process_batches()
        print('Aggregating Results...\n')
        self.aggregate_batch_results()
        print('Done.')

    def prep_GPT_framework(self):
        # prep fs examles
        path_fs_examples_file = os.path.join(self.path_fs_examples, self.meta.file_fs_examples)
        #df_fs_examples = pd.read_csv(path_fs_examples_file)
        df_fs_examples = pd.read_parquet(path_fs_examples_file)
        user_assistant, fs_prompt = util.prep_fs_examples(df=df_fs_examples,
                                                          id_col='filename',
                                                          paragraph_col='paragraph',
                                                          sentence_col='sentence',
                                                          standard_col='term',
                                                          incl_sentence=self.meta.flag_incl_sentence,
                                                          doc_ent_col = 'doc_type',
                                                          incl_doc_entity = self.meta.flag_incl_doc_entity,
                                                          flag_user_assistant=self.meta.flag_user_assistant,
                                                          flag_segmented=self.meta.flag_segmented,
                                                          base_prompt=prompts.examples_base1,
                                                          flag_ext_examples= self.meta.flag_ext_examples)

        # prep instruction prompt elements
        self.system_prompt = self.meta.prompt_system + ' '.join(self.meta.prompt_instructions)
        self.system_prompt += fs_prompt
        self.user_assistant = user_assistant

        # estimate token length
        self.base_prompt_token_length = util.count_tokens(self.system_prompt)
        if user_assistant:
            for ua in user_assistant:
                self.base_prompt_token_length += util.count_tokens(ua[0]) + util.count_tokens(ua[1])

    def load_schedule(self):
        if self.meta.flag_schedule:
            self.macro_schedule = pd.read_csv(os.path.join(self.path_schedules, self.meta.file_macro_schedule))
            self.micro_schedule = pd.read_csv(os.path.join(self.path_schedules, self.meta.file_micro_schedule))
            self.removed_schedule = pd.read_csv(os.path.join(self.path_schedules, self.meta.file_removed_schedule))
            print()
        else:
            print('\tNo schedule detected...\n\tCreating new schedule...\n')
            self.create_schedules()
            # save changes to meta file
            util.update_meta(self.path_meta, self.meta)
        self.path_macro_schedule = os.path.join(self.path_schedules, self.meta.file_macro_schedule)

    def create_schedules(self):
        # Files
        file_micro = f"micro_{self.meta.meta_id}.csv"
        file_macro = f"macro_{self.meta.meta_id}.csv"
        file_removed = f"removed_{self.meta.meta_id}.csv"
        # Paths
        path_micro = os.path.join(self.path_schedules, file_micro)
        path_macro = os.path.join(self.path_schedules, file_macro)
        path_removed = os.path.join(self.path_schedules, file_removed)

        path_input_file_ids_file = os.path.join(self.path_input_file_ids, self.meta.file_input_file_ids)
        # read input file
        micro_schedule = pd.read_csv(path_input_file_ids_file)
        micro_schedule['prompt_token_length'] = micro_schedule['doc_path'].apply(
            util.schedule_compute_cost) + self.base_prompt_token_length
        # remove examples which exceed limit
        removed_examples = micro_schedule[micro_schedule['prompt_token_length'] > self.meta.max_tokens_allowed].copy()
        removed_examples.to_csv(path_removed, index=False)
        del removed_examples
        micro_schedule = micro_schedule[micro_schedule['prompt_token_length'] <= self.meta.max_tokens_allowed].copy()
        micro_schedule.reset_index(drop=True, inplace=True)
        # assign batch ids
        micro_schedule['batch_id'] = micro_schedule.index // self.meta.schedule_batch_size + 1
        micro_schedule['prompt_cost'] = micro_schedule['prompt_token_length'].apply(util.calc_price_gpt_one_example,
                                                                                    args={self.price})
        self.micro_schedule = micro_schedule.copy()
        # Agg. to create macro schedule
        macro_schedule = micro_schedule.drop(['doc_id', 'doc_path'], axis=1).copy()
        micro_schedule.to_csv(path_micro, index=False)
        del micro_schedule
        macro_schedule = macro_schedule.groupby('batch_id').agg(
            num_examples=('prompt_token_length', 'count'),
            avg_prompt_token_length=('prompt_token_length', 'mean'),
            sum_prompt_cost=('prompt_cost', 'sum')
        ).reset_index()
        macro_schedule['status'] = 'unprocessed'
        self.macro_schedule = macro_schedule.copy()
        macro_schedule.to_csv(path_macro, index=False)
        self.meta.overall_est_cost = self.macro_schedule['sum_prompt_cost'].sum()
        self.meta.number_unprocessed_batches = self.macro_schedule.shape[0]
        del macro_schedule
        # Update meta object
        self.meta.file_macro_schedule = file_macro
        self.meta.file_micro_schedule = file_micro
        self.meta.file_removed_schedule = file_removed
        self.meta.flag_schedule = True

    def preprocessing_and_configure(self):
        if not util.read_character_yes_no('Would you like to start processing now?'):
            sys.exit()
        # MultiProcessing Settings
        self.unprocessed_batch_ids = self.macro_schedule[self.macro_schedule['status'] == 'unprocessed'].batch_id.values
        self.meta.number_unprocessed_batches = len(self.unprocessed_batch_ids)
        if len(self.unprocessed_batch_ids) > 0:
            print(f"\n\t{len(self.unprocessed_batch_ids)} unprocessed batches remaining...")
        else:
            print("\n\tAll batches have already been processed. Shutting down...")
            self.aggregate_batch_results()
            sys.exit()
        processed_batch_ids = self.macro_schedule[self.macro_schedule['status'] != 'unprocessed'].batch_id.values
        self.processed_batch_ids = self.manager.list(processed_batch_ids)
        self.num_batches_to_run = util.get_num_batches_to_run('\tHow many batches would you like to run?\t',
                                                              1, len(self.unprocessed_batch_ids))
        self.unprocessed_batch_ids = self.unprocessed_batch_ids[:self.num_batches_to_run]
        self.unprocessed_batch_ids = self.manager.list(self.unprocessed_batch_ids)
        self.num_workers = util.get_num_workers('\tHow many workers would you like to employ?\t',
                                                1, min(36, len(self.unprocessed_batch_ids)))
        self.lock = self.manager.Lock()
        print()

    def aggregate_batch_results(self):
        if not util.check_files_in_directory(self.path_results) or not util.read_character_yes_no('Would you like to aggregate the batched results?'):
            return 0
        batch_result_files = [os.path.join(self.path_results, batch) for batch in os.listdir(self.path_results)]
        agg_df = None
        for path in batch_result_files:
            curr_df = pd.read_csv(path)
            agg_df = pd.concat([agg_df, curr_df]) if isinstance(agg_df, pd.DataFrame) else curr_df
            util.delete_file(path)
        agg_df.reset_index(drop=True, inplace=True)
        agg_df.to_csv(os.path.join(self.path_results, 'agg_results.csv'), index=False)
        

    def process_batches(self):
        with Pool(processes=self.num_workers) as pool:
            for _ in range(self.num_workers):
                print('hi')
                res = pool.apply_async(worker, args=(self.unprocessed_batch_ids,
                                                     self.processed_batch_ids,
                                                     self.lock,
                                                     self.micro_schedule,
                                                     self.base_prompt_token_length,
                                                     self.meta.flag_segmented,
                                                     self.meta.max_token_num,
                                                     self.meta.overlay,
                                                     self.system_prompt,
                                                     self.user_assistant,
                                                     self.meta.model,
                                                     self.answer_labels,
                                                     #self.gpt_source_keys,
                                                     self.gpt_answer_keys,
                                                     self.path_results,
                                                     self.path_macro_schedule,
                                                     ))
                #print(res.get())
            pool.close()
            pool.join()

        print(f"\n\tAll desired batches processed.\n")
        self.meta.number_unprocessed_batches = self.macro_schedule[self.macro_schedule['status'] == 'unprocessed'].shape[0]

def process_batch(batch_id,
                  df_segment,
                  base_token_length,
                  flag_segmented,
                  max_token_num,
                  overlay,
                  system,
                  user_assistant,
                  model,
                  answer_labels,
                  #source_keys,
                  answer_keys,
                  path_results,
                  ):
    df_input = util.prep_inputs(df_segment,
                                'doc_path',
                                ['doc_path', 'doc_id'],
                                base_token_length,
                                flag_segmented,
                                max_token_num,
                                overlay)
    df_input.drop(['prompt_tokens', 'total_tokens'], axis=1, inplace=True)
    client = OpenAI()
    df_input['output'] = df_input.apply(
        lambda x: util.prompt_gpt(client, system, x.prompt, user_assistant, model), axis=1)

    # extend gpt completion
    df_input[['output', 'finish_reason', 'true_total_prompt_tokens', 'completion_tokens']] = df_input.apply(
        lambda x: util.process_gpt_output(x.output), axis=1, result_type='expand')
    df_input.drop(['doc_path'], axis=1, inplace=True)

    # process json answer
    #df_input[answer_labels] = df_input.apply(lambda x: util.expand_output(x.output, answer_keys), axis=1, result_type='expand')
    #df_input[answer_labels] = df_input.apply(lambda x: util.expand_output2(x.output, answer_keys), axis=1, result_type='expand')
    df_input[answer_labels] = df_input.apply(lambda x: util.expand_output3(x.output, answer_keys), axis=1, result_type='expand')
    # save dataframe as csv
    df_input.to_csv(os.path.join(path_results, f'batch_{str(batch_id)}.csv'), index=False)
    return True


def worker(unprocessed_batch_ids,
           processed_batch_ids,
           lock,
           micro_schedule,
           base_token_length,
           flag_segmented,
           max_token_num,
           overlay,
           system,
           user_assistant,
           model,
           answer_labels,
           #source_keys,
           answer_keys,
           path_results,
           path_macro_schedules,
           ):
    while unprocessed_batch_ids:
        with lock:
            if unprocessed_batch_ids:
                batch_id = unprocessed_batch_ids.pop(0)

        print(f"\tProcessing batch {batch_id}")
        df_segment = micro_schedule[micro_schedule.batch_id == batch_id]
        result = process_batch(batch_id,
                               df_segment,
                               base_token_length,
                               flag_segmented,
                               max_token_num,
                               overlay,
                               system,
                               user_assistant,
                               model,
                               answer_labels,
                               #source_keys,
                               answer_keys,
                               path_results,
                               )


        with lock:
            processed_batch_ids.append(batch_id)
            macro_schedule = pd.read_csv(path_macro_schedules)
            macro_schedule.loc[macro_schedule.batch_id == batch_id, "status"] = 'processed'
            util.update_schedule(path_macro_schedules, macro_schedule)
        print(f"\tFinished batch ID: {batch_id}")
