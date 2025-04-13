from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token
        token['username'] = user.username
        token['email'] = user.email  # if your user model has email
        # You can add more fields as needed, for example:
        # token['id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra data to the response
        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
            'id': self.user.id,
        }
        return data
