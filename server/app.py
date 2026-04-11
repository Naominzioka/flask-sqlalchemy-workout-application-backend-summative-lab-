from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here
@app.route('/')
def home():
    body = {'message': 'Welcome to the Workout Application!'}
    return make_response(body, 200)

#list workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    return make_response({"message": "List of all workouts"}, 200)

#get workout by id
@app.route('/workouts/<int:id>', methods=["GET"])
def get_workout_id(id):
    return make_response({"message": f"Show workout {id} with exercises"}, 200)

#add a new workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    return make_response({"message": "Create a workout"}, 201)

#delete a workout
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_a_workout(id):
    return make_response({"message": f"Workout with {id} was successfully deleted"}, 204)

#exercises
#get all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    return make_response({"message": "List of all exercises"}, 200)

#get exercise by id
@app.route('/exercises/<int:id>', methods=["GET"])
def get_exercise_id(id):
    return make_response({"message": f"Show exercise {id} and associated workouts"}, 200)

#add a new exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    return make_response({"message": "Create an exercise"}, 201)

#delete an exercise
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    return make_response({"message": f"Exercise {id} successfully deleted"}, 204)

#add an exercise to a workout
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    return make_response({"message": f"Added exercise {exercise_id} to workout {workout_id}"}, 201)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
    