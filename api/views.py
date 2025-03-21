from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId

from . import mongo_logic  # MongoDB logic

@api_view(["GET"])
def home(request):
    return Response({"message": "Welcome to PFA 2025 API!"})

@api_view(["POST"])
def register_user(request):
    data = request.data
    response = mongo_logic.register_user(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password")
    )
    return Response(response)

@api_view(["POST"])
def login_user(request):
    data = request.data
    response = mongo_logic.login_user(
        username=data.get("username"),
        password=data.get("password")
    )
    return Response(response)

@api_view(["POST"])
def upload_scanned_image(request):
    image_path = request.data.get("image_path")
    user_id = request.data.get("user_id")
    result = mongo_logic.save_scanned_image(image_path, user_id)
    return Response(result)

@api_view(["POST"])
def upload_uploaded_image(request):
    image_path = request.data.get("image_path")
    user_id = request.data.get("user_id")
    result = mongo_logic.save_uploaded_image(image_path, user_id)
    return Response(result)

@api_view(["GET"])
def unprocessed_images(request):
    images = mongo_logic.get_unprocessed_images()
    return Response(images)

@api_view(["GET"])
def classified_images(request):
    images = mongo_logic.get_classifications()
    return Response(images)

@api_view(["GET"])
def classification_detail(request):
    image_path = request.query_params.get("image_path")
    result = mongo_logic.get_classification_by_image(image_path)
    return Response(result)

@api_view(["POST"])
def update_classification(request):
    data = request.data
    mongo_logic.update_classification_result(
        image_path=data.get("image_path"),
        material_type=data.get("material_type"),
        recyclable=data.get("recyclable"),
        price=data.get("price"),
        triangle_code=data.get("triangle_code")
    )
    return Response({"message": "Classification updated"})

@api_view(["POST"])
def update_user_recycling_count(request):
    data = request.data
    user_id = ObjectId(data.get("user_id"))
    material_type = data.get("material_type")
    mongo_logic.update_user_recycled_count(user_id, material_type)
    return Response({"message": "User recycling count updated"})

@api_view(["GET"])
def user_profile(request):
    username = request.query_params.get("username")
    profile = mongo_logic.get_user_profile(username)
    return Response(profile)
