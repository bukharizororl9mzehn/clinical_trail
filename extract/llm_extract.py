from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence

# Initialize the HuggingFace endpoint with your API token
llm = HuggingFaceEndpoint(
    endpoint_url="https://api-inference.huggingface.co/models/tiiuae/falcon-7b",
    huggingfacehub_api_token="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",
    temperature=0.5,
    max_new_tokens=512
)

# Define the prompt template
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Given the following clinical trial text, extract the following as JSON:
- Title
- Condition
- Phase
- Study Type
- Inclusion Criteria
- Exclusion Criteria

Text:
{text}

Respond in this format:
{{
  "title": "...",
  "condition": "...",
  "phase": "...",
  "study_type": "...",
  "inclusion_criteria": ["..."],
  "exclusion_criteria": ["..."]
}}
"""
)

# Combine prompt and LLM into a RunnableSequence
chain = prompt | llm

# Function to extract structured data
def extract_info(text: str):
    # Invoke the chain with the input text
    return chain.invoke({"text": text})
