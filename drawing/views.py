from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from drawing.models import Animation, Drawing
from drawing.serializer import (AnimationInfoSerializer,
                                AnimationPostSerializer, DrawingInfoSerializer,
                                DrawingPostSerializer)
from user.models import User


# Create your views here.
class DrawingAPI(APIView):
    serializer_class = DrawingPostSerializer

    def get(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.filter(id=user_id).first()
        drawings = user.drawings.all() if user else []
        return Response(DrawingInfoSerializer(
            drawings, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            user_id = request.data['user_id']
            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({
                    "status": "error",
                    "message": "User does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                name = request.data['name']
                file = request.data['file']
                drawing = Drawing.objects.create(
                    user=user,
                    name=name,
                    file=file,
                    status='pending')
                return Response({
                    "status": "success",
                    "message": "Image Uploaded Successfully",
                    "data": DrawingInfoSerializer(drawing).data
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class AnimationAPI(APIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnimationPostSerializer
        return AnimationInfoSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass
