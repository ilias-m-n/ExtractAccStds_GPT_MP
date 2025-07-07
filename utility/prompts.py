# System Context Messages   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
system_context_basic1 = """
You are a financial accountant.
"""

# Task Description Auditor:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

task_descr_auditor_15 = """
You are given a segment from a company report.
Your task is to extract, based only on explicit statements from the auditor’s opinion, which accounting standards, rules, practices, principles, or acts were used to prepare certain document types.

Target document types (including close variants/extensions such as "... of the company/group", "company/group ...", "statutory ...", etc):
- financial statements
- consolidated financial statements
- financial report
- annual report

Extraction Instructions:
Extract only sentences that clearly state, in the auditor’s opinion, which accounting standard(s) were used for any target document type.
Only include a document type if the auditor’s opinion explicitly mentions both the document type and an applied accounting standard/rule.
Prioritize sentences beginning with “in our opinion” or "in my opinion".
Extract the full name of each standard or rule, including any jurisdiction, act, provision, or issuer (e.g., “IFRS as adopted by the EU”, “Generally Accepted Accounting Principles in India”).
If multiple standards are stated for a document type, extract them all.
Ignore: prior period applications, remuneration reports, management or director opinions, or any inference not verbatim in the text.
Exclude company names.

Validation:
All extracted document types, standards, and sentences must match exactly as in the text - do not infer, summarize, or paraphrase.

Step-by-Step Instructions:
1. Read the provided section carefully.
2. For each target document type, find sentences in the auditor’s opinion that explicitly mention both the document type and the standard(s) it’s prepared in accordance with.
3. For each target document type, extract the sentence and the full name(s) of the standard(s)/rule(s).
4. Confirm all extracted content is explicit and compliant with the above rules.
5. Discard any sentences that don’t fully meet requirements.
6. Format output as below, grouping by document type.
"""

task_descr_notes_15 = """
You are given a segment from a company report. 
Your task is to extract, based only on explicit, non-auditor statements, which accounting standards, rules, practices, principles, or acts were used to prepare certain document types.

Target document types (including close variants/extensions such as "... of the company/group", "company/group ...", "statutory ...", etc):
- financial statements
- consolidated financial statements
- financial report
- annual report

Extraction Instructions:
Extract only sentences that clearly state the accounting standard(s) applied to any target document type.
Only include a document type if the segment explicitly mentions both the document type and an applied accounting standard/rule.
Extract the full name of each standard or rule, including jurisdiction, act, provision, or issuer (e.g., “IFRS as adopted by the EU”, “Generally Accepted Accounting Principles in India”).
If multiple standards are stated for a document type, extract them all.
Ignore: prior period applications, remuneration reports, auditor opinions, or any inference not verbatim in the text.
Exclude company names.

Validation:
All extracted document types, standards, and sentences must match exactly as in the text - do not infer, summarize, or paraphrase.

Step-by-Step Instructions:
1. Read the provided section carefully.
2. For each target document type, find sentences explicitly mentioning both the document type and the standard(s) it’s prepared in accordance with.
3. For each target document type, extract the sentence and the full name(s) of the standard(s)/rule(s).
4. Confirm all extracted content is explicit and compliant with the above rules.
5. Discard any sentences that don’t fully meet requirements.
6. Format output as below, grouping by document type.
"""

# Answer Format :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

answer_format_8 = """
Output Format (JSON, repeat block for each valid document type):
{
  "document_type_1": [
    {
      "sentence": "Sentence where document_type_1 is mentioned with accounting_standard_A.",
      "terms": ["accounting_standard_A"]
    },
    {
      "sentence": "Sentence where document_type_1 is mentioned with accounting_standard_B and accounting_standard_C.",
      "terms": ["accounting_standard_B", "accounting_standard_C"]
    }
  ],
  "document_type_2": [
    {
      "sentence": "Sentence where document_type_2 is mentioned with accounting_standard_D.",
      "terms": ["accounting_standard_D"]
    }
  ]
}
"""

# Instruction: :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::





# Old

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

🎯Target document types (including close variants and extensions):
- financial statements (including forms such as “financial statements of the company,” “company financial statements”)
- consolidated financial statements (including forms such as “consolidated financial statements for the group”)
- financial report (including forms such as “company financial report”)
- annual report (including forms such as “annual report of the group”)

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

task_descr_auditor_14 = """
You are given a segment from a company report. 
Your task is to extract, based on the auditor’s opinion, which accounting standards, rules, practices, principles, or acts were used to prepare specific document types. 
Only consider what is stated explicitly in the text.

Target document types (including close variants and extensions):
- financial statements (including forms such as “financial statements of the company,” “company financial statements”)
- consolidated financial statements (including forms such as “consolidated financial statements for the group”)
- financial report (including forms such as “company financial report”)
- annual report (including forms such as “annual report of the group”)

Extraction Instructions:
Only extract sentences that clearly state, according to the auditor’s opinion, which accounting standards were used for any of the above document types.
Prioritize sentences beginning with “in our opinion” or “in my opinion.”
Extract the full name of the accounting standard or rule, including any jurisdiction, legal act, provisions, or issuing entity if mentioned (e.g., “IFRS as issued by the IASB”, “IFRS as adopted by the EU”, “Generally Accepted Accounting Principles in India”, etc.).
If a document type is prepared in accordance with multiple standards, list all that apply.
Ignore sentences about previous application of standards, remuneration reports, or opinions of directors or management.

Validation:
Ensure every extracted sentence, document type, and accounting term is found verbatim in the provided text.
Do not infer or supply terms or standards not explicitly stated in the text.
"""

# Task Description Notes :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

task_descr_notes_8 = """
You are given a segment from a company report. 
Your task is to extract, based on general report statements (not auditor opinions), which accounting standards, rules, practices, principles, or acts were used to prepare certain document types. 
Only consider what is stated explicitly in the text.

Target document types (including close variants and extensions):
- financial statements (including forms such as “financial statements of the company,” “company financial statements”)
- consolidated financial statements (including forms such as “consolidated financial statements for the group”)
- financial report (including forms such as “company financial report”)
- annual report (including forms such as “annual report of the group”)

Extraction Instructions:
Only extract sentences that clearly state the accounting standards used for any of the above document types.
Extract the full name of the accounting standard or rule, including any jurisdiction, legal act, provisions, or issuing entity if mentioned (e.g., “IFRS as issued by the IASB”, “IFRS as adopted by the EU”, “Generally Accepted Accounting Principles in India”, etc.).
If a document type is prepared in accordance with multiple standards, list them all.
Ignore sentences about previous application of standards, remuneration reports, or any auditor opinions.

Validation:
Ensure every extracted sentence, document type, and accounting term is found verbatim in the provided text.
Do not infer or supply terms or standards not explicitly stated in the text.
"""

task_descr_notes_7 = """
You are given a segment from a company’s report. Your task is to extract, based on general report statements (not from an auditor), which accounting standards, rules, practices, principles, or acts were used to prepare specific document types. Follow the instructions below strictly.

🎯Target document types (including close variants and extensions):
- financial statements (including forms such as “financial statements of the company,” “company financial statements”)
- consolidated financial statements (including forms such as “consolidated financial statements for the group”)
- financial report (including forms such as “company financial report”)
- annual report (including forms such as “annual report of the group”)

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

task_descr_notes_5 = """
From a company report you are tasked to extract in accordance with which accounting standard/rules/practices/principles/acts \
the company prepares its document types. Document types can be prepared in accordance with more than one accounting standard. Please also make sure to list which document type has been prepared according to which standards, multiple are possible. Look for close variants of the following document types: financial statements, consolidated financial statements, financial report, and annual report.
When you extract the accounting standard make sure to extract also the provisions, jurisdictions, or issuance entities that apply to it.
For example, IFRS as provided by the EU, generally accepted accounting rules/principles/practices as accepted by/in a country, international financial reporting standard as provisioned in the act, International Financial Reporting Standards as issued by the International Accounting Standards Board, and other phrasings.
Make sure to ignore sentences that refer to prior applications of standards. Make sure to ignore sentences about remuneration reports and opinions. 
Before providing an answer, check whether you can find it within the provided text. This means when you find a sentence make sure \
it is actually in the provided text and when you find a document type and term make sure it is actually in the sentence you find.\n
"""

instruction_6 = """
Please follow these instructions:
1) First read the section of the company's report provided.
2) Second find the sentences that contain the desired information.
3) Extract the sentences and their desired document types and terms.
4) Make sure that the term you extract is actually contained in the provided report segment and the sentence you found.
5) Make sure that each sentence abides by the rules mentioned above else reconsider.
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

instruction_9_audit = """
1. Read the provided section carefully.
2. Find sentences where the auditor gives an opinion about accounting standards used for a document type.
3. Extract the complete sentence, the relevant document type(s), and the full accounting standard(s) as stated.
4. Confirm that all extracted information is explicitly present in the source text and matches the requirements above.
5. Discard any sentences that do not comply.
6: Format your output as shown below.
"""

instruction_9_notes = """
1. Read the provided section carefully.
2. Identify sentences that mention both a target document type and the accounting standard(s) it is prepared in accordance with.
3. Extract the complete sentence, the relevant document type(s), and the full accounting standard(s) as stated.
4. Confirm that all extracted information is explicitly present in the source text and matches the requirements above.
5. Discard any sentences that do not comply.
6: Format your output as shown below.
"""

answer_format_split_4 = """
Provide your answer in the following JSON format:
{1: {"sentence" : ["sentence from which you extracted the accounting standard, rule, or act"],
 "doc" : ["1st document type"],
 "term" : ["1st accounting standard/rule/act"; ...; "n-th accounting standard/rule/act"]},
 ...
m: {"sentence" : ["sentence from which you extracted the accounting standard/rule/or act"],
 "doc" : ["m-th document type"],
 "term" : ["1st accounting standard/rule/act"; ...; "k-th accounting standard/rule/act"]}}
"""

answer_format_split_6 = """
📤 Output Format (JSON, repeat inner block for each found and valid document type):
{0: {  "sentence": ["<exact sentence from the text>"],
  "doc": ["<document type mentioned>"],
  "term": ["<accounting standard / rule / act>"; ...]},
 1: {  "sentence": ["<exact sentence from the text>"],
  "doc": ["<document type mentioned>"],
  "term": ["<accounting standard / rule / act>"; ...]},
  ...
}
"""

answer_format_split_7 = """
Output Format (JSON, repeat inner block for each found and valid document type)
{0: {  "sentence": ["<exact sentence from the text>"],
  "doc": ["<document type mentioned>"],
  "term": ["<accounting standard / rule / act>"; ...]},
 1: {  "sentence": ["<exact sentence from the text>"],
  "doc": ["<document type mentioned>"],
  "term": ["<accounting standard / rule / act>"; ...]},
  ...
}
"""