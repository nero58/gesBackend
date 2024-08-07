from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # path('csrf-token/', views.csrf_token_view, name='csrf_token'),#need to handle this
]