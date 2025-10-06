from users_app.api.serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from users_app.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


#list all users should be for admin only
class UserProfileAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

#will register users
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data('user')
        refresh = RefreshToken.for_user(user)

        dashboard_message = {
            "client": f"Hello - {user.first_name}, welcome to your dashboard",
            "writer": f"Hello - {user.first_name}, welcome to your dashboard",
        }.get(user.role, "Unknown role")

        return Response(
            {
                "user":{
                    "id":user.id,
                    'first_name':user.first_name,
                    'email':user.email,
                    'role':user.role,
                },
                'dashboard': dashboard_message,
            'tokens':{
                'refresh': str(refresh),
                'access':str(refresh.access_token),
            }
            }, status=status.HTTP_200_OK
        )



# Create your views here.
