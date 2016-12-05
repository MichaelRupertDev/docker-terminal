from flask import Flask, request, render_template
from subprocess import Popen, PIPE
import docker
import thread

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('dashboard.html', running=docker.ps())

@app.route('/start/<image>', methods=['POST'])
def start(image):
    if request.method == 'POST':
        err = docker.run(image)
        if err:
            return err
        return 'Started ' + image

@app.route('/stop/<cid>', methods=['POST'])
def stop(cid):
    if request.method == 'POST':
        thread.start_new_thread(docker.stop, (cid,))
        return 'Stopping ' + cid

if __name__ == "__main__":
	app.run(host="0.0.0.0")
