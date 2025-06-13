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

task_descr_auditor_6 = """
You are tasked to extract information that can be found within a report of a company. \
More specifically, you are tasked to extract, according to the auditor's opinion, in accordance \
with which accounting standard, rules, practices, principles, or acts the company prepared its financial statements, financial report, and/or annual report. \
Make sure to exclude auditing standards. It is possible that a report is in compliance with more than one accounting standard. \
In this case, you are tasked to extract all that standards, rules, and/or acts that are mentioned. Please also make sure to list which document type \
has been prepared according to the standard, multiple are possible. Examples are: financial statements, consolidated financial statements, financial report, annual report. Please also make sure to not capture standards that refer to previous or upcoming years. \
Note that the auditor will phrase their findings as an opinion, so priotize sentences that start with either 'in our opinion' or 'in my opinion'. \
Make absolutely sure to ignore paragraphs about the opinion of the director/s and also make sure to ignore information about remuneration reports. \
When you extract the accounting standard, rules, practices, principles, or acts make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as \
provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
Sometimes consecutive sentences contain additional standards that are of importance, make sure to record them aswell. \
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
Make sure that it is not the opinion of the director/s. Also make sure to ignore remuneration reports. \
When you extract the accounting standard, rules, practices, principles, or acts make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as \
provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
Sometimes consecutive sentences contain additional standards that are of importance, make sure to record them aswell. \
I will provide you with short text segments that have been extracted from a company's report. \
Make absolutely sure that you only respond with phrases and terms you find within the provided report. \
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a term make sure it is actually in the sentence you find.\n
"""



task_descr_auditor_7 = """
You are tasked to extract information that can be found within a report of a company. \
More specifically, you are tasked to extract, according to the auditor's opinion, in accordance \
with which accounting standard, rules, practices, principles, or acts the company prepared its financial statements, financial report, and/or annual report. \
Make sure to exclude auditing standards. It is possible that a report is in compliance with more than one accounting standard. \
In this case, you are tasked to extract all that standards, rules, and/or acts that are mentioned. Please also make sure to list which document type \
has been prepared according to the standard, multiple are possible. Look for close variants of following document types: financial statements, consolidated financial statements, financial report, annual report. Please also make sure to not capture standards that refer to previous or upcoming years. \
Make sure to ignore remuneration reports. \
Note that the auditor will phrase their findings as an opinion, so priotize sentences that start with either 'in our opinion' or 'in my opinion'. \
Make absolutely sure to ignore sentences about the opinion of the directors.\
When you extract the accounting standard, rules, practices, principles, or acts make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as \
provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
Sometimes consecutive sentences contain additional standards that are of importance, make sure to record them aswell. \
I will provide you with short text segments that have been extracted from a company's report. \
Make absolutely sure that you only respond with phrases and terms you find within the provided report. \
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a term make sure it is actually in the sentence you find.\n
"""

task_descr_auditor_8 = """
From a company report you are tasked to extract, according to the auditor's opinion, in accordance \
with which accounting standards/rules/practices/principles/acts the company prepared its document types. \
Document types can be in compliance with more than one accounting standard. Please also make sure to list which document type \
has been prepared according to which standards, multiple are possible. Look for close variants of the following document types: financial statements, consolidated financial statements, financial report, and annual report. Please also make sure to not capture standards that refer to previous or upcoming years. Make sure to ignore remuneration reports. \
Note that the auditor will phrase their findings as an opinion, priotize sentences that start with either 'in our opinion' or 'in my opinion'. \
Important, do not catch the directors' opinion, we only care about the auditor's opinion.\
When you extract the accounting standard make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
Sometimes consecutive sentences contain additional standards that apply, record them with the previous sentence only if the document type is referred to via a demonstrative pronoun. \
Make absolutely sure that you only respond with senteces, document types, and terms you find within the provided report. \
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a document type and term make sure it is actually in the sentence you find.\n
"""

task_descr_auditor_9 = """
From a company report you are tasked to extract, according to the auditor's opinion, in accordance \
with which accounting standards/rules/practices/principles/acts the company prepared its document types. \
Document types can be in compliance with more than one accounting standard. Please also make sure to list which document type \
has been prepared according to which standards, multiple are possible. Look for close variants of the following document types: financial statements, consolidated financial statements, financial report, and annual report. Please also make sure to not capture standards that refer to previous or upcoming years. Make sure to ignore remuneration reports. \
Note that the auditor will phrase their findings as an opinion, priotize sentences that start with 'in our opinion' or 'in my opinion'. \
Important, ignore the opinion of directos, we only care about the opinion of auditors.\
When you extract the accounting standard make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
Make absolutely sure that you only respond with senteces, document types, and terms you find within the provided report. \
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a document type and term make sure it is actually in the sentence you find.\n
"""

task_descr_auditor_10 = """
From a company report you are tasked to extract, according to the auditor's opinion, in accordance with which accounting standards/rules/practices/principles/acts the company prepared its document types. Document types can be in compliance with more than one accounting standard. Please also make sure to list which document type has been prepared according to which standards, multiple are possible. Look for close variants of the following document types: financial statements, consolidated financial statements, financial report, and annual report. Please also make sure to not capture standards that refer to previous or upcoming years. Make sure to ignore remuneration reports. Note that the auditor will phrase their findings as an opinion, priotize sentences that start with 'in our opinion' or 'in my opinion'. Important, ignore the opinion of directos, we only care about the opinion of auditors. When you extract the accounting standard make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure it is actually in the provided text and when you find a document type and term make sure it is actually in the sentence you find.\n
"""

task_descr_auditor_11 = """
From a company report you are tasked to extract, according to the auditor's opinion, with which accounting standards/rules/practices/principles/acts the company prepared its document types. \
Please also make sure to list which document type has been prepared according to which standards, multiple are possible. Look for close variants of the following document types: financial statements, consolidated financial statements, financial report, and annual report. Please also make sure to not capture standards that refer to previous years. Make sure to ignore remuneration reports. \
Note that the auditor will phrase their findings as an opinion, priotize sentences that start with 'in our opinion' or 'in my opinion'. \
Important, ignore the opinion of directos, we only care about the opinion of auditors.\
When you extract the accounting standard make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a document type and term make sure it is actually in the sentence you find.\n
"""

task_descr_auditor_12 = """
From a company report you are tasked to extract, according to the auditor's opinion, in compliance with which accounting standards/rules/practices/principles/acts the company prepared its document types. \
Document types can be prepared in accordance with more than one accounting standard. Please also make sure to list which document type has been prepared according to which standards, multiple are possible. \
Look for close variants of the following document types: financial statements, consolidated financial statements, financial report, and annual report. 
Note that the auditor will usually phrase their findings as an opinion, priotize sentences that start with 'in our opinion' or 'in my opinion'. \
When you extract the accounting standard make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
Make sure to ignore sentences that refer to prior applications of standards. Make sure to ignore sentences about remuneration reports. \
Make sure to ignore the opinion of directors.\
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a document type and term make sure it is actually in the sentence you find.\n
"""

task_descr_auditor_13 = """
You are given a segment from a company’s report. Your task is to extract, based on the auditor’s opinion, which accounting standards, rules, practices, principles, or acts were used to prepare specific document types. Follow the instructions below strictly.

🎯Target document types (variations allowed):
- Financial statements
- Consolidated financial statements
- Financial report
- Annual report

📌 Extraction Criteria:
- Identify and include only sentences that explicitly state the accounting standards used to prepare one of the above document types.
- Sentences prefaced by "in our opinion" or "in my opinion" should be prioritized.
- Extract the full name of the accounting standard, along with associated provisions, jurisdictions, or issuing entities.
  - Examples: "IFRS as issued by the IASB", "Generally Accepted Accounting Principles in India", "IFRS as adopted by the EU", “GAAP in New Zealand”, “MFRS as issued by MASB”
- If multiple standards apply, list them all.

🚫 Ignore:
- Sentences about prior or historical application of standards
- Sentences about remuneration reports
- Opinions of directors and management (non-auditors)

🧠 Validation:
- Ensure all extracted elements (sentence, document type, and accounting terms) **exist in the provided text**.
- Don’t infer or hallucinate any term or standard not found explicitly.
"""

task_descr_notes_7 = """
You are given a segment from a company’s report. Your task is to extract, based on general report statements (not from an auditor), which accounting standards, rules, practices, principles, or acts were used to prepare specific document types. Follow the instructions below strictly.

🎯 Target document types (variations allowed):

 - Financial statements
 - Consolidated financial statements
 - Financial report
 - Annual report

📌 Extraction Criteria:
 - Identify and include only sentences that explicitly state the accounting standards used to prepare one of the above document types.
 - Extract the full name of the accounting standard or rule, including jurisdictions, legal acts, or issuing entities when mentioned.
  - Examples: “IFRS as issued by the IASB”, “Generally Accepted Accounting Principles in India”, “MFRS as issued by MASB”. “IFRS as adopted by the EU”
- If multiple standards apply, list them all.

🚫 Ignore:
 - Sentences about prior or historical application of standards
 - Sentences about remuneration reports
 - Opinions (i.e. statements made by auditors)

🧠 Validation:
- Ensure all extracted elements (sentence, document type, and accounting terms) **exist in the provided text**.
- Don’t infer or hallucinate any term or standard not found explicitly.
"""

task_descr_notes_6 = """
From a company report you are tasked to extract in accordance with which accounting standard/rules/practices/principles/acts \
the company prepares its document types. Document types can be prepared in accordance with more than one accounting standard.
Please also make sure to list which document type has been prepared according to which standards, multiple are possible.
Look for close variants of the following document types: financial statements, consolidated financial statements, financial report, and annual report.
When you extract the accounting standard make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it.
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings.
Make sure to ignore sentences that refer to prior or upcoming applications of standards.
Make sure to ignore sentences about remuneration reports and opinions.
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a document type and term make sure it is actually in the sentence you find.\n
"""

task_descr_notes_5_2 = """
From a company report you are tasked to extract in accordance with which accounting standard/rules/practices/principles/acts \
the company prepares its document types. Document types can be prepared in accordance with more than one accounting standard. Please also make sure to list which document type has been prepared according to which standards, multiple are possible. Look for close variants of the following document types: financial statements, consolidated financial statements, financial report, and annual report.
When you extract the accounting standard make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it.
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings.
Make sure to ignore sentences that refer to prior applications of standards.
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a document type and term make sure it is actually in the sentence you find.\n
"""

task_descr_notes_5 = """
From a company report you are tasked to extract in accordance with which accounting standard/rules/practices/principles/acts \
the company prepares its document types. Document types can be prepared in accordance with more than one accounting standard. Please also make sure to list which document type has been prepared according to which standards, multiple are possible. Look for close variants of the following document types: financial statements, consolidated financial statements, financial report, and annual report.
When you extract the accounting standard make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it.
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings.
Make sure to ignore sentences that refer to prior applications of standards. Make sure to ignore sentences about remuneration reports and opinions. 
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a document type and term make sure it is actually in the sentence you find.\n
"""

task_descr_notes_4 = """
From a company report you are tasked to extract in accordance with which accounting standard/rules/practices/principles/acts \
the company prepares its document types. Document types can be prepared in accordance with more than one accounting standard. \
Please also make sure to list which document type has been prepared according to which standards, multiple are possible. \
Look for close variants of the following document types: financial statements, consolidated financial statements, financial report, and annual report. Please also make sure to not capture standards that refer to previous or upcoming years. Make sure to ignore remuneration reports and opinions. \
When you extract the accounting standard make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it. \
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a document type and term make sure it is actually in the sentence you find.\n
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
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial \
reporting standard as \
provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings. \
Sometimes consecutive sentences contain additional standards that are of importance, make sure to record them aswell. \
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
 "doc" : "document type, which has been constructed according to the mentioned standard",
 "sentence" : "sentence from which you extracted the accounting standard, rule, or act",
 "term" : "accounting standard, rule, or act you extracted"
}
"""

answer_format_split_3 = """
Answer in the following format:
{
 "doc" : ["dcoument type, which has been constructed according to the mentioned standard"],
 "sentence" : ["sentence from which you extracted the accounting standard, rule, or act"],
 "term" : ["first accounting standard, rule, or act; second accounting standard, rule, or act"]
}
"""

answer_format_split_4 = """
Answer in the following format:
{"sentence" : ["sentence from which you extracted the accounting standard, rule, or act"],
 "doc" : ["1st document type"],
 "term" : ["1st accounting standard/rule/act"; ...; "n-th accounting standard/rule/act"]}
 
 ...

{"sentence" : ["sentence from which you extracted the accounting standard/rule/or act"],
 "doc" : ["m-th document type"],
 "term" : ["1st accounting standard/rule/act"; ...; "k-th accounting standard/rule/act"]}
"""

answer_format_split_5 = """
Answer in the following format:
{"sentence" : ["sentence from which you extracted the accounting standard, rule, or act"],
 "doc" : ["1st document type"],
 "term" : ["1st accounting standard/rule/act", ..., "n-th accounting standard/rule/act"]}

 ...

{"sentence" : ["sentence from which you extracted the accounting standard/rule/or act"],
 "doc" : ["m-th document type"],
 "term" : ["1st accounting standard/rule/act", ..., "k-th accounting standard/rule/act"]}
"""

answer_format_split_6 = """
📤 Output Format (JSON, repeat block for each found and valid document type):
{
  "sentence": ["<exact sentence from the text>"],
  "doc": ["<document type mentioned>"],
  "term": ["<accounting standard / rule / act>"; ...]
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

instruction_5 = """
Please follow these instructions:
1) First read the section of the company's report provided.
2) Second find the sentences that contain the desired information.
3) Extract the sentences and their desired terms from the report.
4) Make sure that the term you extract is actually contained in the provided report segment and the sentence you found.
5) Make sure that each sentence abbides by the rules mentioned above else reconsider.
6) List each sentence with its contained document type and terms in the below json format.
"""

instruction_6 = """
Please follow these instructions:
1) First read the section of the company's report provided.
2) Second find the sentences that contain the desired information.
3) Extract the sentences and their desired document types and terms.
4) Make sure that the term you extract is actually contained in the provided report segment and the sentence you found.
5) Make sure that each sentence abbides by the rules mentioned above else reconsider.
6) List each sentence with its contained document type and terms in the below json format.
"""

instruction_7 = """
Please follow these instructions:
1) First read the section of the company's report provided.
2) Second find the sentences that contain the desired information.
3) Extract the sentences and their desired document types and terms.
4) Make sure that the term you extract is actually contained in the provided report segment and the sentence you found.
5) Make sure that each sentence abbides by the rules mentioned above the instruction, otherwise remove it.
6) List each sentence with its contained document type and terms in the below json format.
"""

instruction_8_audit = """
👣 Step-by-Step Instructions:
1) Read the provided section carefully.
2) Identify sentences containing the relevant auditor opinion and financial document type.
3) Extract the full sentence, the document type(s) mentioned, and the full accounting standard(s) cited.
4) Confirm that all terms you extract are explicitly present in the sentence and source text.
5) Discard any sentence that violates the exclusion criteria.
6) Format your output as shown below, repeating for each valid sentence and document type.
"""

instruction_8_notes = """
👣 Step-by-Step Instructions:
 1) Read the provided section carefully.
 2) Identify sentences that mention both a document type and the accounting standard(s) it follows.
 3) Extract the full sentence, the document type(s) mentioned, and the full accounting standard(s) cited.
 4) Confirm that all terms you extract are explicitly present in the sentence and source text.
 5) Discard any sentence that violates the exclusion criteria.
 6) Format your output as shown below, repeating for each valid sentence and document type.
"""