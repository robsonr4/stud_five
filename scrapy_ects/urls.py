import django
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import MainView, UniTestView, UniView, UniPointsView, UniInfoView


urlpatterns = [
    path('home/', MainView.as_view(), name="home"),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path('profile/', MainView, name="profile"),
    path('profile/settings/', MainView, name="settings"),
    path('uni/', UniView.as_view(), name="uni"),
    path('uni/points/', UniPointsView.as_view(), name="uni_points"),
    path('uni/test/', UniTestView.as_view(), name="uni_test"),
    path('uni/info', UniInfoView.as_view(), name="uni_info"),
    path('task-manager/', MainView, name="task_manager"),
    path('calendar', MainView, name="calendar"),
]
