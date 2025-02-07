from flask import Flask, request, jsonify
from models.meal import Meal
from database import db
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///daily_diet.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/meal", methods=["POST"])
def create_meal():
    data = request.get_json()

    name = data.get("name")
    description = data.get("description")
    date_time = data.get("date_time")
    within_diet = data.get("within_diet")

    if name and description and date_time and within_diet is not None:
        try:
            date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return (
                jsonify(
                    {
                        "message": "Formato de data inválido. Use o formato 'YYYY-MM-DD HH:MM:SS'."
                    }
                ),
                400,
            )

        new_meal = Meal(
            name=name,
            description=description,
            date_time=date_time,
            within_diet=within_diet,
        )

        db.session.add(new_meal)
        db.session.commit()

        return jsonify({"message": "Refeição cadastrada com sucesso"}), 201

    return jsonify({"message": "Dados inválidos"}), 400


@app.route("/meal", methods=["GET"])
def get_all_meals():
    meals = Meal.query.all()

    if meals:
        return jsonify(
            [
                {
                    "name": meal.name,
                    "description": meal.description,
                    "date_time": meal.date_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "within_diet": meal.within_diet,
                }
                for meal in meals
            ]
        )

    return jsonify({"message": "Nenhuma refeição encontrada"}), 404


@app.route("/meal/<int:id_meal>", methods=["GET"])
def read_meal(id_meal):
    meal_data = Meal.query.get(id_meal)
    if meal_data:
        return jsonify(
            {
                "name": meal_data.name,
                "description": meal_data.description,
                "date_time": meal_data.date_time.strftime("%Y-%m-%d %H:%M:%S"),
                "within_diet": meal_data.within_diet,
            }
        )

    return jsonify({"message": "Refeição não encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)
