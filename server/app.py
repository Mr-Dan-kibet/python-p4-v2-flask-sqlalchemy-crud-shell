from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Pet

# Create Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# -------------------------------
# ROUTES
# -------------------------------

@app.route("/")
def home():
    return "Welcome to the Pet API! Use /pets to interact."

# --- CREATE a new pet ---
@app.route("/pets", methods=["POST"])
def create_pet():
    data = request.get_json()
    name = data.get("name")
    species = data.get("species")
    if not name or not species:
        return jsonify({"error": "Name and species are required"}), 400

    pet = Pet(name=name, species=species)
    db.session.add(pet)
    db.session.commit()
    return jsonify({"message": "Pet created", "pet": {"id": pet.id, "name": pet.name, "species": pet.species}}), 201

# --- READ all pets ---
@app.route("/pets", methods=["GET"])
def get_pets():
    pets = Pet.query.all()
    result = [{"id": p.id, "name": p.name, "species": p.species} for p in pets]
    return jsonify(result)

# --- READ a single pet by ID ---
@app.route("/pets/<int:pet_id>", methods=["GET"])
def get_pet(pet_id):
    pet = db.session.get(Pet, pet_id)
    if not pet:
        return jsonify({"error": "Pet not found"}), 404
    return jsonify({"id": pet.id, "name": pet.name, "species": pet.species})

# --- UPDATE a pet ---
@app.route("/pets/<int:pet_id>", methods=["PUT"])
def update_pet(pet_id):
    pet = db.session.get(Pet, pet_id)
    if not pet:
        return jsonify({"error": "Pet not found"}), 404

    data = request.get_json()
    pet.name = data.get("name", pet.name)
    pet.species = data.get("species", pet.species)
    db.session.commit()
    return jsonify({"message": "Pet updated", "pet": {"id": pet.id, "name": pet.name, "species": pet.species}})

# --- DELETE a pet ---
@app.route("/pets/<int:pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    pet = db.session.get(Pet, pet_id)
    if not pet:
        return jsonify({"error": "Pet not found"}), 404

    db.session.delete(pet)
    db.session.commit()
    return jsonify({"message": f"Pet {pet_id} deleted"})

# --- DELETE all pets ---
@app.route("/pets", methods=["DELETE"])
def delete_all_pets():
    num_deleted = Pet.query.delete()
    db.session.commit()
    return jsonify({"message": f"Deleted {num_deleted} pets"})

# -------------------------------
# Run the app
# -------------------------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)
