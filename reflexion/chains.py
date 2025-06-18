from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from reflexion.schema import AnswerQuestion, ReviseAnswer
from langchain_core.output_parsers.openai_tools import PydanticToolsParser, JsonOutputToolsParser
import datetime
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
load_dotenv()
# Actor Agent Prompt 
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert AI researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. After the reflection, **list 1-3 search queries separately** for researching improvements. Do not include them inside the reflection.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format. ONLY return valid JSON. Do not add explanations or extra text."),
    ]
).partial(time=datetime.datetime.now().isoformat())


responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer"
)


#configuring the llm:
key=os.getenv("KEY")
if key is None:
    raise ValueError("API key not found. Please set the KEY environment variable.")
else:
    print("API key found and loaded successfully." + key)
llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=key,
    model_name="mistralai/devstral-small:free"
    
)
responder_parser=PydanticToolsParser(tools=[AnswerQuestion])
# responder_chain = responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")| responder_parser

responder_chain = responder_prompt_template | llm.with_structured_output(AnswerQuestion)



# response=responder_chain.invoke({
#     "messages":[
#         HumanMessage(
#             content="What is the impact of climate change on global food security?"
#         )
#     ]
# })

# print(response.answer)




# ----------------REVISOR--------------
revise_instructions = """Revise your previous answer using the new information from the tool message and AI message.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""

revisor_chain = actor_prompt_template.partial(
    first_instruction=revise_instructions
) | llm.with_structured_output(ReviseAnswer)


# response=revisor_chain.invoke({
#     "messages":[
#         HumanMessage(
#             content='{"answer": "Climate change significantly impacts global food security by altering agricultural productivity, affecting crop yields, and disrupting food supply chains. Rising temperatures, changing precipitation patterns, and increased frequency of extreme weather events lead to reduced agricultural output, particularly in vulnerable regions. For instance, studies indicate that a 1°C increase in global temperature could reduce wheat yields by up to 6% in some areas. Additionally, climate change exacerbates water scarcity, further threatening food production. The World Bank estimates that by 2050, up to 122 million people could be pushed into extreme poverty due to climate-related impacts on agriculture. Therefore, addressing climate change is crucial for ensuring food security and preventing widespread hunger.", "search_queries": ["impact of climate change on agriculture", "climate change effects on crop yields", "food security and climate change"], "reflection": {"missing": "The answer lacks specific examples of crops affected by climate change.", "superfluous": "The answer includes general statements without citing specific studies or data."}}',
           
#         )
#     ]
# })



# print(response)