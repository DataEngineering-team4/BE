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
        try:
            user_id = request.GET.get('user_id')
            user = User.objects.filter(id=user_id).first()
            drawings = user.drawings.all() if user else []
            return Response(DrawingInfoSerializer(
                drawings, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

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
    serializer_class = AnimationPostSerializer

    def get(self, request):
        try:
            user_id = request.GET.get('user_id')
            drawing_id = request.GET.get('drawing_id')
            user = User.objects.filter(id=user_id).first()
            drawing = Drawing.objects.filter(id=drawing_id).first()
            if drawing in user.drawings.all():
                return Response(
                    AnimationInfoSerializer(
                        drawing.animations.all(), many=True).data,
                    status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "Drawing is not for this user"
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            drawing_id = request.data['drawing_id']
            drawing = Drawing.objects.filter(id=drawing_id).first()
            if not drawing:
                return Response({
                    "status": "error",
                    "message": "Drawing does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                purpose = request.data['purpose']
                file = request.data['file']
                animation = Animation.objects.create(
                    drawing=drawing,
                    purpose=purpose,
                    file=file)
                return Response({
                    "status": "success",
                    "message": "Image Uploaded Successfully",
                    "data": AnimationInfoSerializer(animation).data
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
