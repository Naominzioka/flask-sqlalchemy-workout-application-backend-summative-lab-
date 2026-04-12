from flask import Flask, make_response, request
from flask_migrate import Migrate
from schema import *

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
    workouts_list = Workout.query.all()
    if not workouts_list:
        return make_response({"message": "No workouts found"}, 404)
    response_body = WorkoutSchema(many=True).dump(workouts_list)
    return make_response(response_body, 200)

#get workout by id
@app.route('/workouts/<int:id>', methods=["GET"])
def get_workout_id(id):
    workout = Workout.query.filter(Workout.id == id).first()
    if not workout:
        return make_response({"message": "No workout with that id found"}, 404)
    response_body = WorkoutSchema().dump(workout)
    return make_response(response_body, 200)

#add a new workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    if not request.is_json:
        return make_response({"message": "Request body must be JSON"}, 400)

    data = request.get_json()

    try:
        validated_data = WorkoutSchema().load(data)
    except ValidationError as e:
        return make_response({"errors": e.messages}, 400)

    try:
        new_workout = Workout(
            date=validated_data.get('date'),
            duration_minutes=validated_data.get('duration_minutes'),
            notes=validated_data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
    except ValueError as e:
        return make_response({"message": str(e)}, 400)

    response_body = WorkoutSchema().dump(new_workout)
    return make_response(response_body, 201)

#delete a workout
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_a_workout(id):
    workout_to_delete = Workout.query.filter(Workout.id == id).first()
    if not workout_to_delete:
        return make_response({"message": "Workout id not found"}, 404)
    db.session.delete(workout_to_delete)
    db.session.commit()
    return make_response('', 204)
    

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
    