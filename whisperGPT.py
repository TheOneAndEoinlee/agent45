# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 01:57:46 2023

@author: eoinl
"""

from langchain.llms import OpenAIChat
from langchain import PromptTemplate, LLMChain
import whisper
from listener import MyListener
    
model = whisper.load_model("small")

def setup_llm():
    llm = OpenAIChat(temperature=0)
    llm.set_verbose(True)
    
    template_steps = """Question: {question}
    
    Answer: Let's think step by step."""
    
    #template_sassy = """Question: {question}
    #
    #            Answer: The fuck did you say?"""
    
    prompt = PromptTemplate(template=template_steps, input_variables=["question"])
    prefix_messages_assistant = [{"role": "system", "content": "You are a helpful assistant that is very good at problem solving who thinks step by step."}]
    #prefix_messages_sassy = [{"role": "system", "content": "You are Janet, a sassy diva who only responds in sarcasm and profanity."}]
    llm = OpenAIChat(temperature=0, prefix_messages=prefix_messages_assistant)
    
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain
    #%%
    
def pushtotranscribe():
    
    print("Press and hold the 'r' key to begin recording")
    print("Release the 'r' key to end recording")
    with MyListener() as listener:
        listener.join()
  
    
  
    print("Recording Complete")
    #audio_file= open("output.wav", "rb")
    transcript = model.transcribe("output.wav")
    #transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(f"Transcription:{transcript['text']}")
    return(transcript)


#%%
llm_chain = setup_llm()
#%%
text = pushtotranscribe()
#%%
llm_chain.run(text['text'])

