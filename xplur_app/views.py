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

# class Products(RetrieveAPIView):

#     permission_classes = (AllowAny,)
#     authentication_class = JSONWebTokenAuthentication

#     def get(self, request):
#         try:
#             product_list = Product.objects.all()
#             status_code = status.HTTP_200_OK
#             if product_list:
#                 response = {
#                     'success': 'true',
#                     'status code': status_code,
#                     'message': 'Product List fetched successfully',
#                     'data': ProductlistSerializer(product_list,many=True).data
#                     }

#             else:
#                 response = {
#                     'success': 'true',
#                     'status code': status_code,
#                     'message': 'Product List fetched successfully',
#                     'data': [{}]
#                     }

#         except Exception as e:
#             status_code = status.HTTP_400_BAD_REQUEST
#             response = {
#                 'success': 'false',
#                 'status code': status.HTTP_400_BAD_REQUEST,
#                 'message': 'Product List not exists',
#                 'error': str(e)
#                 }
#         return Response(response, status=status_code)
        
# class Product_create(CreateAPIView):

#     permission_classes = (IsAuthenticated,)
#     authentication_class = JSONWebTokenAuthentication
#     serializer_class = ProductlistSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         status_code = status.HTTP_201_CREATED
#         response = {
#             'success' : 'True',
#             'status code' : status_code,
#             'message': 'Product List Created  successfully',
#         }
#         return Response(response, status=status_code)










from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
import json

@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny,])
def Products(request):
    user = request.user.id
    products = Product.objects.all()
    serializer = ProductlistSerializer(products, many=True)
    return JsonResponse({'productss': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny,])
def Product_create(request):
    user = request.user
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
@permission_classes([AllowAny,])
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
@permission_classes([AllowAny,])
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

