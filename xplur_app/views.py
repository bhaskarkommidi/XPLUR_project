from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer,UserLoginSerializer,ProductlistSerializer
from rest_framework.generics import RetrieveAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import UserProfile,Product




class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
    	serializer = self.serializer_class(data=request.data)
    	serializer.is_valid(raise_exception=True)
    	serializer.save()
    	status_code = status.HTTP_201_CREATED
    	response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
        }
    	return Response(response, status=status_code)
    	


class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
    	serializer = self.serializer_class(data=request.data)
    	serializer.is_valid(raise_exception=True)
    	response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
    	status_code = status.HTTP_200_OK
    	return Response(response, status=status_code)

######################################### Product ############################



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def Products(request):
    user = request.user.id
    products = Product.objects.all()
    serializer = ProductlistSerializer(products, many=True)
    return JsonResponse({'productss': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def Product_create(request):
    user = request.user
    import ipdb; ipdb.set_trace()
    try:
        payload = json.loads(request.body)
        product = Product.objects.create(
            sku=payload["sku"],
            name=payload["name"],
            description=payload["description"],
            category=payload["category"],
            price=payload["price"],
            metadata=payload["metadata"] if payload["metadata"] else None,
            
        )
        serializer = ProductlistSerializer(product)
        return JsonResponse({'product': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def Product_update(request, product_id):
    user = request.user.id
    try:
        payload = json.loads(request.body)
        product_item = Product.objects.filter(id=product_id)
        # returns 1 or 0
        product_item.update(**payload)
        product = Product.objects.get(id=product_id)
        serializer = ProductlistSerializer(product)
        return JsonResponse({'product': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def Product_delete(request, product_id):
    user = request.user.id
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

