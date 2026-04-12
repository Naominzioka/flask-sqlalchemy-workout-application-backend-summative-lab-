from marshmallow import Schema, fields, validates_schema, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Boolean(load_default=False)
    
    @validates_schema
    def validate_schema(self, data, **kwargs):
        valid_categories = ['Pilates', 'Yoga', 'Aerobics', 'Cardio', 'Bodybuilding']
        if data['category'] not in valid_categories:
            raise ValidationError('Category must be one of these: Pilates, Yoga, Aerobics, Cardio, Bodybuilding')
        if not data['name'] or data['name'].strip() == '':
            raise ValidationError('Name cannot be empty')
        
    
    
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(allow_none=True)
    duration_minutes = fields.Int(allow_none=True)
    notes = fields.Str(allow_none=True)
    
    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('duration_minutes') is not None and data['duration_minutes'] < 0:
            raise ValidationError('Duration minutes must be a positive numbrer')
        if data.get('notes') is not None and len(data['notes']) > 300:
            raise ValidationError('Notes must be less than 300 characters long')
    
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)
    
    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('duration_seconds') is not None and data['duration_seconds'] < 0:
            raise ValidationError('Duration seconds must be a positive number')
    
    
