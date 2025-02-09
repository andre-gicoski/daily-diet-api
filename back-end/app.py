from flask import Flask, request, jsonify
from models.meal import Meal
from database import db
from models.schema import MealSchema

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


def handle_error(exception, data):
    return (
        jsonify(
            {"error": f"Ocorreu um erro: {str(exception)}", "dados_enviados": data}
        ),
        400,
    )


@app.route("/meal", methods=["POST"])
def create_meal():
    if verify_key():
        return verify_key()

    data = request.get_json()
    meal_schema = MealSchema()

    try:
        new_meal = meal_schema.load(data, session=db.session)
        db.session.add(new_meal)
        db.session.commit()
        return jsonify(meal_schema.dump(new_meal)), 201
    except Exception as e:
        return handle_error(e, data)


@app.route("/meal", methods=["GET"])
def get_all_meals():
    if verify_key():
        return verify_key()

    meals = Meal.query.all()
    if meals:
        meal_schema = MealSchema(many=True)
        return jsonify(meal_schema.dump(meals))

    return jsonify({"message": "Nenhuma refeição encontrada"}), 404


@app.route("/meal/<int:id_meal>", methods=["GET"])
def read_meal(id_meal):
    if verify_key():
        return verify_key()

    meal = db.session.get(Meal, id_meal)
    if meal:
        meal_schema = MealSchema()
        return jsonify(meal_schema.dump(meal))

    return jsonify({"message": "Refeição não encontrada"}), 404


@app.route("/meal/<int:id_meal>", methods=["DELETE"])
def delete_meal(id_meal):
    if verify_key():
        return verify_key()

    meal = db.session.get(Meal, id_meal)
    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": f"Refeição {id_meal} deletada com sucesso"})

    return jsonify({"message": "Refeição não encontrada nesse ID"}), 404


@app.route("/meal/<int:id_meal>", methods=["PUT"])
def update_meal(id_meal):
    if verify_key():
        return verify_key()

    data = request.get_json()
    meal = db.session.get(Meal, id_meal)

    if not meal:
        return jsonify({"error": "Refeição não encontrada com o ID especificado"}), 404

    meal_schema = MealSchema()
    try:
        meal_schema.load(data, instance=meal, session=db.session, partial=True)
        db.session.commit()
        return jsonify(meal_schema.dump(meal)), 200
    except Exception as e:
        return handle_error(e, data)


if __name__ == "__main__":
    app.run(debug=True)
