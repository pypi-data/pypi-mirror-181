from flask import Flask, render_template, request
import sys
import json
from chatgptprtk.req_call import config
import chatgptprtk.req_call as rc

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None


app = Flask(__name__)

bot_eng=rc.chatgptCall()

api_key="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"
bot_eng.setApiKey(api_key)


@app.route('/getChatgptResponse', methods=['GET', 'POST'])
def home():
    payload = request.get_json(silent=True, cache=False, force=True)
    if payload is None:
        resp = {"responseCode": 412, "responseDesc": "Wrong JSON format : Failed to decode JSON object"}
        return resp
    if 'msg' in payload:
        msg=payload['msg']
        op=bot_eng.sendMessage(msg)
        resp={"responseCode": 200,"chatGptResp":op}
        return resp
    else:
        resp={"responseCode": 412,"responseDesc":"'msg' is a required parameter"}
        return resp

def displayServerInfo() -> None:
    print('::Sample Request::')
    sample_req={'msg':'<YOUR MESSAGE HERE>'}
    print(json.dumps(sample_req,indent=4))
    print('API Endpoint: {Server URL}/getChatgptResponse')

def startServer(host=None, port=None) -> None:
    if config['API_KEY'] is None or config['API_KEY'] == '':
        print('ERROR: Can not start server. API Key is not set.')
        sys.exit()

    try:
        if (host and port is None) or (port and host is None):
            print('ERROR: Both host and port required!!!')
            sys.exit()
        if host and port:
            displayServerInfo()
            app.run(host=host,port=port)
        else:
            displayServerInfo()
            app.run()
    except Exception:
        print('Oops!! Internal Server Error. Try after sometime.')
        sys.exit()

class chatgptprtkException(Exception):
    pass