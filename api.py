from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/book-flight', methods=['POST'])
def book_flight():
    data = request.json
    print("🚀 Booking received:", data)
    response = {
        "message": f"Booking confirmed for {data['name']} on {data['date']} from {data['from']} to {data['to']}",
        "status": "success"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)
