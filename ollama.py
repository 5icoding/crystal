# from ollama import generate


# response = generate('phi', 'Why is the sky blue?')
# print(response['response'])


# curl http://localhost:11434/api/generate -d '{"model": "phi","prompt":"Why is the sky blue?"}'

import ollama
response = ollama.chat(model='llama2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])