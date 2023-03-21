from langchain.chains import LLMChain, ConversationChain, SequentialChain
from langchain.chains.base import Chain
from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate
)

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

chat = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(return_messages=True)


template="""You are an expert prompt engineer.      
      Craft an efficient prompt for specifying ANOTHER Large language model to embody the perfect role and personality required for the task. 
      The prompt should be short and efficient, but complete. Lay out a chain of thought process for each role to structure the responses.
        respond as follows:
"You are a [role].
[specification of roles and procedures]

Embody the perfect role and personality required for the task.
Begin by asking the user to specify the task they want to accomplish."
"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")

chat_prompt_template = ChatPromptTemplate.from_messages([system_message_prompt,MessagesPlaceholder(variable_name="history"), human_message_prompt])

prompting_chain = LLMChain(llm=chat, prompt=chat_prompt_template, output_key="prompt")

#expert_sytem_message = prompting_chain.run("designing my room")




class ExpertChain(ConversationChain,BaseModel):

    prompt= chat_prompt_template
    llm= chat
    memory= memory

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Call the chain."""
        #check if memory is empty
        if len(self.memory.chat_memory.messages) == 0:
            #if it is, then run the prompting chain
            self.prompt = chat_prompt_template
            #generate the expert system message

            expert_system_message = prompting_chain.run(inputs)
            print(expert_system_message)
            chat_template = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(expert_system_message),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}")])
            self.prompt = chat_template



        return super()._call(inputs)
    

if __name__ == "__main__":

    expert_chain = ExpertChain()

    print(expert_chain.run("creating my dnd character, I already have a concept but I want to flesh it out and make it unique"))




