
# ChatGptPrtk

ChatGPT is a prototype artificial intelligence chatbot developed by [OpenAI](https://openai.com/) which specializes in dialogue. 

ChatGptPrtk is a python wrapper around OpenAI ChatGPT for easy access of its functionality.

## Features

- Programmable use as SDK
- Create server and run API with customizable payload
- No Moderation
- API Key based authentication

## Installation

Install ChatGptPrtk with pip

```bash
  pip install chatgptprtk
```

## Usages

_Create an account in [OpenAI](https://openai.com/) and get API Key_

Get AI Response

```bash
  import chatgptprtk as ch

  api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx83r"
  ch.setApiKey(api_key)

  msg="write a pallindrome program in java"
  response=ch.sendMessage(msg)
```

Start a server
```bash
  ch.startServer()
```


## License

[MIT](https://choosealicense.com/licenses/mit/)