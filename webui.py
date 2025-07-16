from flask import Flask, render_template_string
import threading

app = Flask(__name__)

# Dummy state for stub
state = {
    'running': False,
    'current_tasks': [],
    'completed_tasks': []
}

@app.route('/')
def index():
    return render_template_string('''
    <h1>BabyAGI Web UI (Stub)</h1>
    <p>Status: {{ 'Running' if running else 'Stopped' }}</p>
    <h2>Current Tasks</h2>
    <ul>{% for t in current_tasks %}<li>{{ t }}</li>{% endfor %}</ul>
    <h2>Completed Tasks</h2>
    <ul>{% for t in completed_tasks %}<li>{{ t }}</li>{% endfor %}</ul>
    <form method="post" action="/start"><button type="submit">Start</button></form>
    <form method="post" action="/stop"><button type="submit">Stop</button></form>
    ''', running=state['running'], current_tasks=state['current_tasks'], completed_tasks=state['completed_tasks'])

@app.route('/start', methods=['POST'])
def start():
    state['running'] = True
    return index()

@app.route('/stop', methods=['POST'])
def stop():
    state['running'] = False
    return index()

if __name__ == '__main__':
    app.run(debug=True) 