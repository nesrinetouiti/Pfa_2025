import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image


from pymongo import MongoClient
from datetime import datetime
import mongo_logic  # Import the MongoDB logic file

# Load the AI model
MODEL_PATH = 'path/to/your/model.h5'  # Update with the correct path
model = tf.keras.models.load_model(MODEL_PATH)

# Function to process an image and predict recyclability
def predict_recyclability(image_path):
    img = image.load_img(image_path, target_size=(224, 224))  # Resize image
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize

    prediction = model.predict(img_array)
    return "Recyclable" if prediction[0][0] > 0.5 else "Not Recyclable"

# Function to process pending images and update MongoDB
def process_pending_images():
    pending_images = mongo_logic.get_unprocessed_images()  # Get images from MongoDB
    if not pending_images:
        print("No pending images to process.")
        return

    for image_data in pending_images:
        image_path = image_data["image_path"]
        result = predict_recyclability(image_path)

        # Example: Set material type and estimated price
        material_type = "Plastic" if result == "Recyclable" else "Unknown"
        estimated_price = 0.5 if result == "Recyclable" else 0.0
        triangle_code = "♻️" if result == "Recyclable" else None

        # Update classification result in MongoDB
        mongo_logic.update_classification_result(
            image_path=image_path,
            material_type=material_type,
            recyclable=result,
            price=estimated_price,
            triangle_code=triangle_code
        )

        print(f"Updated {image_path}: {result}")

# Run classification processing
if __name__ == "__main__":
    process_pending_images()
