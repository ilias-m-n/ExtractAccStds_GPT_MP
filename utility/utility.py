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
def select_file(path):
    root = Tk()
    root.withdraw()  # Hides the main window
    file_path = filedialog.askopenfilename(initialdir=path, title="Select file")
    if file_path:
        print(f"File selected: {file_path}")
    return file_path

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
            with open(file_path, "r") as file:
                res = file.read()
        except UnicodeDecodeError:
            return return_if_none
        else:
            # checks whether text contains words temporary solution
            # data should be cleaned before creating datasets
            pattern = re.compile(r'\w+')
            if not bool(re.search(pattern, res)):
                return return_if_none
    return res


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
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_completion(client: OpenAI, messages: list[dict[str, str]], model: str = "gpt-3.5-turbo-0125", temp=0):
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
    response = client.chat.completions.create(model=model, messages=messages, temperature=temp)
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
               temp=0):
    messages = create_messages_context_gpt(system, prompt, user_assistant)
    output = get_completion(client, messages, model, temp)
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

def read_character_and_decide():
    while True:  # Keep asking until we get a 'y' or 'n'
        print("\tWould you like to start processing now?")
        user_input = input("\tEnter 'y' or 'n': ").lower()  # Convert to lowercase to handle 'Y' or 'N'
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("\tInvalid input. Please enter 'y' or 'n'.")

def all_keys_present(dictionary, keys):
    return all(key in dictionary for key in keys)

def expand_output(output, answer_keys=None):
    """
    answer_codes:
        0: answer readable
        1: answer not correctly formatted in json
        2: not all source keys present - no longer relevant
        3: not all answers keys present
    """
    if answer_keys is None:
        answer_keys = ['sentence', 'term']

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

    # # check whether all source keys present in dict
    # if not all_keys_present(out_dict, source_keys):
    #     answer_code = 2

    # check whether all answer keys present in answer dicts
    if not all_keys_present(out_dict, answer_keys):
        answer_code = 3

    # extract answers
    # for s in source_keys:
    #     source = out_dict.get(s, None)
    #     if source:
    #         for a in answer_keys:
    #             answers.append(source.get(a, None))
    for a in answer_keys:
        answers.append(out_dict.get(a, None))

    return *answers, answer_code

# Task specific
def prep_fs_examples(df, id_col, paragraph_col, sentence_col, standard_col, incl_sentence,
                     flag_user_assistant,
                     flag_segmented, base_prompt=""):
    user_assistant = None
    prompt_examples = ""

    if flag_user_assistant:
        if not flag_segmented:
            user_assistant = get_user_assistant_context(df, id_col, paragraph_col, sentence_col,
                                                        standard_col, incl_sentence)
        else:
            user_assistant = get_user_assistant_context_segmented(df, paragraph_col, sentence_col,
                                                                  standard_col, incl_sentence)
    else:
        if not flag_segmented:
            prompt_examples = get_examples_prompt(df, id_col, paragraph_col, sentence_col, standard_col,
                                                  incl_sentence, base_prompt)
        else:
            prompt_examples = get_examples_prompt_segmented(df, paragraph_col, sentence_col,
                                                            standard_col, incl_sentence, base_prompt)

    return user_assistant, prompt_examples

def get_user_assistant_context(df, id_col, paragraph_col, sentence_col, standard_col, incl_sentence):
    user_assistant = []

    for id_ua in df[id_col].unique():
        user_content = ""
        assistant_content = None
        row = df[df[id_col] == id_ua]


        user_content += str(row[paragraph_col].values[0]) + " ... "
        if incl_sentence:
            assistant_content = {"sentence": str(row[sentence_col].values[0]),
                                 "term": str(row[standard_col].values[0])}
        else:
            assistant_content = {"term": str(row[standard_col].values[0])}

        user_assistant.append((user_content, json.dumps(assistant_content)))

    return user_assistant


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


def get_examples_prompt(df, id_col, paragraph_col, sentence_col, standard_col, incl_sentence, base):
    examples = base

    for index, curr_id in enumerate(df[id_col].unique()):
        examples += "\nExample " + str(index) + ":\n"
        paragraph = ""
        sentence_std = None
        row = df[df[id_col] == curr_id]


        paragraph += str(row[paragraph_col].values[0]) + " ... "
        if incl_sentence:
            sentence_std = {"sentence": str(row[sentence_col].values[0]),
                            "term": str(row[standard_col].values[0])}
        else:
            sentence_std = {"term": str(row[standard_col].values[0])}

        examples += paragraph + "\nAnswer " + str(index) + ":\n"
        examples += json.dumps(sentence_std) + '\n'

    return examples


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