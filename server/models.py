from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData

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
    
    workout_exercise = db.relationship('WorkoutExercise', back_populates = 'exercise')
    workouts = db.relationship('Workout', back_populates = 'exercises', secondary = 'workout_exercises')
    
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
    date = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    workout_exercise = db.relationship('WorkoutExercise', back_populates = 'workout')
    exercises = db.relationship('Exercise', back_populates = 'workouts', secondary='workout_exercises')
    
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
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    
    @validates('duration_seconds')
    def validate_duration_seconds(self, key, value):
        if value is None:
            return value
        if value < 0:
            raise ValueError("Duration must be a positive number")
        return value
    
    workout = db.relationship('Workout', back_populates = 'workout_exercise')
    exercise = db.relationship('Exercise', back_populates = 'workout_exercise')
    
    def __repr__(self):
        return f'<WorkoutExercise {self.id}, {self.reps}, {self.sets}, {self.duration_seconds}>'
    