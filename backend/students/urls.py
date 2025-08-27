from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("", views.student_list, name="student-list"),
    path("create/", views.student_create, name="student-create"),
    path("<int:pk>/", views.student_detail, name="student-detail"),
]
