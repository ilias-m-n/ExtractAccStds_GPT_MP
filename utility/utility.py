import json
import os
import pickle
import re
from collections import Counter
from tkinter import Tk, filedialog

import pandas as pd
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from tiktoken import get_encoding

from . import Meta
from . import text_cleaning as tc

# File Dialog
def select_file(path, title):
    root = Tk()
    root.withdraw()  # Hides the main window
    file_path = filedialog.askopenfilename(initialdir=path, title=title)
    if file_path:
        print(f"File selected: {file_path}")
    return file_path

# check whether folder is empty
def check_files_in_directory(path):
    eles = os.listdir(path)
    eles = [ele for ele in eles if ele != '.gitkeep']
    return len(eles) > 0

# delete file 
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} has been deleted successfully.")
    except OSError as error:
        print(f"Error: {error}")
        print(f"Failed to delete {file_path}.")

# Planning functions: Cost and Compute Time

def calc_price_gpt(num_files, avg_tok_size, num_segments, price, tokens_per_price=1000) -> float:
    price = num_files * num_segments * avg_tok_size / tokens_per_price * price
    return price


def calc_price_gpt_one_example(token_length, price, tokens_per_price=1000) -> float:
    return token_length / tokens_per_price * price


def calc_compute_time(num_files, avg_tok_size, num_segments, tokens_per_minute) -> dict:
    minutes_raw = num_files * avg_tok_size * num_segments / tokens_per_minute
    days = minutes_raw // (60 * 24)
    hours = (minutes_raw - days * (60 * 24)) // 60
    minutes = minutes_raw % 60

    # return f"days': {days}, 'hours': {hours}, 'min': {minutes}, 'raw min': {minutes_raw}"
    return {'days': days, 'hours': hours, 'min': minutes, 'raw min': minutes_raw}


# Estimate number of tokens
def count_tokens(text: str, encoding: str = "cl100k_base") -> int:
    encoding = get_encoding(encoding)
    return len(encoding.encode(text))


# Read text and check for empty files
def parse_txt(file_path: str, return_if_none="") -> str:
    res = return_if_none
    # first check whether file exists
    if os.path.isfile(file_path):
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                res = file.read()
        except UnicodeDecodeError:
            print('error reading')
            return return_if_none
        else:
            # checks whether text contains words temporary solution
            # data should be cleaned before creating datasets
            pattern = re.compile(r'\w+')
            if not bool(re.search(pattern, res)):
                return return_if_none
    return res

def read_prompt_for_agg_res(path):
    return tc.clean_text(parse_txt(path))

# Prep Inputs
def prep_inputs(raw_df, filepath_col, coi, base_token_length, flag_segment, max_token_num, overlay,
                encoding="cl100k_base"):
    input_df = raw_df[coi].copy().drop_duplicates()
    input_df['prompt'] = input_df[filepath_col].apply(parse_txt).apply(tc.clean_text)
    input_df['prompt_tokens'] = input_df['prompt'].apply(count_tokens)
    input_df['total_tokens'] = input_df['prompt_tokens'] + base_token_length

    if flag_segment:
        input_df = segment_text_column(input_df, max_token_num, overlay, base_token_length, encoding)

    return input_df

def prep_single_input(path):
    return tc.clean_text(parse_txt(path))


# Create overlaying segments for text
def segment_text_column(raw_df, max_tokens, overlay, context_num_tokens, encoding):
    result_df = pd.DataFrame()
    raw_df = raw_df.copy()

    for index in raw_df.index:
        row = raw_df.loc[index].copy()
        prompt = raw_df.loc[index]['prompt']
        raw_df.drop(index, inplace=True)

        segments = segment_text(prompt, max_tokens - context_num_tokens, overlay, encoding)

        for index_seg, seg in enumerate(segments):
            i_row = row.copy()
            i_row["segment"] = str(index_seg)
            i_row["prompt"] = seg
            i_row = pd.DataFrame([i_row])
            result_df = pd.concat([result_df, i_row], ignore_index=True)

    result_df["prompt_tokens"] = result_df["prompt"].apply(count_tokens)
    result_df["total_tokens"] = result_df["prompt_tokens"] + context_num_tokens

    return result_df


def segment_text(text, max_tokens, overlay, encoding: str = "cl100k_base"):
    tokens_ = 0
    indexes = []
    text_token_len = count_tokens(text)
    while tokens_ + max_tokens <= text_token_len:
        indexes.append((tokens_, max_tokens + tokens_))
        tokens_ += max_tokens - overlay
    indexes.append((tokens_, text_token_len))

    encoder = get_encoding(encoding)
    encoded_text = encoder.encode(text)

    segments = [encoder.decode(encoded_text[index[0]:index[1]]) for index in indexes]

    return segments


# Commonly used terms section
def det_commonly_used_terms(terms: pd.Series, delimiter="|", min_ratio: float = .40) -> dict[str, int]:
    res = []
    for items in terms.dropna().values:
        for item in items.split(delimiter):
            if item == "":
                continue
            res.append(item)
    return {k: v for k, v in Counter(res).items() if v >= terms.size * min_ratio}


def concat_terms(terms: dict[str, int], delimiter=" , ") -> str:
    return delimiter.join(list(terms.keys()))


# Call API
@retry(wait=wait_random_exponential(min=15, max=120), stop=stop_after_attempt(100))
def get_completion(client: OpenAI, messages: list[dict[str, str]], model: str = "gpt-3.5-turbo-0125", temp=0, stream = False, n = 1):
    """
    # Available Models: https://platform.openai.com/docs/models/overview
    
    # Model Response: GPT models return a status code with one of four values, documented in the Response format section
     of the Chat documentation.
        
        stop: API returned complete model output
        length: Incomplete model output due to max_tokens parameter or token limit
        content_filter: Omitted content due to a flag from our content filters
        null: API response still in progress or incomplete
            
        -> 'response.choices[0].finish_reason'
    """
    response = client.chat.completions.create(model=model, messages=messages, temperature=temp, stream = stream, n = n)
    return response


def create_messages_context_gpt(system: str, prompt: str, user_assistant: list[tuple[str, str]] = None) \
        -> list[dict[str, str]]:
    """
    # Message Types
        - system: messages describe the behavior of the AI assistant. A useful system message for data science use cases
          is "You are a helpful assistant who understands data science."
        - user: messages describe what you want the AI assistant to say
        - assistant messages describe previous responses in the conversation.

    The first message should be a system message. Additional messages should alternate between user and assistant.
    """

    messages = [{"role": "system", "content": system}, ]

    if user_assistant:
        for example in user_assistant:
            user, assistant = example
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": prompt})

    return messages


def prompt_gpt(client: OpenAI,
               system: str,
               prompt: str,
               user_assistant: list[tuple[str, str]] = None,
               model: str = "gpt-3.5-turbo-0125",
               temp=0,
               stream = False,
               n = 1):
    messages = create_messages_context_gpt(system, prompt, user_assistant)
    output = get_completion(client, messages, model, temp, stream, n)
    return output

def partial_pivot(df: pd.DataFrame, id_col, sub_id_col, values_cols, other_cols):
    pivot = df.pivot(index=id_col, columns=sub_id_col, values=values_cols)
    df = df[other_cols].copy()
    df.drop_duplicates(inplace=True)
    pivot.columns = [f"{col}_{source}" for col, source in pivot.columns]
    pivot.reset_index(inplace=True)
    return pd.merge(df, pivot, on=id_col, how='inner')


def process_gpt_output(chat_comp: ChatCompletion):
    finish_reason = chat_comp.choices[0].finish_reason
    answer = chat_comp.choices[0].message.content
    comp_tokens = chat_comp.usage.completion_tokens
    prompt_tokens = chat_comp.usage.prompt_tokens

    return answer, finish_reason, prompt_tokens, comp_tokens


def schedule_compute_cost(path_file):
    return count_tokens(tc.clean_text(parse_txt(path_file)))


def update_meta(path_meta: str, meta: Meta):
    with open(path_meta, 'wb') as file:
        pickle.dump(meta, file)


def update_schedule(path_schedule: str, schedule: pd.DataFrame):
    schedule.to_csv(path_schedule, index=False)


def get_num_batches_to_run(prompt, lower_bound, upper_bound):
    while True:
        try:
            user_input = input(prompt)
            if str(user_input) == 'all':
                return upper_bound
            number = int(user_input)
            if lower_bound <= number <= upper_bound:
                return number
            else:
                print(f"Please enter a number within the bounds ({lower_bound}, {upper_bound}).")
        except ValueError:
            print("The input is not a valid integer. Please try again.")


def get_num_workers(prompt, lower_bound, upper_bound):
    while True:
        try:
            user_input = input(prompt)
            number = int(user_input)
            if lower_bound <= number <= upper_bound:
                return number
            else:
                print(f"Please enter a number within the bounds ({lower_bound}, {upper_bound}).")
        except ValueError:
            print("The input is not a valid integer. Please try again.")

def read_bounded_integer(prompt, lower_bound, upper_bound):
    while True:
        try:
            user_input = input(prompt)
            number = int(user_input)
            if lower_bound <= number <= upper_bound:
                return number
            else:
                print(f"Please enter a number within the bounds ({lower_bound}, {upper_bound}).")
        except ValueError:
            print("The input is not a valid integer. Please try again.")

def read_character_yes_no(prompt):
    while True:  # Keep asking until we get a 'y' or 'n'
        print(f"\t{prompt}")
        user_input = input("\tEnter 'y' or 'n': ").lower()  # Convert to lowercase to handle 'Y' or 'N'
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("\tInvalid input. Please enter 'y' or 'n'.")

def choose_from_list(prompt, choices):
    choices = {k:v for k, v in enumerate(choices)}
    while True:
        print(f"\t{prompt}", f"\t {choices}")
        user_input = input("\tSelect integer value of mode: ") 
        try:
            user_input = int(user_input)
        except:
            print("\tInvalid input. Please provide integer value.")
            continue
        if user_input in choices.keys():
            return choices[user_input]
        else:
            print("\tInvalid input. Please make sure to select one of the available values.")

def all_keys_present(dictionary, keys):
    return all(key in dictionary for key in keys)

def split_dicts_string(input_string):
    dict_strings = re.findall(r'\{[^{}]*\}', input_string)
    return dict_strings
'''
def expand_output(output, answer_keys):
    """
    answer_codes:
        0: answer readable
        1: answer not correctly formatted in json
        2: not all answers keys present
    """
    out_dict = None
    answer_code = 0
    len_answer = len(answer_keys) #* len(source_keys)
    answers = list()

    # check output format
    try:
        out_dict = json.loads(output)
    except ValueError:
        answer_code = 1
        return *[None for _ in range(len_answer)], answer_code

    if not isinstance(out_dict, dict):
        answer_code = 1
        return *[None for _ in range(len_answer)], answer_code

    # check whether all answer keys present in answer dicts
    if not all_keys_present(out_dict, answer_keys):
        answer_code = 2

    for a in answer_keys:
        answers.append(out_dict.get(a, None))

    return *answers, answer_code

def expand_output2(output, answer_keys):
    """
    answer_codes:
        0: answer readable
        1: no dictionary found in output
        2: individual answer not correctly formatted in json
        3: individual answer not correctly formatted as dictionary
        4: individual answer not all answers keys present

    """
    len_answer = len(answer_keys)
    
    answers = {key:[] for key in range(len_answer)}
    answer_codes = list()

    answer_dicts = split_dicts_string(output)
    if len(answer_dicts) == 0:
        answer_codes = [1]
        return *[None for _ in range(len_answer)], answer_codes

    # check output format
    for dict_s in answer_dicts:
        out_dict = None
        try:
            mod_dict_s = re.sub(r',\s*\n?\s*}', '}', dict_s)
            out_dict = json.loads(mod_dict_s)
        except ValueError:
            answer_codes.append(2)
            for key in range(len_answer):
                answers[key].append("None")
            continue

        if not isinstance(out_dict, dict):
            answer_codes.append(3)
            for key in range(len_answer):
                answers[key].append("None")

        # check whether all answer keys present in answer dicts
        if not all_keys_present(out_dict, answer_keys):
            answer_codes.append(4)
            for key in range(len_answer):
                answers[key].append("None")
        
        flag_answer_code = False
        for i, a in enumerate(answer_keys):
            answers[i].append(out_dict.get(a, "None"))
            if flag_answer_code:
                continue
            answer_codes.append(0)
            flag_answer_code = True

    #print(answers)
    #for key in answers:
    #    if answers[key] == None:
    #        answers[key] = ""
    answers = ["; ".join(answers[key]) for key in answers]

    return *answers, answer_codes
'''

def clean_json_string(json_str):
    # Regular expression to match non-printable characters
    non_printable_regex = re.compile(r'[\x00-\x1F\x7F-\x9F]')
    
    # Substitute non-printable characters with an empty string
    return non_printable_regex.sub('', json_str)

def expand_output(output, answer_keys):
    """
    answer_codes:
        0: answer readable
        1: no dictionary found in output
        2: individual answer not correctly formatted in json
        3: individual answer not correctly formatted as dictionary
        4: individual answer not all answers keys present

    """

    output = clean_json_string(output)
    
    len_answer = len(answer_keys)
    
    answers = {key:[] for key in range(len_answer)}
    answer_codes = list()

    answer_dicts = split_dicts_string(output)
    if len(answer_dicts) == 0:
        answer_codes = [1]
        return *[None for _ in range(len_answer)], answer_codes

    # check output format
    for dict_s in answer_dicts:
        out_dict = None
        try:
            mod_dict_s = re.sub(r',\s*\n?\s*}', '}', dict_s)
            out_dict = json.loads(mod_dict_s)
        except ValueError:
            answer_codes.append(2)
            for key in range(len_answer):
                answers[key].append("None")
            continue

        #print(out_dict)

        if not isinstance(out_dict, dict):
            answer_codes.append(3)
            for key in range(len_answer):
                answers[key].append("None")

        # check whether all answer keys present in answer dicts
        if not all_keys_present(out_dict, answer_keys):
            answer_codes.append(4)
            for key in range(len_answer):
                answers[key].append("None")
        
        flag_answer_code = False
        for i, a in enumerate(answer_keys):
            #print(i, a, out_dict.get(a, "None"))
            answers[i].append(out_dict.get(a, "None"))
            if flag_answer_code:
                continue
            answer_codes.append(0)
            flag_answer_code = True

    answers = [(answers[key]) for key in answers]
    #print(answers)

    return *answers, answer_codes



# Task specific
def prep_fs_examples(df, id_col, paragraph_col, sentence_col, standard_col, incl_sentence,
                     doc_ent_col, incl_doc_entity, flag_user_assistant,
                     flag_segmented, base_prompt="", flag_ext_examples = False):
    user_assistant = None
    prompt_examples = ""

    if not flag_ext_examples:
        if flag_user_assistant:
            user_assistant = get_user_assistant_context(df, id_col, paragraph_col, sentence_col,
                                                        standard_col, incl_sentence, doc_ent_col, incl_doc_entity)
        else:
            prompt_examples = get_examples_prompt(df, id_col, paragraph_col, sentence_col, standard_col,
                                                  incl_sentence, base_prompt, doc_ent_col, incl_doc_entity)
    else:
        if flag_user_assistant:
            user_assistant = get_user_assistant_context_ext(df, paragraph_col, sentence_col,
                                                        standard_col, incl_sentence, doc_ent_col, incl_doc_entity)
        else:
            prompt_examples = get_examples_prompt_ext(df, paragraph_col, sentence_col, standard_col,
                                                  incl_sentence, base_prompt, doc_ent_col, incl_doc_entity)
    
    
    return user_assistant, prompt_examples

def get_user_assistant_context(df, id_col, paragraph_col, sentence_col, standard_col, incl_sentence, doc_ent_col, incl_doc_entity):
    user_assistant = []

    for id_ua in df[id_col].unique():
        user_content = ""
        assistant_content = None
        row = df[df[id_col] == id_ua]


        user_content += str(row[paragraph_col].values[0]) + " ... "
        if incl_doc_entity and incl_sentence:
            assistant_content["doc"] = str(row[doc_ent_col].values[0])
            assistant_content = {"doc":str(row[doc_ent_col].values[0]),
                                 "sentence": str(row[sentence_col].values[0]),
                                 "term": str(row[standard_col].values[0])}
        elif incl_sentence:
            assistant_content = {"sentence": str(row[sentence_col].values[0]),
                                 "term": str(row[standard_col].values[0])}
        else:
            assistant_content = {"term": str(row[standard_col].values[0])}
            

        user_assistant.append((user_content, json.dumps(assistant_content)))

    return user_assistant

def get_examples_prompt(df, id_col, paragraph_col, sentence_col, standard_col, incl_sentence, base, doc_ent_col, incl_doc_entity):
    examples = base

    for index, curr_id in enumerate(df[id_col].unique()):
        examples += "\nExample " + str(index) + ":\n"
        paragraph = ""
        sentence_std = None
        row = df[df[id_col] == curr_id]


        paragraph += str(row[paragraph_col].values[0]) + " ... "
        if incl_sentence and incl_doc_entity:
            sentence_std = {"doc": str(row[doc_ent_col].values[0]),
                            "sentence": str(row[sentence_col].values[0]),
                            "term": str(row[standard_col].values[0])}
        if incl_sentence:
            sentence_std = {"sentence": str(row[sentence_col].values[0]),
                            "term": str(row[standard_col].values[0])}
        else:
            sentence_std = {"term": str(row[standard_col].values[0])}

        examples += paragraph + "\nAnswer " + str(index) + ":\n"
        examples += json.dumps(sentence_std) + '\n'

    return examples

def get_user_assistant_context_ext(df, paragraph_col, sentence_col, standard_col, incl_sentence, doc_ent_col, incl_doc_entity):
    user_assistant = []
    
    for i, row in df.iterrows():
        
        user_content = row[paragraph_col]
        assistant_content = ''

        for n in range(len(row[sentence_col])):
            curr_ac = {
                'doc': row[doc_ent_col][n].split(';'),
                'sentence': row[sentence_col][n].split(';'),
                'term': row[standard_col][n].split(';')
            }
    
            assistant_content += json.dumps(curr_ac) + '\n\n'
    
        user_assistant.append((user_content, assistant_content))

    return user_assistant

def get_examples_prompt_ext(df, paragraph_col, sentence_col, standard_col, incl_sentence, base, doc_ent_col, incl_doc_entity):
    examples = "base"
    
    for i, row in df.iterrows():
    
        examples += "\nExample " + str(i) + ":\n"
        
        user_content = row[paragraph_col]
        
        assistant_content = ''
            
        for n in range(len(row[sentence_col])):
            curr_ac = {
                'doc': row[doc_ent_col][n].split(';'),
                'sentence': row[sentence_col][n].split(';'),
                'term': row[standard_col][n].split(';')
            }
    
            assistant_content += json.dumps(curr_ac) + '\n'
    
        examples += user_content + "\nAnswer " + str(i) + ":\n"
        examples += assistant_content + '\n'
        
    return examples




### Legacy Functions
def legacy_prep_fs_examples(df, id_col, paragraph_col, sentence_col, standard_col, incl_sentence,
                     doc_ent_col, incl_doc_entity, flag_user_assistant,
                     flag_segmented, base_prompt=""):
    user_assistant = None
    prompt_examples = ""

    if flag_user_assistant:
        if not flag_segmented:
            user_assistant = get_user_assistant_context(df, id_col, paragraph_col, sentence_col,
                                                        standard_col, incl_sentence, doc_ent_col, incl_doc_entity)
        else:
            user_assistant = get_user_assistant_context_segmented(df, paragraph_col, sentence_col,
                                                                  standard_col, incl_sentence)
    else:
        if not flag_segmented:
            prompt_examples = get_examples_prompt(df, id_col, paragraph_col, sentence_col, standard_col,
                                                  incl_sentence, base_prompt, doc_ent_col, incl_doc_entity)
        else:
            prompt_examples = get_examples_prompt_segmented(df, paragraph_col, sentence_col,
                                                            standard_col, incl_sentence, base_prompt)

    return user_assistant, prompt_examples

def get_user_assistant_context_segmented(df, paragraph_col, sentence_col, standard_col,
                                         incl_sentence):
    user_assistant = []

    for i, row in enumerate(df.index):
        paragraph = df.loc[row, paragraph_col]
        sentence_std = df.loc[row, sentence_col]
        standard_std = df.loc[row, standard_col]

        assistant_content = None

        if incl_sentence:
            assistant_content = {"sentence": sentence_std,
                                 "term": standard_std}
        else:
            assistant_content = {"term": standard_std}

        user_assistant.append((paragraph, json.dumps(assistant_content)))

    return user_assistant

def get_examples_prompt_segmented(df, paragraph_col, sentence_col, standard_col, incl_sentence,
                                  base):
    examples = base

    for i, row in enumerate(df.index):

        examples += "\nExample " + str(i) + ":\n"

        paragraph = df.loc[row, paragraph_col]

        sentence_std = df.loc[row, sentence_col]
        standard_std = df.loc[row, standard_col]

        if incl_sentence:
            sentence_std = {"sentence": sentence_std,
                            "term": standard_std}
        else:
            sentence_std = {"term": standard_std}

        examples += paragraph + "\nAnswer " + str(i) + ":\n"
        examples += json.dumps(sentence_std) + '\n'

    return examples




# legacy