import os
from dotenv import load_dotenv

# Azure OpenAI
from langchain_openai import AzureChatOpenAI

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, session, url_for)

import identity.web
from flask_session import Session

import app_config

load_dotenv()

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

app.jinja_env.globals.update(Auth=identity.web.Auth)  # Useful in template for B2C
auth = identity.web.Auth(
    session=session,
    authority=app.config["AUTHORITY"],
    client_id=app.config["CLIENT_ID"],
    client_credential={
        "thumbprint": app.config["THUMBPRINT"],
        "private_key": app.config["PRIVATE_KEY"],
        },
)

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('AZURE_OPENAI_ENDPOINT')
api_version = os.getenv('AZURE_OPENAI_API_VERSION')
azure_deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')

@app.route('/hello', methods=['POST'])
def hello():
    req = request.form.get('req')
    original_req = req  # Pc639

    token = auth.get_token_for_client(app_config.SCOPE)
    if "error" in token:
        print(token['error'])
        return redirect(url_for("index"))

    llm = AzureChatOpenAI(
        api_version=api_version,
        azure_deployment=azure_deployment,
        azure_ad_token=token['access_token'],
    )
    print(token['access_token'])
    text = llm.invoke(req).content

    if req:
        print('Request for hello page received with req=%s' % req)
        return render_template('hello.html', req=text, original_req=original_req)  # P2b66
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
