from django.urls import path
from .views import QueryView, QuestionsListView

urlpatterns = [
    path("query/", QueryView.as_view(), name="query"),
    path("questions/", QuestionsListView.as_view(), name="questions"),
]
