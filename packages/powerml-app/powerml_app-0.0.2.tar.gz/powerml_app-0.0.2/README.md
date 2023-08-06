# PowerML Python Package

  from powerml_app.PowerML import PowerML
  config = {"key": ""}
  powerml = PowerML(config)
  testPrompt = "hello there"
  response = powerml.predict(prompt=testPrompt)
  print(response)

  data = ["item1\n new line", "item2", "item3"]
  val = powerml.fit(data, "llama")
  print(val)