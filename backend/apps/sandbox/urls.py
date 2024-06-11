from django.urls import path
from .views import PointListCreateAPIView, PointRetrieveUpdateDestroyAPIView

urlpatterns = [
    # path('points/', PointListCreateAPIView.as_view(), name='point-list-create'),
    # path('points/<int:pk>/', PointRetrieveUpdateDestroyAPIView.as_view(), name='point-detail'),
]
