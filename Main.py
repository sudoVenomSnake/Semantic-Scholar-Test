import openai
import requests
from openai import OpenAI

import streamlit as st

st.title("Semantic Scholar Test")

@st.cache_data
def query(base_prompt):
    completion = openai.chat.completions.create(
        model = "gpt-4",
        messages = [
            {
                "role": "user",
                "content": base_prompt,
            },
        ],
    )
    response = completion.choices[0].message.content
    st.subheader("Generating Prompts -")
    st.text(response)
    return response

@st.cache_data
def get_semantic_scholar(i):
    return requests.get(f"http://api.semanticscholar.org/graph/v1/paper/search?query={i}&offset=1&limit=50&fields=title,abstract,authors,journal,publicationTypes,year,referenceCount,citationCount,influentialCitationCount,url")

user_prompt = st.text_input(label = "Please enter your prompt -")

if user_prompt:
    base_prompt = f"""This is the prompt that turns research question into queries:

Your are Jane Doe, a great research assistant. You help turning people's queries into query that is friendly to search engine, semantic scholar.

Think Step by step in XML, these are for you to take notes and think out loud and will not be shown to the user:

<thinking>
</thinking>

and give a simple searchable phrase in these XML tags:

<result>
</result>

An example for you is - 

User: Do lower caste and Dalit students have equitable access and representation in elite liberal arts universities in India?

Assistant:
<thinking>
The query is about the social dynamics of college admissions and demographics in India, particularly within the context of caste-based distinctions. It specifically targets "lower caste and Dalit" students in the context of "elite liberal arts" institutions. To make this query search-engine-friendly, we need to incorporate relevant keywords like "lower caste," "Dalit," "access," "representation," "elite institutions," "liberal arts colleges," and "India." Also, academic search engines like Semantic Scholar may have more precise articles when using terms like "equity" in education, "social inclusion," and "higher education caste disparities."
</thinking>

<result>
equity in education for Dalit and lower caste students at elite liberal arts colleges in India
</result>

user: break this query into multiple smaller queries

<thinking>
The initial query is complex because it touches multiple dimensions: caste ("lower caste" and "Dalit"), types of institutions ("elite liberal arts universities"), and the nature of access ("equitable access and representation"). Breaking this query into smaller components may help in finding more nuanced literature covering different aspects of the original query. Relevant search phrases should include variations that cover:
- The access of lower caste and Dalit students to higher education in general.
- Representation and demographics of these communities within elite institutions in India.
- Case studies or data on liberal arts institutions specifically.
- Research on educational equity and social stratification in the Indian context.
</thinking>

<result>
Dalit student enrollment in Indian higher education
lower caste representation in India's elite universities
liberal arts college demographics and caste in India
educational equity for marginalized communities in India
</result>

Start

User: {user_prompt}

<thinking>
</thinking>

<result>
</result>

break this query into multiple smaller queries

<thinking>
</thinking>

<result>
</result>

End
"""
    response = query(base_prompt)

    queries = response.split("<result>")[2].split("</result>")[0].split("\n")[1:-1]

    st.subheader("Semantic Scholar Responses -")
    for i in queries:
        response = get_semantic_scholar(i)
        st.write(response.json())