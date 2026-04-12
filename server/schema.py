from marshmallow import Schema, fields

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Boolean(load_default=False)
    
    
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(allow_none=True)
    duration_minutes = fields.Int(allow_none=True)
    notes = fields.Str(allow_none=True)
    
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    
    
