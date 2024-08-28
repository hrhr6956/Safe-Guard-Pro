from flask import Flask, render_template
import subprocess
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

@app.route('/')
def index(name=None):
    return render_template('index.html',name=name)

@app.route('/exec')
def parse(name=None):
    import face_recognition
    print("done")
    return render_template('index.html',name=name)

@app.route('/run_security_script', methods=['POST'])
def run_security_script():
    
    subprocess.Popen(["python", "security.py"])
    return 'Security script is running...'

if __name__ == '__main__':
    app.run(debug=True)
    
