from django.urls import path
from .views import storage, StorageUpdateView, StorageDeleteView

app_name = 'storage'

urlpatterns = [
    path('', storage, name='storage'),
    path('update/<int:pk>/', StorageUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', StorageDeleteView.as_view(), name='delete'),
]
