from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.json_util import dumps
import os

app = Flask(__name__)
CORS(app)

# MongoDB connection setup
mongo_uri = os.environ.get('MONGODB_URI', "mongodb+srv://admin:admin@cluster0.iw8pgql.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(mongo_uri)
db = client['fruit_ninja']  # Adjust the database name as needed
scores = db.scores

# Add or update a score
@app.route('/api/score', methods=['POST'])
def add_or_update_score():
    data = request.json
    session_id = data.get('sessionId')
    score = data.get('score')
    
    existing_score = scores.find_one({'sessionId': session_id})
    
    if existing_score and score > existing_score['score']:
        scores.update_one({'sessionId': session_id}, {'$set': {'score': score}})
        return jsonify({'message': 'Score updated'}), 201
    elif not existing_score:
        scores.insert_one({'sessionId': session_id, 'score': score})
        return jsonify({'message': 'New score saved'}), 201
    
    return jsonify({'message': 'Existing score is higher or equal. No update needed.'}), 200

# Get top scores
@app.route('/api/scores', methods=['GET'])
def get_scores():
    top_scores = scores.find().sort('score', -1).limit(10)
    return dumps(top_scores), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
