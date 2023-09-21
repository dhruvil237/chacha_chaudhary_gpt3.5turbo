# Import the necessary modules
import fastapi
import openai
import uvicorn
from pydantic import BaseModel
import os
from typing import List

# Set the OpenAI API key
openai.api_key = 'pk-**********************************************' # set this as it is, don't replace with your key
api_key = os.environ.get('NORTHSTAR_API_KEY')
# api_key = ""
openai.api_base = f'https://proxy.ainorthstar.tech/{api_key}/v1'

# Create a FastAPI app
app = fastapi.FastAPI()

# Define a request model for chat completion
class ChatRequest(BaseModel):
    # The chat history as a list of strings
    history: List[str]
    # The partial message to be completed as a string
    partial: str

# # Define a response model for chat completion
# class ChatResponse(BaseModel):
#     # The completed message as a string
#     completion: str

# Define an endpoint for chat completion using gpt-3.5-turbo model
@app.post("/chat")
def chat(request: ChatRequest):
    system = "you are Chacha Chaudhary and you only explain/ answer related to namami ganges project"
    system_msg = [{"role": "system", "content": system}]
    user_assistant_msgs = [
        {"role": "assistant", "content": request.history[i]} if i % 2 != 0 else {"role": "user", "content": request.history[i]}
        for i in range(len(request.history))]

    msgs = system_msg + user_assistant_msgs
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=msgs)
    status_code = response["choices"][0]["finish_reason"]
    assert status_code == "stop", f"The status code was {status_code}."

    return response["choices"][0]["message"]["content"]

# Run the app using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
