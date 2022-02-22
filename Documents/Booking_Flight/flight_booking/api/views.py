from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
import api.models as am
import api.serializers as aps


class LoginTokenViewSet(TokenObtainPairView):
    serializer_class = aps.LoginTokenSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = am.AppUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = aps.ChangePasswordSerializer

