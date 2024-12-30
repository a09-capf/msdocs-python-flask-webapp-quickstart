import os
from dotenv import load_dotenv

# Azure OpenAI
from langchain_openai import AzureChatOpenAI

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

os.environ["AZURE_OPENAI_API_KEY"] = os.getenv('AZURE_OPENAI_API_KEY')
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('AZURE_OPENAI_ENDPOINT')
api_version = os.getenv('AZURE_OPENAI_API_VERSION')
azure_deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')

@app.route('/hello', methods=['POST'])
def hello():
   req = request.form.get('req')

   llm = AzureChatOpenAI(
       api_version=api_version,
       azure_deployment=azure_deployment,
   )
   text = llm.invoke(req).content

   if req:
       print('Request for hello page received with req=%s' % req)
       return render_template('hello.html', req = text)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()
