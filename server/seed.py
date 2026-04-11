#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


with app.app_context():
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    
    exercises_list = []
    
    #ccategory should be one of those in models.py
    exercises_list.append(Exercise(name='Push-ups', category='Bodybuilding', equipment_needed=False))
    exercises_list.append(Exercise(name='Running', category='Cardio', equipment_needed=False))
    exercises_list.append(Exercise(name='Yoga', category='Yoga', equipment_needed=True))
    exercises_list.append(Exercise(name='Pilates', category='Pilates', equipment_needed=True))
    exercises_list.append(Exercise(name='Jumping Jacks', category='Aerobics', equipment_needed=False))
    
    db.session.add_all(exercises_list)
    db.session.commit()
	
    # add workouts that match the exercises above
    """duration_minutes is the total time spent on the workout
    it is the total time spent in the gym or doing the workout"""
    w1 = Workout(id=1, date=date(2024, 6, 1), duration_minutes=30, notes='Felt great!')
    w2 = Workout(id=2, date=date(2024, 6, 1), duration_minutes=45, notes='Challenging but rewarding!')
    w3 = Workout(id=3, date=date(2024, 6, 2), duration_minutes=60, notes='Relaxing and refreshing!')
    w4 = Workout(id=4, date=date(2024, 6, 2), duration_minutes=40, notes='Intense but effective!')
    w5 = Workout(id=5, date=date(2024, 6, 3), duration_minutes=50, notes='Strengthening and toning!')
   
    db.session.add_all([w1, w2, w3, w4, w5])
    db.session.commit()


    #add workout exercises that match the workouts and exercises above
    """duration_seconds is the time spent on one specific exercise inside that workout
    it is broken down into seconds spent on each exercise on that workout"""
    workout_exercises = [
        WorkoutExercise(workout_id=1, exercise_id=1, reps=15, sets=3, duration_seconds=None),
        WorkoutExercise(workout_id=1, exercise_id=5, reps=20, sets=3, duration_seconds=None),
        WorkoutExercise(workout_id=2, exercise_id=2, reps=None, sets=None, duration_seconds=1800),
        WorkoutExercise(workout_id=3, exercise_id=3, reps=None, sets=None, duration_seconds=2400),
        WorkoutExercise(workout_id=4, exercise_id=4, reps=None, sets=None, duration_seconds=2100),
        WorkoutExercise(workout_id=5, exercise_id=1, reps=12, sets=4, duration_seconds=None),
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()
    
    