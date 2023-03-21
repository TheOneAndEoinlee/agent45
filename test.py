#function that returns the number of lines of a text file
def number_of_lines(filename=""):
    with open(filename, encoding='utf-8') as f:
        return len(f.readlines())
    
from langchain import (ChatPromptTemplate, 
                       HumanMessagePromptTemplate,
                       MessagesPlaceholder,
                       SystemMessagePromptTemplate,
                       AIMessagePromptTemplate)

def savePromptToJSON(prompt, filename="prompt.json"):
    with open(filename, 'w') as f:
        f.write(prompt.json())

def loadPromptFromJSON(filename="prompt.json"):