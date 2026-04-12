# Flask SQLAlchemy Workout Application Backend

## Description

This project is a Flask backend API for tracking workouts, exercises, and the exercises performed within each workout. It uses Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow to manage data models, database migrations, validation, and JSON responses.

The application is designed around three main resources:

- `Workout` stores the date, total duration, and notes for a workout session.
- `Exercise` stores the name, category, and whether equipment is needed.
- `WorkoutExercise` connects workouts and exercises so a single workout can contain many exercises, each with its own reps, sets, or duration.

The API supports:

- Creating and viewing workouts
- Creating and viewing exercises
- Linking exercises to workouts through `WorkoutExercise`
- Validating workout and exercise data before saving it
- Returning JSON responses that can be consumed by a frontend or API client such as Postman

This project is useful for practicing how Flask works with relational data, schema validation, and REST-style endpoints in a backend-only application.

## Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd flask-sqlalchemy-workout-application-backend-summative-lab
```

2. Install dependencies with Pipenv:

```bash
pipenv install
```

3. Activate the virtual environment:

```bash
pipenv shell
```

4. Move into the server directory:

```bash
cd server
```

5. Apply database migrations:

```bash
flask db upgrade
```

If you ever make model changes later, you can generate and apply a new migration with:

```bash
flask db migrate -m "describe your change"
flask db upgrade
```

6. Optional: seed the database with sample data:

```bash
python seed.py
```

## Run Instructions

Start the Flask development server from the `server` directory.

Option 1 (recommended):

```bash
export FLASK_APP=app.py
flask run --port 5555
```

Option 2:

```bash
python app.py
```

The API will run locally at:

```bash
http://127.0.0.1:5555
```

You can then test routes in the browser, with Postman, or by using tools like `curl`.

## Using Flask Shell

Besides calling the API routes, you can also interact directly with the database using Flask shell. This is useful for checking saved records, testing relationships, and manually creating sample data during development.

From the `server` directory, start Flask shell with:

```bash
flask shell
```

Once inside the shell, import your database and models:

```python
from models import db, Workout, Exercise, WorkoutExercise
```

### Example: View all records

```python
Workout.query.all()
Exercise.query.all()
WorkoutExercise.query.all()
```

### Example: Create a new exercise

```python
new_exercise = Exercise(name='Squats', category='Bodybuilding', equipment_needed=False)
db.session.add(new_exercise)
db.session.commit()
```

### Example: Create a new workout

```python
from datetime import date

new_workout = Workout(date=date.today(), duration_minutes=35, notes='Leg day session')
db.session.add(new_workout)
db.session.commit()
```

### Example: Link an exercise to a workout

```python
entry = WorkoutExercise(
	workout_id=new_workout.id,
	exercise_id=new_exercise.id,
	reps=12,
	sets=4,
	duration_seconds=None
)

db.session.add(entry)
db.session.commit()
```

### Example: Query relationships

```python
workout = Workout.query.first()
workout.workout_exercises

exercise = Exercise.query.first()
exercise.workout_exercises
```

Using Flask shell is helpful when you want to inspect data quickly without sending HTTP requests.

## API Endpoints

- `GET /` 
	Returns a welcome message for the API.
- `GET /workouts` 
	Returns all workouts.
- `GET /workouts/<id>` 
	Returns a single workout by ID.
- `POST /workouts` 
	Creates a new workout.
- `DELETE /workouts/<id>` 
	Deletes a workout by ID.
- `GET /exercises` 
	Returns all exercises.
- `GET /exercises/<id>` 
	Returns a single exercise by ID.
- `POST /exercises` 
	Creates a new exercise.
- `DELETE /exercises/<id>` 
	Deletes an exercise by ID.
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` 
	Adds an exercise to a workout with details such as reps, sets, and duration.

## Test Files

Test files are not included in this submission.

## Notes

- Run commands such as `python app.py`, `python seed.py`, and `flask shell` from the `server` directory.
- The database file is created in the Flask instance folder because the app uses `sqlite:///app.db`.
- If you want fresh sample data, run `python seed.py` again after clearing or recreating the database.

## Learning Purpose

This project was built for learning purposes to practice backend development with Flask, relational database design with SQLAlchemy, schema validation with Marshmallow, and database migrations with Flask-Migrate.

It can be used as a reference project for understanding how models, routes, validation, and database relationships work together in a REST-style Flask application.

## License

This project is shared for educational and reading purposes. You may use it as a learning reference and adapt it for personal practice.
