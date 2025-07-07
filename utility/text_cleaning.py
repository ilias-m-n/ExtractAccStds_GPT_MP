import re


def replace_consecutive_newlines(text) -> str:
    # Use regular expression to replace consecutive newlines with a single newline
    modified_text = re.sub(r'\n\s*\n*', ' ', text)
    return modified_text


def remove_special_characters(text) -> str:
    # Use replace to remove \x0c
    modified_text = re.sub(r'[\x0c\xad]', ' ', text)
    return modified_text


def remove_links(text) -> str:
    # Use regular expression to remove links starting with www.
    # Use regular expression to remove links
    modified_text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    return modified_text


def remove_dates(text) -> str:
    # Use regular expression to remove dates like "31 March 2006"
    modified_text = re.sub(r'\b\d{1,2} [a-zA-Z]+ \d{4}\b', ' ', text)
    return modified_text


def remove_currency(text) -> str:
    modified_text = re.sub(r'[$€£¥₹₽₩₺₴₭₪₨]', " ", text)
    return modified_text


def remove_decimal_numbers(text) -> str:
    # Use regular expression to remove decimal point numbers, sometimes followed by "p" for percent
    modified_text = re.sub(r'\b[(]?(\d{1,3},)*\d{0,3}.\d+[pkKmMbB)]?\b', ' ', text)
    return modified_text


def remove_parenthesis(text) -> str:
    modified_text = re.sub(r'\(\s*\d*[a-zA-Z]?\+?\s*\)', ' ', text)
    return modified_text


def remove_percent(text) -> str:
    # Use regular expression to remove "per cent" text and percent symbols
    modified_text = re.sub(r'\b(?:per cent|%)\b', ' ', text)
    return modified_text


def remove_lonely_symbols(text) -> str:
    modified_text = re.sub(r"\s+(\(?\d{0,2}%[),]?|\'|N/A|\(|p|per cent|\*|·|million|,|\.|-|:)\s+", ' ', text)
    return modified_text


def remove_extra_spaces(text) -> str:
    # Use regular expression to remove extra spaces
    return re.sub(r' {2,}', ' ', text)


def remove_extra_points(text) -> str:
    modified_text = re.sub(r'\.{2,}', r"\.", text)
    return modified_text


def remove_double_backslashes(text):
    # Use regular expression to remove double backslashes
    modified_text = re.sub(r'\\', '', text)
    return modified_text


def remove_emails(text):
    # Use regular expression to remove email addresses
    modified_text = re.sub(r'\S+@\S+', ' ', text)
    return modified_text


def remove_mult_underscore(text):
    modified_text = re.sub(r'__+', " ", text)
    return modified_text


def rem_non_printables(text):
    # Regular expression to match non-printable characters
    non_printable_regex = re.compile(r'[\x00-\x1F\x7F-\x9F]')

    # Substitute non-printable characters with an empty string
    return non_printable_regex.sub('', text)


def replace_quotes_around_brackets(s):
    # Replace single quote before [
    s = s.replace("']", '"]')
    # Replace single quote after ]
    s = s.replace("['", '["')
    return s


def clean_text(text) -> str:
    text = remove_special_characters(text)
    text = replace_consecutive_newlines(text)
    text = remove_links(text)
    # text = remove_dates(text)
    text = remove_currency(text)
    text = remove_decimal_numbers(text)
    # text = remove_lonely_symbols(text)
    text = remove_multiple_spaces(text)
    text = remove_extra_points(text)
    text = remove_double_backslashes(text)
    text = remove_emails(text)
    text = remove_mult_underscore(text)
    return text


def fix_spaces_around_symbols(text: str) -> str:
    """
    Cleans up spacing and removes unwanted characters (hyphens, spaces before/after symbols) in the string.
    Applies: comma, colon, semicolon, parentheses, brackets, slash, hyphen, multiple spaces.
    """
    text = remove_space_before_comma_colon_semicolon(text)
    text = remove_space_before_after_parentheses(text)
    text = remove_space_before_after_brackets(text)
    text = remove_space_around_slash(text)
    text = remove_hyphens(text)
    text = remove_multiple_spaces(text)
    return text


def remove_space_before_comma_colon_semicolon(text: str) -> str:
    """
    Removes spaces immediately before a comma, colon (:), or semicolon (;).
    Leaves spaces after untouched.
    """
    text = re.sub(r'\s+,', ',', text)
    text = re.sub(r'\s+:', ':', text)
    text = re.sub(r'\s+;', ';', text)
    return text


def remove_space_before_after_parentheses(text: str) -> str:
    """
    Removes spaces immediately after '(' and immediately before ')'.
    Does not touch spaces inside text or between words.
    """
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    return text


def remove_space_before_after_brackets(text: str) -> str:
    """
    Removes spaces immediately after '[' and immediately before ']'.
    Does not remove spaces inside text or between words.
    """
    text = re.sub(r'\[\s+', '[', text)
    text = re.sub(r'\s+\]', ']', text)
    return text


def remove_space_around_slash(text: str) -> str:
    """
    Removes spaces immediately before and after a slash (/).
    Does not affect other characters.
    """
    text = re.sub(r'\s*/\s*', '/', text)
    return text


def remove_hyphens(text: str) -> str:
    """
    Removes all hyphens (-) from the input string.
    """
    return text.replace('-', '')


def remove_multiple_spaces(text: str) -> str:
    """
    Replaces every occurrence of two or more consecutive spaces with a single space.
    """
    return re.sub(r' {2,}', ' ', text)
