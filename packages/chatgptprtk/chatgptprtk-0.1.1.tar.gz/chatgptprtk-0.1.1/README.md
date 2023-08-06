
# ChatGptPrtk
[![PyPi](https://img.shields.io/pypi/v/chatgptprtk.svg)](https://pypi.python.org/pypi/chatgptprtk) 
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/pratikjoshi999/chatGptPrtkPkg/blob/main/LICENSE)

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

## API Reference

#### Endpoint

```bash
  {Host url}/getChatgptResponse
```
#### Request

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `msg` | `string` | **Required**. Your Message to AI |

#### Response


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `chatGptResp`      | `string` |  Response from chatGPT |
| `responseCode`      | `int` |  API Response Code |

#### API Key
Set a valid API Key using `setApiKey()` before starting server.


## License

[MIT](https://github.com/pratikjoshi999/chatGptPrtkPkg/blob/main/LICENSE)