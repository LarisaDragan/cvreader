import os
from pdfminer.high_level import extract_text
from flask import Flask, jsonify, request, Response
from chatwrap.client import LLMClient
from chatwrap.cli import LLM_SERVER_URL


app = Flask(__name__)
CVS_PATH = 'CVs'

@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'

@app.route('/extractSkills', methods=['POST'])
def extract_skills():
    cv = "Larisa Dragan, Python -learning, JavaScript, React, with an experience 3+ years"
    llmClient = LLMClient(LLM_SERVER_URL)
    body = request.get_json()
    
    prompt=f'Extract the skills from the CV {body}. Return the response in the following format: skill' 
    
    response = llmClient.send_request(prompt, model="llama-3.2-1b-instruct", temperature=0.7, streaming=False)

    response_data = response.json()  
    
    if response.status_code == 200:
        try:
            response_data = response.json() # Extrage datele JSON
            # acceseaza continutul extras ca raspuns json
            content = response_data['choices'][0]['message']['content']
            
            # returneaza continutul extras
            return content
        except ValueError:
            # daca nu e JSON valid, trimite un raspuns ca text
            return jsonify({"message": response.text})
    else:
        # În caz că nu este 200 OK, returnează un mesaj de eroare
        return jsonify({"error": "Failed to fetch data from LLM"})
    

@app.route('/findCandidates', methods=['GET'])
def get_top_candidates():
    return 'Top candidates works!'


@app.route('/uploadCV', methods=["POST"])
def upload_cv():
    file = request.files['file']
    
    file.save(os.path.join(CVS_PATH, file.filename))
    
    return 'Uploaded with success!'

@app.route('/extractInfo', methods=["POST"])
def extract_info():
    file_name=request.get_json()['filename']
    
    if not os.path.exists(os.path.join(CVS_PATH, file_name)):
        return Response("File not found", status=404 )
        
    text = extract_text(os.path.join(CVS_PATH, file_name))
    
    print("==", text)
    
    return 'Info extracted!'

# TODO: install chroma 
#  save info from extract to chroma
#  extra: read from db - chroma

if __name__ == '__main__':
    app.run(debug=True)