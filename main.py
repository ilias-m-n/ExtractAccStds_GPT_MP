import os
import pickle
from uuid import uuid4
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

from Controller import Controller
from utility.Meta import Meta
from utility.utility import update_meta
import config

def read_meta_config():
    meta = None
    path_meta = None
    if config._meta:
        # Load meta and schedule
        path_meta = os.path.join(os.getcwd(), 'meta_files', config._meta)
        with open(path_meta, 'rb') as file:
            meta = pickle.load(file)
    else:
        # Read config file
        model = config._model
        min_ratio = config._min_ratio
        flag_incl_sentence = config._flag_incl_sentence
        flag_user_assistant = config._flag_user_assstant
        flag_segmented = config._flag_segmented
        max_token_num = config._max_token_num
        overlay = config._overlay
        file_fs_examples = config._file_fs_examples
        file_input_file_ids = config._file_input_file_ids
        schedule_batch_size = config._schedule_batch_size
        max_tokens_allowed = config._max_tokens_allowed

        # Create new Meta object and schedule
        meta = Meta(uuid4(),
                    model,
                    datetime.now(),
                    flag_incl_sentence,
                    flag_user_assistant,
                    flag_segmented,
                    min_ratio,
                    max_token_num,
                    overlay,
                    file_fs_examples,
                    file_input_file_ids,
                    schedule_batch_size,
                    max_tokens_allowed)

        meta_filename = f"meta_{meta.meta_id}_{meta.creation_datetime}.pkl"
        path_meta = os.path.join(os.getcwd(), 'meta_files', meta_filename)
        update_meta(path_meta, meta)
        # with open(path_meta, 'wb') as file:
        #     pickle.dump(meta, file)

    return meta, path_meta

if __name__ == '__main__':
    _ = load_dotenv(find_dotenv())
    meta, path_meta = read_meta_config()
    con = Controller(meta, path_meta)
    con.run()
