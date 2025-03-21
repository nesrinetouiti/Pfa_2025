from pymongo import MongoClient
from datetime import datetime
import bcrypt

# Connect to MongoDB and define collections
client = MongoClient("mongodb://localhost:27017/")
db = client["recycling_db"]
classifications = db["classifications"]
users = db["users"]
statistics = db["statistics"]

# Save a scanned image to the database with 'pending' status
def save_scanned_image(image_path, user_id):
    data = {
        "user_id": user_id,
        "image_path": image_path,
        "source": "scan",
        "status": "pending",
        "timestamp": datetime.utcnow()
    }
    classifications.insert_one(data)
    return data

# Save an uploaded image to the database with 'pending' status
def save_uploaded_image(image_path, user_id):
    data = {
        "user_id": user_id,
        "image_path": image_path,
        "source": "upload",
        "status": "pending",
        "timestamp": datetime.utcnow()
    }
    classifications.insert_one(data)
    return data

# Retrieve all images that have not yet been classified
def get_unprocessed_images():
    return list(classifications.find({"status": "pending"}, {"_id": 0}))

# Update a classification entry after the model has processed the image
def update_classification_result(image_path, material_type, recyclable, price, triangle_code=None):
    update_data = {
        "material_type": material_type,
        "recyclable": recyclable,
        "estimated_price": price,
        "status": "classified"
    }
    if triangle_code:
        update_data["triangle_code"] = triangle_code

    classifications.update_one(
        {"image_path": image_path},
        {"$set": update_data}
    )

# Retrieve all images that have been classified
def get_classifications():
    return list(classifications.find({"status": "classified"}, {"_id": 0}))

# Retrieve classification details for a specific image
def get_classification_by_image(image_path):
    return classifications.find_one({"image_path": image_path}, {"_id": 0})

# Update the recycling price for a specific material type
def update_recycling_price(material_type, new_price):
    classifications.update_many(
        {"material_type": material_type},
        {"$set": {"estimated_price": new_price}}
    )

# Retrieve overall classification statistics
def get_statistics():
    return list(statistics.find({}, {"_id": 0}))

# Register a new user with hashed password and initialize recycling counts
def register_user(username, email, password):
    existing_user = users.find_one({"username": username})
    if existing_user:
        return {"error": "Username already exists"}

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = {
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "recycled_items": {
            "Plastic": 0,
            "Glass": 0,
            "Aluminum": 0
        },
        "created_at": datetime.utcnow()
    }
    users.insert_one(user)
    return {"message": "User registered successfully"}

# Authenticate a user by verifying their username and password
def login_user(username, password):
    user = users.find_one({"username": username})
    if not user:
        return {"error": "User not found"}

    if bcrypt.checkpw(password.encode('utf-8'), user["password_hash"]):
        return {"message": "Login successful", "user_id": str(user["_id"])}
    else:
        return {"error": "Incorrect password"}

# Update the count of recycled items for a specific user and material
def update_user_recycled_count(user_id, material_type):
    users.update_one(
        {"_id": user_id},
        {"$inc": {f"recycled_items.{material_type}": 1}}
    )

# Retrieve a user's profile including their recycling statistics
def get_user_profile(username):
    return users.find_one({"username": username}, {"_id": 0, "password_hash": 0})
