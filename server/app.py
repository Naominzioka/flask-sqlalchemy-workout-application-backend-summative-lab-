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
        validated_data = WorkoutSchema().load(data)  # deserialize incoming data into a Python dictionary and validate it.
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

    response_body = WorkoutSchema().dump(new_workout) # serialize the new workout object into a JSON-compatible format for the response.
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
    exercises_list = Exercise.query.all()
    if not exercises_list:
        return make_response({"message": "No exercises found"}, 404)
    response_body = ExerciseSchema(many=True).dump(exercises_list)
    return make_response(response_body, 200)

#get exercise by id
@app.route('/exercises/<int:id>', methods=["GET"])
def get_exercise_id(id):
    exercise = Exercise.query.filter(Exercise.id==id).first()
    if not exercise:
        return make_response({"message": "Exercise id not found"}, 404)
    response_body = ExerciseSchema().dump(exercise)
    return make_response(response_body, 200)

#add a new exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    if not request.is_json:
        return make_response({"message": "Request body must be JSON"}, 400)

    data = request.get_json()

    try:
        validated_exercise = ExerciseSchema().load(data)
    except ValidationError as e:
        return make_response({"errors": e.messages}, 400)

    try:
        new_exercise = Exercise(
            name = validated_exercise.get('name'),
            category = validated_exercise.get('category'),
            equipment_needed = validated_exercise.get('equipment_needed')
        )
        db.session.add(new_exercise)
        db.session.commit()
    except ValueError as e:
        return make_response({"message": str(e)}, 400)
    response_body = ExerciseSchema().dump(new_exercise)
    return make_response(response_body, 201)

#delete an exercise
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise_to_delete = Exercise.query.filter(Exercise.id==id).first()
    if not exercise_to_delete:
        return make_response({"message": "Exercise id not found"}, 404)
    db.session.delete(exercise_to_delete)
    db.session.commit()
    return make_response('', 204)

#add an exercise to a workout
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    if not workout or not exercise:
        return make_response({"message": "Workout or Exercise id not found"}, 404)
    
    data = request.get_json()

    try:
        validated_workout_exercise = WorkoutExerciseSchema().load(data)
    except ValidationError as e:
        return make_response({"errors": e.messages}, 400)
    
    workout_exercise = WorkoutExercise(**validated_workout_exercise)
    workout_exercise.workout_id = workout_id
    workout_exercise.exercise_id = exercise_id
    
    db.session.add(workout_exercise)
    db.session.commit()
    
    response_body = WorkoutExerciseSchema().dump(workout_exercise)
    return make_response(response_body, 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    