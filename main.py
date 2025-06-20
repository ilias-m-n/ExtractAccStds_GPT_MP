import os
import pickle
from uuid import uuid4
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

from Controller import Controller
from utility.Meta import Meta
from utility.utility import update_meta, select_file, check_files_in_directory, read_character_yes_no, choose_from_list
import config

def read_meta_config():
    
    meta = None
    path_meta = None
    path_meta_files = os.path.join(os.getcwd(), 'data', 'meta_files')
    
    if check_files_in_directory(path_meta_files) and read_character_yes_no('Would you like to load a preexisting meta-file?'):
        path_meta = select_file(path_meta_files, 'Select Meta File')
        # Load meta and schedule
        with open(path_meta, 'rb') as file:
            meta = pickle.load(file)
            print(f"\n\nReading meta file: {meta.filename}\n")
    else:
        # Read config file
        model = config._model
        batchAPI_method = config._batchAPI_method
        batchAPI_endpoint = config._batchAPI_endpoint
        batchAPI_completion_window = config._batchAPI_completion_window
        batchAPI_description = config._batchAPI_description
        min_ratio = config._min_ratio
        flag_incl_sentence = config._flag_incl_sentence
        flag_incl_doc_entity = config._flag_incl_doc_entity
        flag_user_assistant = config._flag_user_assistant
        flag_segmented = config._flag_segmented
        flag_ext_examples = config._flag_ext_examples
        max_token_num = config._max_token_num
        overlay = config._overlay
        schedule_batch_size = config._schedule_batch_size
        max_tokens_allowed = config._max_tokens_allowed
        gpt_answer_keys = config._gpt_answer_keys
        prompt_system = config._prompt_system
        prompt_instructions = config._prompt_instructions

        mode = choose_from_list('Please choose API query mode:', ['default', 'batchAPI'])

        path_input_files = os.path.join(os.getcwd(), 'data', 'input_file_ids')
        file_input_file_ids = select_file(path_input_files, 'Select Input File').split('\\')[-1]

        path_fs_examples = os.path.join(os.getcwd(), 'data', 'fs_examples')
        file_fs_examples = select_file(path_fs_examples, 'Select File with Few-Shot Examples').split('\\')[-1]

        # Create new Meta object and schedule
        meta = Meta(uuid4(),
                    model,
                    mode,
                    batchAPI_method,
                    batchAPI_endpoint,
                    batchAPI_completion_window,
                    batchAPI_description,
                    datetime.now(),
                    flag_incl_sentence,
                    flag_incl_doc_entity,
                    flag_user_assistant,
                    flag_segmented,
                    flag_ext_examples,
                    min_ratio,
                    max_token_num,
                    overlay,
                    file_fs_examples,
                    file_input_file_ids,
                    schedule_batch_size,
                    max_tokens_allowed,
                    gpt_answer_keys,
                    prompt_system,
                    prompt_instructions)

        path_meta = os.path.join(path_meta_files, meta.filename)
        update_meta(path_meta, meta)
        print(f"\n\nCreated meta file: {meta.filename}\n")

    return meta, path_meta

def main():
    _ = load_dotenv(find_dotenv())
    meta, path_meta = read_meta_config()
    print(meta)
    con = Controller(meta, path_meta)
    con.run()

if __name__ == '__main__':
    main()
