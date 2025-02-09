from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, ValidationError
from models.meal import Meal
from datetime import datetime

def validate_datetime(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValidationError("Formato de data inválido. Use o formato 'YYYY-MM-DD HH:MM:SS'.")

class MealSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Meal
        load_instance = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=False)
    date_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)
    within_diet = fields.Bool(required=True)

meal_schema = MealSchema()
meals_schema = MealSchema(many=True)

