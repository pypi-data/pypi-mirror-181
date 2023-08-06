import openai
import json
import sys

config={}

class chatgptCall:
    def __init__(self,api_key=None,msg=None):
        self.api_key=api_key
        self.msg=msg


    def setApiKey(self,api_key):
        self.api_key=api_key
        config['API_KEY']=api_key
        openai.api_key = self.api_key

    def sendMessage(self,msg):
        self.msg=msg

        if self.api_key is None or self.api_key == '':
            print('ERROR: API Key is not set.')
            sys.exit()

        if self.msg is None or self.msg == '':
            print('ERROR: A valid message is required')
            sys.exit()

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.msg,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        if 'choices' in response:
            resp = response.get('choices')
            if 'text' in resp[0]:
                resp=resp[0].get('text')
            else:
                raise Exception('Something Went Wrong! Please check Api Key')
        else:
            raise Exception('Something Went Wrong! Please check Api Key')
        return resp



class chatgptprtkException(Exception):
    pass