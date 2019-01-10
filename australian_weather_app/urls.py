from django.urls import path, include
from australian_weather_app import views

urlpatterns = [
    path(r'home/', views.home, name="home"),

    # User management
    path(r'accounts/signup/', views.SignUp.as_view(), name="signup"),
    path(r'accounts/', include('django.contrib.auth.urls')),

    # Record management
    path(r'add_observation/', views.add_observation, name="add_observation"),
    path(r'list_observations/', views.list_observations, name="list_observations"),
    path(r'edit_observation/<int:observation_id>/', views.edit_observation, name="edit_observation"),
    path(r'delete_observation/', views.delete_observation, name="delete_observation"),

    # Prediction
    path(r'predict_rainfall/', views.predict_rainfall, name="predict_rainfall")
]
