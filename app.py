from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Project Giza Controller</h1>
    <form action="/run" method="post">
        <textarea name="cmd" rows="5" cols="40"></textarea><br>
        <input type="submit" value="Send Command to Swarm">
    </form>
    '''

@app.route('/run', methods=['POST'])
def run():
    command = request.form['cmd']
    # This runs the command on your host
    output = subprocess.check_output(command, shell=True).decode()
    return f"<pre>{output}</pre><a href='/'>Go Back</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
