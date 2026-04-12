from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

db = SQLAlchemy(metadata=metadata)

# Define Models here

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    category = db.Column(db.String, nullable = False)
    equipment_needed = db.Column(db.Boolean)
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise')
    """association proxy is to access workouts directly from exercise,
    and create WorkoutExercise instances when adding workouts to an exercise
    we don't have to manually create a WorkoutExercise instance if we want to add a workout to an exercise, 
    we can just add the workout to the workouts association proxy and it will automatically create the WorkoutExercise instance for us.
    The creator function is a lambda function that takes a workout as an argument 
    and returns a new WorkoutExercise instance with the workout set to the workout argument"""
    workouts = association_proxy('workout_exercises', 'workout', creator=lambda workout: WorkoutExercise(workout=workout))
    
    #validators
    valid_categories = ['Pilates', 'Yoga', 'Aerobics', 'Cardio', 'Bodybuilding']
    @validates('name', 'category')
    def validate_exercise(self, key, value):
        if key == 'name':
            if not value or value.strip() == '':
                raise ValueError('Name cannot be empty')
            return value
        if key == 'category':
            if not value or value.strip() == '':
                raise ValueError('Category cannot be empty')

            if value.strip() not in self.valid_categories:
                raise ValueError('Category must be one of these: Pilates, Yoga, Aerobics, Cardio, Bodybuilding')

            return value.strip()
            
    
    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}, {self.category}, {self.equipment_needed}>'
    
class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout')
    """association proxy is to access exercises directly from workout,
    and create WorkoutExercise instances when adding exercises to a workout
    in simple terms, this allows us to add exercises to a workout without having to manually create a WorkoutExercise instance each time.
    The creator function is a lambda function that takes an exercise as an argument
    and returns a new WorkoutExercise instance with the exercise set to the exercise argument"""
    exercises = association_proxy('workout_exercises', 'exercise', creator=lambda exercise: WorkoutExercise(exercise=exercise))
    
    @validates('duration_minutes', 'notes')
    def validate_duration(self, key, value):
        if key == 'duration_minutes':
            if value is None:
                return value
            if value < 0:
                raise ValueError("Duration must be a positive number")
            return value
        if key == 'notes':
            if value is None:
                return value
            if len(value) > 300:
                raise ValueError('Notes must be less than 300 characters long.')
            return value 
        return value
        
    
    def __repr__(self):
        return f'<Workout {self.id}, {self.date}, {self.duration_minutes}, {self.notes}>'
    
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key = True)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)
    
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    
    @validates('reps', 'sets', 'duration_seconds')
    def validate_workout_exercise_metrics(self, key, value):
        if value is None:
            return value
        if value < 0:
            raise ValueError(f"{key.replace('_', ' ').title()} must be a positive number")
        return value
    
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    
    def __repr__(self):
        return f'<WorkoutExercise {self.id}, {self.reps}, {self.sets}, {self.duration_seconds}>'
    