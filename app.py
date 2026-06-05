from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Project Giza Controller</h1>
    <form action="/run" method="post">
        <textarea name="cmd" rows="10" cols="60" placeholder="Type your commands here..."></textarea><br>
        <input type="submit" value="Execute Command">
    </form>
    '''

@app.route('/run', methods=['POST'])
def run():
    command = request.form.get('cmd', '')
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
        return f"<h2>Output:</h2><pre>{output}</pre><a href='/'>Go Back</a>"
    except subprocess.CalledProcessError as e:
        return f"<h2>Error:</h2><pre>{e.output.decode()}</pre><a href='/'>Go Back</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
