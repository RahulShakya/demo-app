from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.accounts.serializers import UserSerializer


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
