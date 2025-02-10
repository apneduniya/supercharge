

KNOWLEDGE_BASE_SYSTEM_PROMPT="""If the question's answer is not in the context, strictly say "I don't know".
"""


KNOWLEDGE_BASE_PROMPT="""You need to give a simple, formal and precise answer for the question asked by the user from this context.

CONTEXT:
{context}

QUESTION: 
{question}

ANSWER:
"""


SUPERTEAM_MEMBER_SYSTEM_PROMPT="""If you see no details of any person in the context, strictly say "I don't know".
"""

SUPERTEAM_MEMBER_PROMPT="""You need to give information of the person who fits best for the question asked by the user from people data context.

PEOPLE DATA CONTEXT:
{context}

USER QUESTION:
{question}

YOUR ANSWER:
"""


