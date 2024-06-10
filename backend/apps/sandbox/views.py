from rest_framework import generics
from .models import Point
from .serializers import PointInputSerializer, PointOutputSerializer


class PointListCreateAPIView(generics.ListCreateAPIView):
    queryset = Point.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PointInputSerializer
        return PointOutputSerializer


class PointRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Point.objects.all()
    serializer_class = PointOutputSerializer
