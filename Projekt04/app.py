import json
import threading
from flask import Flask, render_template, Response, jsonify
from main import run_project

app = Flask(__name__)

# Global flag to handle process cancellation
cancel_event = threading.Event()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run')
def run():
    def generate():
        cancel_event.clear()
        
        for msg in run_project(cancel_event):
            if isinstance(msg, str):
                if msg.startswith("IMAGE:"):
                    # Send image path instructions
                    data = json.dumps({"image": msg.split("IMAGE:")[1].strip()})
                else:
                    # Send console text
                    data = json.dumps({"text": msg})
                
                # Format exactly as Server-Sent Events require
                yield f"data: {data}\n\n"
        
        # Notify the JS script that the stream is closed
        yield f"data: {json.dumps({'done': True})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/cancel', methods=['POST'])
def cancel():
    cancel_event.set()
    return jsonify({"status": "Cancellation requested. Awaiting current task to break..."})

if __name__ == '__main__':
    app.run(debug=True, threaded=True)