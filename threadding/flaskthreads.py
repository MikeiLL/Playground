from flask import Flask, jsonify
import threading
import time
import random
import re
"""
https://devguide.dev/blog/threads-and-long-running-tasks-in-flask
"""

app = Flask(__name__)

def long_running_task():
    # Simulate a long-running task
    time.sleep(5)
    with open('/usr/share/dict/words') as f:
        words=[w for w in f.read().split() if re.match('^[a-z]+$', w)]
    tenrandomwords = ""
    for ct in range(1,5):
        tenrandomwords += " " + random.choice(words)
    print("Long-running task completed for %s" % tenrandomwords)

@app.route('/execute_task')
def execute_task():
    # Start the long-running task in a separate thread
    thread = threading.Thread(target=long_running_task)
    thread.start()
    return jsonify({'message': 'Long-running task started.'})

if __name__ == '__main__':
    app.run(debug=True)
