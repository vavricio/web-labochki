from django.contrib import admin
from django.urls import path

from fibonacci.views import ExampleView, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calculation', ExampleView.as_view()),
    path('', index)
]
