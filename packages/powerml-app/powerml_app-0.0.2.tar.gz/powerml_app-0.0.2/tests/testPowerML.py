import sys
import os


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.dirname(
        os.path.realpath(__file__))), "src")
    sys.path.append(path)
    from powerml_app.utils.run_ai import run_ai
    response = run_ai()
    print(response)

    from powerml_app.PowerML import PowerML
    config = {"key": ""}
    powerml = PowerML(config)
    testPrompt = "hello there"
    response = powerml.predict(prompt=testPrompt)
    print(response)

    data = ["item1\n new line", "item2", "item3"]
    val = powerml.fit(data, "llama")
    print(val['model'])
