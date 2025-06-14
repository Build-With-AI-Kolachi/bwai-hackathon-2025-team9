preprocessor_cleaning_template = """
You are provided a query. For the query, perform the following steps:   

Text Cleaning:

Normalize Input: Convert the query to lowercase, correct typos using legal dictionaries, and expand abbreviations (e.g., "Fed. R. Civ. P." becomes "Federal Rules of Civil Procedure").
Context Extraction: Identify any jurisdictional hints (e.g., "California labor law") or legal domains (e.g., "intellectual property").

Input: {query}

"input_text": the original query text.
"cleaned_text": the normalized and cleaned version of the query.
Important: Output only the JSON with no additional text or explanation.
"""

preprocessor_intent_extraction_template = """
You are provided a query. For the query, perform the following steps:


Intent Extraction:

Taxonomy: Classify the query into a legal intent (e.g., "contract dispute", "employment rights", "criminal defense").
Intent Fallback: If no clear legal intent is detected, assign a fallback intent (e.g., "jurisdiction clarification needed").

Input: {cleaned}

Return a JSON array where each element is an object containing the following keys:
"intent": the list of identified legal intents.

"""

preprocessor_template = """
You are provided a query. For the query, perform the following steps:

Text Cleaning:
Normalize Input: Convert the query to lowercase, correct typos, and expand abbreviations.

Format: {format_instructions}

Input: {query}
"""

analysis_template = """
You are provided a WhatsApp message. For the message, perform the following steps:

*) Analyze the Message:
- Assess the content and context of the message
- Identify if it's a customer inquiry, complaint, or general message

*) Message Classification:
Classify the message as one of the following:
- account_management
- product_info
- general

*) Identify the Priority Level:
- High Priority: Urgent issues affecting service/product usage
- Medium Priority: Non-urgent but important inquiries
- Low Priority: General questions or non-critical issues
- Needs Clarification: Unclear or ambiguous messages requiring more information

Format: {format_instructions}

Input: {query}
"""




# ==================== 
# Old Preprocessing Prompt
# ====================
"""Text Cleaning:
Normalize Input: Convert the query to lowercase, correct typos using legal dictionaries, and expand abbreviations (e.g., "Fed. R. Civ. P." becomes "Federal Rules of Civil Procedure").
Context Extraction: Identify any jurisdictional hints (e.g., "California labor law") or legal domains (e.g., "intellectual property").

Intent Extraction:
Taxonomy: Classify the query into a legal and non-legal (e.g., legal = "contract dispute", "employment rights", "criminal defense" etc).
Intent Fallback: If no clear legal intent is detected, assign a general intent (e.g., "jurisdiction clarification needed")."""

"""
sUBcATEGORY 
# Examples:
# 1) Hi! Can you help me with Commercial Document Evidence Act? Statutory Interpretation
# 2) What are the side effects of aspirin? Medication Information
# 3) How can I fix a 404 error on my website? Web Development
# 4) Can you help me with a legal issue? Needs Clarification
# 5) Hey! How's your day going? Casual Conversation
# """
# ===================


tool_calling_template = """
You are a helpful assistant.
Make sure to use the `vector_retriever_tool` tool for searching information from documents.

("placeholder", "{chat_history}"),
("human", "{input}"),
("placeholder", "{agent_scratchpad}"),
"""

finding_absolutes_template = """
You are a helpful assistant.
You are required to find absolutes in the given text (i.e., words that are absolute in nature like `always` etc).


format: {format_instructions}
analysis: {analysis}

"""

general_prompt = """
Respond to the following question concisely:

Question: {query}
Answer:
"""