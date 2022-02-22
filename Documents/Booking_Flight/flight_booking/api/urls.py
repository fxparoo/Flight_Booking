from django.urls import path, include
import api.views as apv
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('accounts/', include('rest_registration.api.urls')),
    path('account/token/', apv.LoginTokenViewSet.as_view(), name='token'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('change-password/<int:pk>/', apv.ChangePasswordView.as_view(), name='token_verify')

]
