from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData

metadata = MetaData()

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
    
    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}, {self.category}, {self.equipment_needed}>'
    
class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Workout {self.id}, {self.date}, {self.duration_minutes}, {self.notes}>'
    
class WorkoutExercises(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key = True)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))