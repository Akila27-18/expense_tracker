from django.contrib import admin
from django.urls import path, include
from tracker import views as tracker_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", tracker_views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="tracker/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", tracker_views.dashboard, name="dashboard"),
    path("expenses/", tracker_views.expense_list, name="expense_list"),
    path("expenses/add/", tracker_views.expense_create, name="expense_create"),
    path("expenses/<int:pk>/edit/", tracker_views.expense_edit, name="expense_edit"),
    path("expenses/<int:pk>/delete/", tracker_views.expense_delete, name="expense_delete"),
]
