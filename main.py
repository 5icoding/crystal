import flet as ft
import subprocess

# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer

# def get_llm(prompt_text):

#     torch.set_default_device("cuda")
#     model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5", torch_dtype="auto", trust_remote_code=True)

#     tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5", trust_remote_code=True)   

#     inputs = tokenizer(prompt_text, return_tensors="pt", return_attention_mask=False)

#     outputs = model.generate(**inputs, max_length=200)
#     text = tokenizer.batch_decode(outputs)[0]
#     print(text)

#     return text

def get_llm(prompt_text):
    print(prompt_text)
    # 微软的phi2模型 
    command = 'ollama run phi '+"'" +prompt_text +"'"
    print(command)

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # 获取返回信息
    stdout = result.stdout
    stderr = result.stderr

    print("STDOUT:")
    print(stdout)
    print("STDERR:")
    print(stderr)

    return stdout


txt_answer = ft.TextField(
    label="Answer", 
    multiline=True,
    value="\n\n\n\n\n\n\n",)

txt_ask = ft.TextField(
    label="Ask",
    value="What is the meaning of life?",
    multiline=True,
    min_lines=1,
    max_lines=3)

def main(page: ft.Page):
    def btn_click(e):
        txt_answer.value = get_llm(txt_ask.value)

        page.update()
        txt_ask.focus()

    page.add(txt_answer)
    page.add(txt_ask)
    page.add(ft.ElevatedButton("Say hello!", on_click=btn_click))


ft.app(target=main)