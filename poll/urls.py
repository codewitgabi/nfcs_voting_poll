from django.urls import path
from . import views


app_name = "poll"
urlpatterns = [
	path("", views.index, name="index"),
	path("vote/<str:id>/", views.vote, name="vote"),
	path("result/", views.result, name="result"),
	path("download/", views.download_result, name="download_result"),
]