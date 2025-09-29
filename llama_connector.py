import json, re
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from models import ActionPlan

MODEL_NAME = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=256)
llm = HuggingFacePipeline(pipeline=pipe)

TEMPLATE = """
Convert the following telecom user query into JSON.
Supported actions: list_offers, get_offer, place_order, get_customer_info, get_usage, get_balance.
Return JSON with keys: action, id (optional), filters (optional).
User: {query}
"""

prompt = PromptTemplate(input_variables=["query"], template=TEMPLATE)
chain = LLMChain(llm=llm, prompt=prompt)

def query_to_action_plan(user_query: str) -> ActionPlan:
    raw = chain.run(query=user_query)
    try:
        obj = json.loads(re.search(r"\{.*\}", raw, re.S).group())
    except Exception:
        obj = {"action": "list_offers", "filters": {}}
    return ActionPlan(**obj)
