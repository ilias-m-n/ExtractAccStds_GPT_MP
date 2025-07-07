import os
import sys
import numpy as np
import pandas as pd
import json
from math import isnan

from Tools.demo.mcast import sender

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

        self.path_batchAPI = os.path.join(self.path_data, 'batchAPI_jobs')
        self.path_batchAPI_inputs = os.path.join(self.path_batchAPI, f"batch_inputs_{self.meta.meta_id}")
        if self.meta.mode == 'batchAPI' and not os.path.exists(self.path_batchAPI_inputs):
            os.makedirs(self.path_batchAPI_inputs)

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

        # BatchAPI Client
        self.bAPI_client = None

        # Aux. Info
        cost_per_1k_tokens_synch = {"gpt-3.5-turbo-0125": 0.0005,  # gpt-3.5-turbo
                                    "gpt-4-turbo-2024-04-09": 0.01,  # gpt-4-turbo
                                    "gpt-4o-2024-08-06": 0.0025,  # gpt-4o
                                    "gpt-4o-mini-2024-07-18": 0.00015,  # gpt-4o-mini
                                    "o1-2024-12-17": 0.015,  # o1,
                                    'o1-pro-2025-03-19': 0.15,  # o1-pro
                                    'o1-mini-2024-09-12': 0.0011,  # o1-mini
                                    "o3-2025-04-16": 0.002,  # o3,
                                    'o3-pro-2025-06-10': 0.02,  # o3-pro
                                    'o3-mini-2025-01-31': 0.0011,  # o3-mini
                                    'gpt-4.1-2025-04-14': 0.002,  # gpt-4.1
                                    'gpt-4.1-mini-2025-04-14': 0.0004,  # gpt-4.1-mini
                                    'gpt-4.1-nano-2025-04-14': 0.0001  # gpt-4.1-nano
                                    }

        cost_per_1k_tokens_batchAPI = {"gpt-3.5-turbo-0125": 0.00025,  # gpt-3.5-turbo
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
                                       'gpt-4.1-nano-2025-04-14': 0.00005}  # gpt-4.1-nano

        cost_per_1k_tokens = {'default': cost_per_1k_tokens_synch, 'batchAPI': cost_per_1k_tokens_batchAPI}

        self.price = cost_per_1k_tokens[self.meta.mode][self.meta.model]

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
        self.gpt_answer_keys = self.meta.gpt_answer_keys
        self.answer_labels = [f"{a}" for a in self.gpt_answer_keys]

    def run(self):
        if self.meta.mode == 'default':
            self.run_default()
        if self.meta.mode == 'batchAPI':
            self.run_batchAPI()

    def run_default(self):
        print('Starting controller...\n')
        print('Generating GPT framework...\n')
        self.prep_GPT_framework()
        print('Loading schedule...')
        self.load_schedule()
        print('Preprocessing and configuration...\n')
        self.preprocessing_and_configure_default()
        print('Processing batches...\n')
        self.process_batches()
        print('Aggregating Results...\n')
        self.aggregate_batch_results()
        print('Done.')

    def run_batchAPI(self):
        print('Starting controller...\n')
        print('Generating GPT framework...\n')
        self.prep_GPT_framework()
        print('Loading schedule...')
        self.load_schedule()
        if not self.meta.flag_batchAPI_prep_done:
            print('Creating batchAPI jobs...')
        self.prep_batchAPI_jobs()
        print('Configure and process...\n')
        self.preprocessing_and_configure_batchAPI()
        print('Process retrieved outputs...\n')
        self.process_batchAPI_outputs()
        print('Done')

    def prep_GPT_framework(self):
        # prep fs examles
        path_fs_examples_file = os.path.join(self.path_fs_examples, self.meta.file_fs_examples)
        df_fs_examples = util.parquet_nested_safe_read(path_fs_examples_file, ['docs', 'sentences', 'terms'])
        user_assistant, fs_prompt = util.prep_fs_examples(df=df_fs_examples,
                                                          id_col='filename',
                                                          paragraph_col='paragraph',
                                                          sentence_col='sentences',
                                                          standard_col='terms',
                                                          incl_sentence=self.meta.flag_incl_sentence,
                                                          doc_ent_col='docs',
                                                          incl_doc_entity=self.meta.flag_incl_doc_entity,
                                                          flag_user_assistant=self.meta.flag_user_assistant,
                                                          flag_segmented=self.meta.flag_segmented,
                                                          flag_ext_examples=self.meta.flag_ext_examples)

        # prep instruction prompt elements
        self.system_prompt = self.meta.prompt_system + ' '.join(self.meta.prompt_instructions)
        self.system_prompt += fs_prompt
        self.user_assistant = user_assistant

        # estimate token length
        self.base_prompt_token_length = util.count_tokens(self.system_prompt)
        if self.user_assistant:
            for ua in self.user_assistant:
                self.base_prompt_token_length += util.count_tokens(ua[0]) + util.count_tokens(ua[1])

        def expand_fs_example_printer(dic):
            jj = json.loads(dic)
            for doc, eles in jj.items():
                print(doc, '\n')
                for ele in eles:
                    print('\t', ele["sentence"], '\n')
                    print('\t\t', ele["terms"], '\n')

        if util.read_character_yes_no('Would you like to show the prompt?\n'):
            print(self.system_prompt)
        if util.read_character_yes_no('Would you like to show the simulated conversation?\n'):
            for ua in user_assistant:
                print()
                print('user:')
                print(f'{ua[0]}')
                print()
                print('assistant:')
                # print(f'{ua[1]}')
                expand_fs_example_printer(ua[1])

    def load_schedule(self):
        if self.meta.flag_schedule:
            self.macro_schedule = pd.read_csv(os.path.join(self.path_schedules, self.meta.file_macro_schedule))
            self.micro_schedule = pd.read_parquet(os.path.join(self.path_schedules, self.meta.file_micro_schedule))
            self.removed_schedule = pd.read_parquet(os.path.join(self.path_schedules, self.meta.file_removed_schedule))
            print()
        else:
            print('\tNo schedule detected...\n\tCreating new schedule...\n')
            self.create_schedules()
            # save changes to meta file
            util.update_meta(self.path_meta, self.meta)
        self.path_macro_schedule = os.path.join(self.path_schedules, self.meta.file_macro_schedule)

    def create_schedules(self):
        # Files
        file_micro = f"micro_{self.meta.meta_id}.parquet"
        file_macro = f"macro_{self.meta.meta_id}.csv"
        file_removed = f"removed_{self.meta.meta_id}.parquet"
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
        removed_examples.to_parquet(path_removed, index=False)
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
        micro_schedule.to_parquet(path_micro, index=False)
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

    def prep_batchAPI_jobs(self):
        if not self.meta.flag_batchAPI_prep_done:
            method = self.meta.batchAPI_method
            url = self.meta.batchAPI_endpoint

            batch_ids = self.macro_schedule['batch_id'].values

            self.macro_schedule['path_batchAPI_job'] = ""
            self.macro_schedule["batchAPI_input_file_id"] = ""
            self.macro_schedule["batchAPI_batch_id"] = ""

            self.macro_schedule["batchAPI_output_file_id"] = ""
            self.macro_schedule["batchAPI_error_file_id"] = ""

            self.macro_schedule["batchAPI_path_output_file"] = ""
            self.macro_schedule["batchAPI_path_error_file"] = ""

            self.macro_schedule = self.macro_schedule.astype({"batchAPI_input_file_id": 'str',
                                                              "batchAPI_batch_id": 'str',
                                                              "batchAPI_output_file_id": 'str',
                                                              "batchAPI_error_file_id": 'str',
                                                              "batchAPI_path_output_file": 'str',
                                                              "batchAPI_path_error_file": 'str'})

            for batch in batch_ids:
                path_file_curr = os.path.join(self.path_batchAPI_inputs, f'batch_job_{batch}.jsonl')
                df_curr = self.micro_schedule[self.micro_schedule.batch_id == batch]
                temp_dict = {"custom_id": "",
                             "method": method,
                             "url": url,
                             "body": {"model": self.meta.model,
                                      "temperature": 0,
                                      "n": 1,
                                      "response_format": {"type": "json_object", },
                                      "logprobs": True,
                                      "messages": [{"role": "system", "content": self.system_prompt}]
                                      }
                             }

                if self.user_assistant:
                    for ua in self.user_assistant:
                        temp_dict['body']["messages"].append({"role": "user", "content": ua[0]})
                        temp_dict['body']["messages"].append({"role": "assistant", "content": ua[1]})

                # pre-append final prompt
                temp_dict['body']["messages"].append({"role": "user", "content": ""})

                with open(path_file_curr, 'w', encoding='utf-8') as file:
                    for index, row in df_curr.iterrows():
                        temp_dict['custom_id'] = str(row['doc_id'])
                        tmp_prompt = util.prep_single_input(row["doc_path"])
                        if len(tmp_prompt) == 0:
                            continue
                        temp_dict['body']["messages"][-1]['content'] = tmp_prompt
                        file.write(json.dumps(temp_dict) + '\n')
                self.macro_schedule.loc[self.macro_schedule.batch_id == batch, "path_batchAPI_job"] = path_file_curr
            util.update_schedule(self.path_macro_schedule, self.macro_schedule)
            self.meta.flag_batchAPI_prep_done = True
            util.update_meta(self.path_meta, self.meta)

        # Fix deprecated warning when excel reads strings columns as float
        self.macro_schedule = self.macro_schedule.astype({"batchAPI_input_file_id": 'str',
                                                          "batchAPI_batch_id": 'str',
                                                          "batchAPI_output_file_id": 'str',
                                                          "batchAPI_error_file_id": 'str',
                                                          "batchAPI_path_output_file": 'str',
                                                          "batchAPI_path_error_file": 'str'})

    def preprocessing_and_configure_default(self):
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

    def preprocessing_and_configure_batchAPI(self):
        if not util.read_character_yes_no('Would you like to start processing now?'):
            sys.exit()

        # All Batch IDs
        all_batch_ids = self.macro_schedule['batch_id'].values

        # Processing Batch IDs
        bAPI_uploaded_batch_ids = list(self.macro_schedule[self.macro_schedule['status'] == 'uploaded'].batch_id.values)
        bAPI_validating_batch_ids = list(
            self.macro_schedule[self.macro_schedule['status'] == 'validating'].batch_id.values)
        bAPI_in_progress_batch_ids = list(
            self.macro_schedule[self.macro_schedule['status'] == 'in_progress'].batch_id.values)
        bAPI_finalizing_batch_ids = list(
            self.macro_schedule[self.macro_schedule['status'] == 'finalizing'].batch_id.values)

        # OpenAI Client
        self.bAPI_client = OpenAI()

        # Check status of uploaded batches
        check_ids = sorted(
            bAPI_uploaded_batch_ids + bAPI_validating_batch_ids + bAPI_in_progress_batch_ids + bAPI_finalizing_batch_ids)
        if len(check_ids) > 0:
            print('\nChecking status of uploaded batches...')
            self.batchAPI_check_status(check_ids)

        # Visualization Print
        if util.read_character_yes_no(f'\nWould you like to show the current status of all batches?: '):
            print('\n', self.macro_schedule[
                ['batch_id', 'status', 'batchAPI_input_file_id', 'batchAPI_output_file_id', 'batchAPI_error_file_id']])

        # Download completed batches
        comp_ids = self.macro_schedule[self.macro_schedule['status'] == 'completed'].batch_id.values
        if len(comp_ids) > 0:
            print('\nDownloading completed batch jobs...')
            self.batchAPI_retrieve_completed(comp_ids)

        # Upload/Queue new batches
        unprocessed_ids = self.macro_schedule[self.macro_schedule['status'] == 'unprocessed'].batch_id.values
        if len(unprocessed_ids) == 0:
            print('\nNo unprocessed batches to upload.')
        else:
            num_batches_to_run = util.read_bounded_integer('\nHow many batches would you like to upload? ', 0,
                                                           len(unprocessed_ids))
            up_ids = unprocessed_ids[:num_batches_to_run]
            if len(up_ids) > 0:
                print('\nUpload unprocessed batches...\n')
                self.batchAPI_upload_jobs(up_ids)
        print()

        # process results
        # self.bAPI_expired_batch_ids = self.macro_schedule[self.macro_schedule['status'] == 'downloaded'].batch_id.values

    def batchAPI_check_status(self, check_ids):
        for i in check_ids:
            curr_batch_id = self.macro_schedule.loc[self.macro_schedule['batch_id'] == i, 'batchAPI_batch_id'].values[0]
            response = self.bAPI_client.batches.retrieve(curr_batch_id)
            status = response.status
            self.macro_schedule.loc[self.macro_schedule['batch_id'] == i, 'status'] = status
            if status == 'completed':
                self.macro_schedule.loc[
                    self.macro_schedule['batch_id'] == i, 'batchAPI_output_file_id'] = response.output_file_id
                self.macro_schedule.loc[
                    self.macro_schedule['batch_id'] == i, 'batchAPI_error_file_id'] = response.error_file_id
        util.update_schedule(self.path_macro_schedule, self.macro_schedule)

    def batchAPI_retrieve_completed(self, comp_ids):
        for i in comp_ids:
            # file ids
            curr_output_file_id = \
                self.macro_schedule.loc[self.macro_schedule['batch_id'] == i, 'batchAPI_output_file_id'].values[0]
            curr_error_file_id = \
                self.macro_schedule.loc[self.macro_schedule['batch_id'] == i, 'batchAPI_error_file_id'].values[0]

            print(f'\nRetrieving batch {i}, output_file_id {curr_output_file_id}, error_file_id {curr_error_file_id}')

            # retrieve result
            result = self.bAPI_client.files.content(curr_output_file_id)

            # write results to file
            # print(isinstance(curr_output_file_id, str))
            if isinstance(curr_output_file_id, str):
                path_out_comp = os.path.join(self.path_results, f'batch_{str(i)}_out.jsonl')
                output = result.content
                print(f"\tWriting outputs to file at: {path_out_comp}")
                with open(path_out_comp, 'wb') as file:
                    file.write(output)
                self.macro_schedule.loc[
                    self.macro_schedule['batch_id'] == i, 'batchAPI_path_output_file'] = path_out_comp
            # write errors to file
            # print(isinstance(curr_error_file_id, str))
            if isinstance(curr_error_file_id, str):
                path_err_comp = os.path.join(self.path_results, f'batch_{str(i)}_err.jsonl')
                error = self.bAPI_client.files.content(curr_error_file_id).content
                # print(error)
                print(f"\tWritin errors to file at: {path_err_comp}")
                with open(path_err_comp, 'wb') as file:
                    file.write(error)
                self.macro_schedule.loc[
                    self.macro_schedule['batch_id'] == i, 'batchAPI_path_error_file'] = path_err_comp
            self.macro_schedule.loc[self.macro_schedule['batch_id'] == i, 'status'] = 'downloaded'

        util.update_schedule(self.path_macro_schedule, self.macro_schedule)

    def batchAPI_upload_jobs(self, new_ids):
        for i in new_ids:
            # upload file
            path_curr_input = self.macro_schedule.loc[self.macro_schedule.batch_id == i, "path_batchAPI_job"].values[0]

            batch_file = self.bAPI_client.files.create(
                file=open(path_curr_input, 'rb'),
                purpose='batch'
            )
            self.macro_schedule.loc[self.macro_schedule.batch_id == i, "batchAPI_input_file_id"] = batch_file.id
            cur_file_id = self.macro_schedule.loc[self.macro_schedule.batch_id == i, "batchAPI_input_file_id"].values[0]

            # create batch job
            batch_job = self.bAPI_client.batches.create(
                input_file_id=cur_file_id,
                endpoint=self.meta.batchAPI_endpoint,
                completion_window=self.meta.batchAPI_completion_window
            )
            self.macro_schedule.loc[self.macro_schedule.batch_id == i, "batchAPI_batch_id"] = batch_job.id

            self.macro_schedule.loc[self.macro_schedule.batch_id == i, "status"] = 'uploaded'
        util.update_schedule(self.path_macro_schedule, self.macro_schedule)

    def aggregate_batch_results(self):
        if not util.check_files_in_directory(self.path_results) or not util.read_character_yes_no(
                'Would you like to aggregate the batched results?'):
            return 0
        batch_result_files = [os.path.join(self.path_results, batch) for batch in os.listdir(self.path_results)]
        agg_df = None
        for path in batch_result_files:
            curr_df = pd.read_csv(path)
            agg_df = pd.concat([agg_df, curr_df]) if isinstance(agg_df, pd.DataFrame) else curr_df
            # util.delete_file(path)
        agg_df.reset_index(drop=True, inplace=True)
        agg_df.to_csv(os.path.join(self.path_results, 'agg_results.csv'), index=False)

    def process_batchAPI_outputs(self):
        # 
        down_ids = list(self.macro_schedule[self.macro_schedule['status'] == 'downloaded'].batch_id.values)

        for i in down_ids:
            curr_path = \
                self.macro_schedule.loc[self.macro_schedule['batch_id'] == i, 'batchAPI_path_output_file'].values[0]

            doc_id = []
            prompt_tokens = []
            comp_tokens = []
            finish_reason = []
            answer = []
            logprobs = []

            with open(curr_path, 'rb') as file:
                for line in file:
                    jobj = json.loads(line)
                    doc_id.append(int(jobj['custom_id']))
                    prompt_tokens.append(int(jobj['response']['body']['usage']['prompt_tokens']))
                    comp_tokens.append(int(jobj['response']['body']['usage']['completion_tokens']))
                    finish_reason.append(jobj['response']['body']['choices'][0]['finish_reason'])
                    answer.append(jobj['response']['body']['choices'][0]['message']['content'])
                    logprobs.append(jobj['response']['body']['choices'][0]['logprobs'])

            curr_df = pd.DataFrame({'doc_id': doc_id,
                                    'output': answer,
                                    'finish_reason': finish_reason,
                                    'true_total_prompt_tokens': prompt_tokens,
                                    'completion_tokens': comp_tokens,
                                    'logprobs_raw': logprobs})

            curr_df['logprob_output'] = [util.calc_overall_seq_logprob(logprob['content']) for logprob in logprobs]
            curr_df['probs_output'] = np.exp(curr_df['logprob_output'])

            def expand_output_column(df):
                rows = []
                for _, row in df.iterrows():
                    base = row.drop('output').to_dict()
                    try:
                        # print('1:', row['output'])
                        output_dict = json.loads(row['output'])
                        # print('2:', output_dict)
                        # print('------------------------------')
                    except Exception:
                        output_dict = {}
                    if not output_dict:
                        empty_row = base.copy()
                        empty_row['doc'] = None
                        empty_row['sentence'] = None
                        empty_row['terms'] = None
                        empty_row['has_result'] = False
                        rows.append(empty_row)
                    else:
                        for key, val in output_dict.items():
                            doc = key
                            for ele in val:
                                new_row = base.copy()
                                new_row['doc'] = doc
                                new_row['sentence'] = ele.get('sentence', '')
                                new_row['terms'] = ele.get('terms', [])
                                new_row['has_result'] = True
                                rows.append(new_row)

                return pd.DataFrame(rows)

            curr_df = expand_output_column(curr_df)

            curr_df.to_parquet(os.path.join(self.path_results, f'batch_{i}.parquet'), index=False)

            self.macro_schedule.loc[self.macro_schedule['batch_id'] == i, 'status'] = 'processed'
            util.update_schedule(self.path_macro_schedule, self.macro_schedule)

        if util.read_character_yes_no('Would you like to aggregate the batched results?'):
            batch_result_files = [os.path.join(self.path_results,
                                               batch) for batch in os.listdir(self.path_results) if
                                  ((batch.startswith('batch')) and (batch.endswith('parquet')))]
            agg_df = None
            for path in batch_result_files:
                curr_df = pd.read_parquet(path)
                agg_df = pd.concat([agg_df, curr_df]) if isinstance(agg_df, pd.DataFrame) else curr_df

            if util.read_character_yes_no('Would you like to add the gpt_prompts to the aggregate results?'):
                tmp_micro = self.micro_schedule[self.micro_schedule.doc_id.isin(agg_df.doc_id)][
                    ['doc_id', 'doc_path']].copy()
                agg_df = pd.merge(agg_df, tmp_micro, how='left', on='doc_id')
                # print(agg_df[agg_df['doc_id'].isna()])
                agg_df['prompt'] = agg_df['doc_path'].apply(util.read_prompt_for_agg_res)

                agg_df = agg_df[
                    ['doc_id', 'doc_path', 'has_result', 'logprob_output', 'probs_output', 'doc', 'terms', 'sentence',
                     'prompt']]
            else:
                agg_df = agg_df[
                    ['doc_id', 'doc_path', 'has_result', 'logprob_output', 'probs_output', 'doc', 'terms', 'sentence']]
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
                                                     self.gpt_answer_keys,
                                                     self.path_results,
                                                     self.path_macro_schedule,
                                                     ))
                # print(res.get())
            pool.close()
            pool.join()

        print(f"\n\tAll desired batches processed.\n")
        self.meta.number_unprocessed_batches = \
            self.macro_schedule[self.macro_schedule['status'] == 'unprocessed'].shape[0]


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
                  # source_keys,
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
    # df_input[answer_labels] = df_input.apply(lambda x: util.expand_output(x.output, answer_keys), axis=1, result_type='expand')
    # df_input[answer_labels] = df_input.apply(lambda x: util.expand_output2(x.output, answer_keys), axis=1, result_type='expand')
    df_input[answer_labels] = df_input.apply(lambda x: util.expand_output3(x.output, answer_keys), axis=1,
                                             result_type='expand')
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
           # source_keys,
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
                               # source_keys,
                               answer_keys,
                               path_results,
                               )

        with lock:
            processed_batch_ids.append(batch_id)
            macro_schedule = pd.read_csv(path_macro_schedules)
            macro_schedule.loc[macro_schedule.batch_id == batch_id, "status"] = 'processed'
            util.update_schedule(path_macro_schedules, macro_schedule)
        print(f"\tFinished batch ID: {batch_id}")
