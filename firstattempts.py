# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 15:49:38 2023

@author: eoinl
"""
import langchain as lc
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
I want you to act as a naming consultant for new companies.

Here are some examples of good company names:

- search engine, Google
- social media, Facebook
- video sharing, YouTube

The name should be short, catchy and easy to remember.

What is a good name for a company that makes {product}?
"""

prompt = PromptTemplate(
    input_variables=["product"],
    template=template,
)

llm = OpenAI(temperature=0.9)
