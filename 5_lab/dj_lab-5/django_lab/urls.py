from django.urls import path

from .views import ChanCreateView, ChanDeleteView, ChanEditView

urlpatterns = [
    path('', ChanCreateView.as_view()),
    path('<int:pk>/', ChanEditView.as_view()),
    path('<int:pk>/delete', ChanDeleteView.as_view())
]
