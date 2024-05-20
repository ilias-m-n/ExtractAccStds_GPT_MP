# System Context Messages   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
system_context_basic1 = """
You are a financial accountant.
"""

# Few Shot Examples
examples_base1 = """
Here are a few examples:
"""

# Task Description :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

task_descr_old1 = """
You are tasked to extract information contained within two sections, the auditor section and the notes section,  \
of a provided financial statement. \
More specifically, from the notes section you are tasked to extract according to what accounting standard \
the financial statement has been prepared, and from the auditor section you are tasked to extract what accounting \
standard the financial statement is in compliance with. \
It is possible that a financial statement is in compliance with or has been constructed according to multiple \
standards, in which case you should extract both - note, double standards are most likely in close vicinity to each other. \
I will provide you with long textual sequences. Make absolutely sure that you only respond with phrases you find within \
the provided financial statement. \
Before providing an answer, check whether you can find it within the provided text.\n
"""

# Adjustment segmented documents
task_descr_old2 = """
You are tasked to extract information from the auditor section and the notes section that can be found within a financial statement document.\
More specifically, from the notes section you are tasked to extract according to what accounting standard \
the financial statement has been prepared, and from the auditor section you are tasked to extract what accounting \
standard the financial statement is in compliance with. \
It is possible that a financial statement is in compliance with or has been constructed according to multiple \
standards, in which case you should extract both - note, double standards are most likely in close vicinity to each other. \

I will provide you with smaller segments from longer textual sequences this means that it is often the case that none of the desired information is contained within one of the segments. 
Make absolutely sure that you only respond with phrases you find within the provided segment of a financial statement. \
Before providing an answer, check whether you can find it within the provided text.\n
"""

task_descr_auditor_1 = """
You are tasked to extract information that can be found within a financial statement document. \
More specifically, you are tasked to extract in accordance with which accounting standard the financial statement \
presents its information. It is possible that a financial statement presents its information in compliance with more \
than one accounting standard. In this case, you are tasked to extract all that standards that are mentioned.\
I will provide you with short text segments that have been extracted from a financial statement document. \
Make absolutely sure that you only respond with phrases you find within the provided financial statement. \
Before providing an answer, check whether you can find it within the provided text.\n
"""

task_descr_auditor_2 = """
You are tasked to extract information that can be found within a report of a company. \
More specifically, you are tasked to extract, according to the auditor's opinion, in accordance \
with which accounting standard the company prepared its financial statements, financial report, and/or annual report. \
It is possible that a report is in compliance with more than one accounting standard. \
In this case, you are tasked to extract all that standards that are mentioned. Please also make sure to list which document type \
has been prepared according to the standard, multiple are possible. Examples are: financial statements, consolidated financial statements, financial report, annual report. Please also make sure to not capture standards that refer to previous or upcoming years. \
Note that the auditor will most likely phrase their findings as an opinion. \
I will provide you with short text segments that have been extracted from a company's report. \
Make absolutely sure that you only respond with phrases you find within the provided financial statement. \
Before providing an answer, check whether you can find it within the provided text.\n
"""

task_descr_auditor_3 = """
You are tasked to extract information that can be found within a report of a company. \
More specifically, you are tasked to extract, according to the auditor's opinion, in accordance \
with which accounting standard, rules, or acts the company prepared its financial statements, financial report, and/or annual report. \
It is possible that a report is in compliance with more than one accounting standard. \
In this case, you are tasked to extract all that standards, rules, and/or acts that are mentioned. Please also make sure to list which document type \
has been prepared according to the standard, multiple are possible. Examples are: financial statements, consolidated financial statements, financial report, annual report. Please also make sure to not capture standards that refer to previous or upcoming years. \
Note that the auditor will phrase their findings as an opinion, so priotize sentences that start with either 'in our opinion' or 'in my opinion'. \
When you extract the accounting standard, rules, or acts make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules as accepted by the US, international financial reporting standard as \
provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
I will provide you with short text segments that have been extracted from a company's report. \
Make absolutely sure that you only respond with phrases and terms you find within the provided report. \
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a term make sure it is actually in the sentence you find.\n
"""

task_descr_auditor_4 = """
You are tasked to extract information that can be found within a report of a company. \
More specifically, you are tasked to extract, according to the auditor's opinion, in accordance \
with which accounting standard, rules, or acts the company prepared its financial statements, financial report, and/or annual report. \
Make sure to exclude auditing standards. \
It is possible that a report is in compliance with more than one accounting standard. \
In this case, you are tasked to extract all that standards, rules, and/or acts that are mentioned. Please also make sure to list which document type \
has been prepared according to the standard, multiple are possible. Examples are: financial statements, consolidated financial statements, financial report, annual report. Please also make sure to not capture standards that refer to previous or upcoming years. \
Note that the auditor will phrase their findings as an opinion, so priotize sentences that start with either 'in our opinion' or 'in my opinion'. \
When you extract the accounting standard, rules, or acts make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules as accepted by the US, international financial reporting standard as \
provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
I will provide you with short text segments that have been extracted from a company's report. \
Make absolutely sure that you only respond with phrases and terms you find within the provided report. \
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a term make sure it is actually in the sentence you find.\n
"""

task_descr_auditor_5 = """
You are tasked to extract information that can be found within a report of a company. \
More specifically, you are tasked to extract, according to the auditor's opinion, in accordance \
with which accounting standard, rules, practices, principles, or acts the company prepared its financial statements, financial report, and/or annual report. \
Make sure to exclude auditing standards. \
It is possible that a report is in compliance with more than one accounting standard. \
In this case, you are tasked to extract all that standards, rules, and/or acts that are mentioned. Please also make sure to list which document type \
has been prepared according to the standard, multiple are possible. Examples are: financial statements, consolidated financial statements, financial report, annual report. Please also make sure to not capture standards that refer to previous or upcoming years. \

Note that the auditor will phrase their findings as an opinion, so priotize sentences that start with either 'in our opinion' or 'in my opinion'. \
When you extract the accounting standard, rules, practices, principles, or acts make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as \
provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
I will provide you with short text segments that have been extracted from a company's report. \
Make absolutely sure that you only respond with phrases and terms you find within the provided report. \
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a term make sure it is actually in the sentence you find.\n
"""

task_descr_notes_3 = """
You are tasked to extract information that can be found within a report of a company. \
More specifically, you are tasked to extract in accordance with which accounting standard, rules, practices, principles, or acts the company \
presents/prepares  its financial statements, financial report, and/or annual report. \
Make sure to exclude opinions. \
It is possible that a report has been prepared in compliance with more than one accounting standard. \
In this case, you are tasked to extract all that standards, rules, and/or acts that are mentioned. Please also make sure to list which document type has \
been prepared according to the standard, multiple are possible. Examples are: financial statements, consolidated financial statements, financial report, \ 
annual report. Please also make sure to not capture standards that refer to previous or upcoming years. \
Note the company will never phrase it as an opinion. \
When you extract the accounting standard, rules, practices, principles, or acts make sure to extract also the provisions, jurisdictions, or issuance \
entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial \ reporting standard as \
provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
I will provide you with short text segments that have been extracted from a company's report. \
Make absolutely sure that you only respond with phrases and terms you find within the provided report. \
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a term make sure it is actually in the sentence you find.\n
"""

task_descr_notes_1 = """
You are tasked to extract information that can be found within a financial statement document. \
More specifically, you are tasked to extract in accordance with which accounting standard the financial statement \
has been prepared. It is possible that a financial statement has been prepared in compliance with more \
than one accounting standard. In this case, you are tasked to extract all that standards that are mentioned.\
I will provide you with short text segments that have been extracted from a financial statement document. \
Make absolutely sure that you only respond with phrases you find within the provided financial statement. \
Before providing an answer, check whether you can find it within the provided text.\n
"""

task_descr_notes_2 = """
You are tasked to extract information that can be found within a report of a company. \
More specifically, you are tasked to extract in accordance with which accounting standard the company presents its financial statements, financial report, and/or annual report. \
It is possible that a report has been prepared in compliance with more than one accounting standard. \
has been prepared. \
It is possible that a report is in compliance with more than one accounting standard. \
In this case, you are tasked to extract all that standards that are mentioned. Please also make sure to list which document type \
has been prepared according to the standard, multiple are possible. Examples are: financial statements, consolidated financial statements, financial report, annual report. Please also make sure to not capture standards that refer to previous or upcoming years. \
Note the company will never phrase it as an opinion. \
I will provide you with short text segments that have been extracted from a financial statement document. \
Make absolutely sure that you only respond with phrases you find within the provided financial statement. \
Before providing an answer, check whether you can find it within the provided text.\n
"""


# Common Terms :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## Terms commonly found around standard in auditor section
common_terms_section_auditor_old = """
For the auditor part you will most likely find some of these terms, delimited by tags (<auditor><\\auditor>) \
and separated by commas, in the vicinity of the information to be extracted: <auditor>{terms_auditor}<\\auditor>.
"""

## Terms commonly found around standard in notes section
common_terms_section_notes_old = """
Within the notes part you will most likely find some of these terms, delimited by tags (<notes><\\notes>) \
and separated by commas, in the vicinity of the information to be extracted: <notes>{terms_notes}<\\notes>.
"""

# Answer styles :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

answer_format_old1 = """
Answer in the following format:
{
"notes" : {
    "sentence" : "sentence from which you extracted the standard contained in the notes section",
    "term" : "accounting standard you found in the notes section"},
"audit" : {
    "sentence" : "sentence from which you extracted the standard contained in the auditor section",
    "term" : "accounting standard you found in the auditor section"}
}
"""

answer_format_old2 = """
Answer in one of the following formats:
- For the audit part:
{
"audit" : {
    "sentence" : "sentence from which you extracted the standard contained in the auditor section",
    "term" : "accounting standard you found in the auditor section"}
}
- For the notes part:
{
"notes" : {
    "sentence" : "sentence from which you extracted the standard contained in the notes section",
    "term" : "accounting standard you found in the notes section"}
}
- In case both parts are in teh same segment:
{
"notes" : {
    "sentence" : "sentence from which you extracted the standard contained in the notes section",
    "term" : "accounting standard you found in the notes section"},
"audit" : {
    "sentence" : "sentence from which you extracted the standard contained in the auditor section",
    "term" : "accounting standard you found in the auditor section"}
}
- In case neither the notes nor the audit section are contained within  the segment:
{
"no info": "no answer"
}
"""

answer_format_old3 = """
Answer in the following format:
{
"notes" : {"term": accounting standard you found in the notes section},
"audit": {"term": accounting standard extracted from the auditor section}
}
"""

## note segmented
answer_note_seg1 = """
Note in case a segment contains none of the information just answer with: "no info contained".
"""

### Split Format

answer_format_split_1 = """
Answer in the following format:
{
 "sentence" : "sentence from which you extracted the accounting standard",
 "term" : "accounting standard you extracted"
}
"""

answer_format_split_2 = """
Answer in the following format:
{
 "doc" : "dcoument type, which has been constructed according to the mentioned standard",
 "sentence" : "sentence from which you extracted the accounting standard, rule, or act",
 "term" : "accounting standard, rule, or act you extracted"
}
"""

# Instruction: :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
instruction_old = """ 
Please follow these instructions:
1) First read the financial statement.
2) Second find the sentence that contains the desired term.
3) Extract the desired term.
4) Make sure that the term you extract is acutally contained in the provided financial statement.
5) List both the term and the sentence from which you extracted the term.
"""

instruction_old_split = """ 
Please follow these instructions:
1) Read the segment of the financial statement.
2) Identify whether the segment contains the audit part, the notes part, both parts, or neither part.
3) Second find the sentence that contains the desired term and notes whether it is extracted from the \
audit part or the notes part.
4) Extract the desired term.
5) Double check that the term you extract is actually contained in the provided segment.
6) List both the term, the sentence, and what part you extracted the term from.
"""

instruction_1 = """
Please follow these instructions:
1) First read the financial statement segments.
2) Second find the sentence that contains the desired term.
3) Extract the desired term.
4) Make sure that the term you extract is actually contained in the provided financial statement segment.
5) List both the term and the sentence from which you extracted the term.
"""

instruction_2 = """
Please follow these instructions:
1) First read the financial statement segments.
2) Second find the sentence that contains the desired term.
3) Extract the desired term.
4) Make sure that the term you extract is actually contained in the provided financial statement segment.
5) List both the term and the sentence from which you extracted the term.
"""

instruction_3 = """
Please follow these instructions:
1) First read the company's report.
2) Second find the sentences that contain the desired information.
3) Extract the desired terms from the sentences.
4) Make sure that the term you extract is actually contained in the provided financial statement segment.
5) Make sure that each sentence abbides by the rules mentioned above else remove.
6) List both the term and the sentence from which you extracted the term.
"""

instruction_4 = """
Please follow these instructions:
1) First read the section of the company's report provided.
2) Second find the sentences that contain the desired information.
3) Extract the sentences and their desired terms from the report.
4) Make sure that the term you extract is actually contained in the provided report segment and the sentence you found.
5) Make sure that each sentence abbides by the rules mentioned above else reconsider.
6) List the document type, term, and sentence from which you extracted the document type and term.
"""