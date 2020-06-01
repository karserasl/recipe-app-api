# @Author: Lam
# @Date:   31/05/2020 13:58
from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    # If requested from app.urls && the endpoints is in the request, use the View in user.
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
