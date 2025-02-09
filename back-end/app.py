from flask import Flask, request, jsonify
from models.meal import Meal
from database import db
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///daily_diet.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
API_KEYS = {"secret-key"}

db.init_app(app)

with app.app_context():
    db.create_all()


def verify_key():
    key = request.headers.get("X-API-KEY")
    if key not in API_KEYS:
        return jsonify({"erro": "Acesso negado, chave inválida"}), 403
    return None


@app.route("/meal", methods=["POST"])
def create_meal():
    auth = verify_key()
    if auth:
        return auth

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
    auth = verify_key()
    if auth:
        return auth
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
    auth = verify_key()
    if auth:
        return auth
    meal = db.session.get(Meal, id_meal) 
    if meal:
        return jsonify(
            {
                "name": meal.name,
                "description": meal.description,
                "date_time": meal.date_time.strftime("%Y-%m-%d %H:%M:%S"),
                "within_diet": meal.within_diet,
            }
        )

    return jsonify({"message": "Refeição não encontrada"}), 404


@app.route("/meal/<int:id_meal>", methods=["DELETE"])
def delete_meal(id_meal):
    auth = verify_key()
    if auth:
        return auth
    meal = db.session.get(Meal, id_meal) 
    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": f"Refeição {id_meal} deletada com sucesso"})

    return jsonify({"message": "Refeição não encontrada nesse ID"}), 404


@app.route("/meal/<int:id_meal>", methods=["PUT"])
def update_meal(id_meal):
    auth = verify_key()
    if auth:
        return auth
    data = request.get_json()
    meal = db.session.get(Meal, id_meal)

    if data and meal:
        meal.name = data.get("name")
        meal.description = data.get("description")
        meal.date_time = datetime.strptime(data.get("date_time"), "%Y-%m-%d %H:%M:%S")
        meal.within_diet = data.get("within_diet")

        db.session.commit()

        return (
            jsonify(
                {
                    "message": f"A refeição '{meal.name}' foi atualizada com sucesso!",
                    "description": meal.description,
                    "date_time": meal.date_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "within_diet": meal.within_diet,
                }
            ),
            200,
        )

    return jsonify({"error": "Refeição não encontrada"}), 400


if __name__ == "__main__":
    app.run(debug=True)
