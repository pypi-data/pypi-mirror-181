import requests

import logging

logger = logging.getLogger(__name__)


def run_ai(prompt="Say this is a test",
           stop="",
           model="llama",
           max_tokens=128,
           return_logprobs=False,
           api="powerml",
           temperature=0,
           key="",
           ):

    params = {
        "prompt": prompt,
        "model": model,
        "max_tokens": max_tokens,
        "stop": stop,
        "temperature": temperature,
    }
    if api == "powerml":
        # if the model is one of our models, then hit our api
        try:
            resp = powerml_completions(params, key)
        except:
            raise Exception("API failing")
        if 'error' in resp:
            raise Exception(str(resp))
        text = resp['completion']
        if return_logprobs:
            return text, None
        return text
    else:
        # otherwise hit openai
        try:
            resp = openai_completions(params)
        except:
            raise Exception("Run 'powerml start' first")
        if 'error' in resp:
            raise Exception(str(resp))
        text = resp['choices'][0]['text']
        if return_logprobs:
            logprobs = resp['choices'][0]['logprobs']
            return text, logprobs
        return text


def powerml_completions(params, key):
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json", }
    response = requests.post(
        url="https://api.staging.powerml.co/v1/completions",
        headers=headers,
        json=params)
    return response.json()


def openai_completions(params, key):
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json", }
    response = requests.post(
        url="https://api.openai.com/v1/completions",
        headers=headers,
        json=params)
    return response.json()


if __name__ == "__main__":
    text = run_ai()
    print(text)
