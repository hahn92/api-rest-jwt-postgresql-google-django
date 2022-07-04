from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer
from TheLibrary.googleAuth import authorize

# Custom User
from django.contrib.auth import get_user_model
User = get_user_model()


class ListUsersAPIView(APIView):
    """
    - Consulta Usuario
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        user = User.objects.get(id=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)



@api_view(['GET', 'POST'])
def registerToken(request):
    """
    - Registra un token
    """
    if request.method == 'GET':
        return Response({'status': 'ok'})

    if request.method == 'POST':
        authorize()
        return Response({'status': 'ok'})