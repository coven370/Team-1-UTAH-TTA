
#To run the API run 
#uvicorn app:app
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from ollama import chat
from ollama import ChatResponse
from rag import perform_search

app = FastAPI()

AI_MODEL = 'deepseek-r1:8b'
class Prompt(BaseModel):
    messages: List[Dict[str,str]]
    metda_data: Optional[str] = None#Optional string for now
    
    
@app.get('/api/generate')
async def generate(prompts: Prompt):
    '''Generates according to the prompts passed in. It will return plain text to stream it. 
    
    Here is a example of the JSON format that is sent in.
        
        {
    "model": "llama3",           // Required: Name of the model to use
    "messages": [                // Required: Array of message objects
        {
        "role": "system",        // Role: system, user, or assistant
        "content": "You are a helpful assistant"
        },
        {
        "role": "user",
        "content": "Hello, how are you?"
        },
        {
        "role": "assistant",
        "content": "I'm doing well, thank you for asking!"
        },
        {
        "role": "user",
        "content": "What can you help me with today?"
        }
    ],
    "stream": false,             // Optional: Whether to stream the response
    "options": {                 // Optional: Same options as generate API
        "temperature": 0.7,
        "top_p": 0.9,
        "num_predict": 256
    }
    }
    '''
    
    print(prompts)
    
    async def prompt_gen(prompts):
        
        #We can add more cotnext to more stuff but we will figure that out later. 
        prompts.messages[-1]['content'] = prompts.messages[-1]['content'] + f'\n Here is the context for this request: {perform_search(prompts.messages[-1], 10)[0]}'
        stream: ChatResponse = chat(model=AI_MODEL, messages=prompts.messages, stream=True)
        
        for chunk in stream:
            yield chunk['message']['content']
    
    return StreamingResponse(prompt_gen(prompts), media_type='text/plain')    
    