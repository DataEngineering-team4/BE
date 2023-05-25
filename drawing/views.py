from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from drawing.models import Animation, Drawing
from drawing.serializer import (AnimationInfoSerializer,
                                AnimationPostSerializer, DrawingInfoSerializer,
                                DrawingPostSerializer)


# Create your views here.
class DrawingAPI(APIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DrawingPostSerializer
        return DrawingInfoSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass


class AnimationAPI(APIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DrawingPostSerializer
        return DrawingInfoSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass
