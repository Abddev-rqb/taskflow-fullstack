from django.urls import path
from .views import AdminDashboardView, UserDashboardView

urlpatterns = [
    path("admin/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("user/", UserDashboardView.as_view(), name="user-dashboard"),
]