import requests
import json
from powerml_app.utils.run_ai import powerml_completions
from typing import TypedDict


class ConfigType(TypedDict):
    key: str


class PowerML:
    def __init__(self, config: ConfigType):
        self.config = config
        self.key = self.config["key"]
        print(self.key)

    def predict(self,
                prompt: str = "Say this is a test",
                stop: str = "",
                model: str = "llama",
                max_tokens: int = 128,
                temperature: int = 0,
                ) -> str:
        params = {
            "prompt": prompt,
            "model": model,
            "max_tokens": max_tokens,
            "stop": stop,
            "temperature": temperature,
        }
        # if the model is one of our models, then hit our api
        try:
            resp = powerml_completions(params, self.key)
        except:
            raise Exception("API failing")
        if 'error' in resp:
            raise Exception(str(resp))
        text = resp['completion']
        return text

    def fit(self,
            data: list[str],
            model: str = "llama"):
        # Upload filtered data to train api
        response = requests.post(
            url="https://api.staging.powerml.co/v1/train",
            json={
                "dataset": self.__make_dataset_string(data),
                "model": model
            })
        return response.json()

    def __make_dataset_string(self, training_data):
        dataset = "\n".join(
            [json.dumps({"prompt": item.replace("\n", "\\n")}) for item in training_data])
        print("Generated dataset: ", dataset)
        return dataset
