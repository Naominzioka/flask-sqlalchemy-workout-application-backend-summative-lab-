from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

db = SQLAlchemy(metadata=metadata)

# Define Models here
"""
these are the tables for the db with columns and data types. 
The __repr__ method is what i will use to provide a string output for each object and also for debugging purposes."""

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)
    
    workout_exercise = db.relationship('WorkoutExercise', back_populates = 'exercise')
    workouts = db.relationship('Workout', back_populates = 'exercises', secondary = 'workout_exercises')
    
    
    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}, {self.category}, {self.equipment_needed}>'
    
class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    workout_exercise = db.relationship('WorkoutExercise', back_populates = 'workout')
    exercises = db.relationship('Exercise', back_populates = 'workouts', secondary='workout_exercises')
    
    def __repr__(self):
        return f'<Workout {self.id}, {self.date}, {self.duration_minutes}, {self.notes}>'
    
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key = True)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    
    workout = db.relationship('Workout', back_populates = 'workout_exercise')
    exercise = db.relationship('Exercise', back_populates = 'workout_exercise')
    
    def __repr__(self):
        return f'<WorkoutExercise {self.id}, {self.reps}, {self.sets}, {self.duration_seconds}>'
    