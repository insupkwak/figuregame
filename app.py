import json
from flask import Flask, request, jsonify, render_template
from datetime import datetime




app = Flask(__name__)
data_file = 'attempts.json'


def load_data():
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, default=str)


attempts_log = load_data()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/attempts', methods=['POST'])
def record_attempt():
    data = request.get_json()
    if not data or not all(key in data for key in ['digits', 'attempts', 'username']):
        return jsonify({'error': 'Missing data'}), 400

    data['timestamp'] = datetime.now()
    attempts_log.append(data)


    print(attempts_log)

    save_data(attempts_log)  # 데이터를 파일에 저장

    return jsonify({'message': 'Data saved successfully', 'data': data}), 201


@app.route('/attempts/<int:digits>', methods=['GET'])
def get_attempts(digits):

    digits_str = str(digits)
    attempts_log = load_data()  # 파일에서 데이터를 로드
    

    filtered_attempts = [attempt for attempt in attempts_log if attempt['digits'] == digits_str]
    sorted_attempts = sorted(filtered_attempts, key=lambda x: x['attempts'])
    
    print(sorted_attempts)

    return jsonify(sorted_attempts)


if __name__ == '__main__':
    app.run(host='0.0.0.0')