from django.urls import path
from views import writing_to_csv

urlpatterns = [
    path("level_data/", writing_to_csv, name="writing_to_csv")
]
