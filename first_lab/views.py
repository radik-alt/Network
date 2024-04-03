from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from first_lab.models import Region, BookLover, Book, Publisher
from first_lab.serializator import RegionSerializer, BookLoverSerializer, UserSerializer, BookSerializer, \
    PublisherSerializer


def index(request):
    return HttpResponse("Hello world!")


class RegionViewSet(viewsets.ViewSet):

    @staticmethod
    def get_ordering(request):
        try:
            return request.GET.get('ordering')
        except Exception:
            return None

    @staticmethod
    def get_pagination(request):
        try:
            page = int(request.GET.get('page'))
            page_size = int(request.GET.get('pagesize'))
            return {'page': page, 'page_size': page_size}
        except Exception:
            return None

    @staticmethod
    def get_filter_region_name(request):
        try:
            return request.GET.get('name')
        except Exception:
            return None

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('ordering', openapi.IN_QUERY, description="Ordering (asc or desc)", type=openapi.TYPE_STRING),
        openapi.Parameter('name', openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('pagesize', openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER),
    ], responses={200: BookSerializer()})
    def get(self, request):
        pagination_data = self.get_pagination(request)
        if pagination_data:
            page = pagination_data['page']
            page_size = pagination_data['page_size']
        else:
            page = None
            page_size = None

        queryset = Region.objects.all()
        ordering = self.get_ordering(request)
        name_region = self.get_filter_region_name(request)

        if name_region:
            queryset = queryset.filter(name=name_region)

        if ordering == 'asc':
            queryset = queryset.order_by('code')
        elif ordering == 'desc':
            queryset = queryset.order_by('-code')

        paginator = MyModelPagination(page, page_size)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = RegionSerializer(result_page, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegionViewSetById(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        try:
            return Region.objects.get(pk=pk)
        except Region.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: RegionSerializer()})
    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = RegionSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        region = self.get_object(pk)
        serializer = RegionSerializer(region, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        region = self.get_object(pk)
        region.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyModelPagination(PageNumberPagination):

    def __init__(self, page, page_size):
        if page is not None:
            self.page = page
        else:
            self.page = 1

        if page_size is not None:
            self.page_size = page_size
        else:
            self.page_size = 10

    page = 1
    page_size_query_param = 'page_size'
    page_size = 10


class BookLoverViewSet(viewsets.ViewSet):

    @staticmethod
    def get_ordering(request):
        try:
            return request.GET.get('ordering')
        except Exception:
            return None

    @staticmethod
    def get_filter_first_name(request):
        try:
            return request.GET.get('first_name')
        except Exception:
            return None

    @staticmethod
    def get_filter_birthday(request):
        try:
            return request.GET.get('birthday')
        except Exception:
            return None

    @staticmethod
    def get_filter_date_of_joining(request):
        try:
            return request.GET.get('date_of_joining')
        except Exception:
            return None

    @staticmethod
    def get_pagination(request):
        try:
            page = int(request.GET.get('page'))
            page_size = int(request.GET.get('pagesize'))
            return {'page': page, 'page_size': page_size}
        except Exception:
            return None

    @staticmethod
    def get_parameters():
        return [
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Ordering ('asc' or 'desc')",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('first_name', openapi.IN_QUERY, description="First name to filter by",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('birthday', openapi.IN_QUERY, description="Birthday to filter by",
                              type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('date_of_joining', openapi.IN_QUERY, description="Date of joining to filter by",
                              type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number for pagination",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Page size for pagination",
                              type=openapi.TYPE_INTEGER),
        ]

    @swagger_auto_schema(manual_parameters=get_parameters())
    def get(self, request):
        pagination_data = self.get_pagination(request)
        if pagination_data:
            page = pagination_data['page']
            page_size = pagination_data['page_size']
        else:
            page = None
            page_size = None

        filter_birthday = self.get_filter_birthday(request)
        filter_date_of_joint = self.get_filter_date_of_joining(request)
        filter_first_name = self.get_filter_first_name(request)
        ordering = self.get_ordering(request)

        queryset = BookLover.objects.all()

        if filter_first_name:
            queryset = queryset.filter(first_name=filter_first_name)
        elif filter_birthday:
            queryset = queryset.filter(birthday=filter_birthday)
        elif filter_date_of_joint:
            queryset = queryset.filter(date_of_joining=filter_date_of_joint)

        if ordering == 'asc':
            queryset = queryset.order_by('birthday')
        elif ordering == 'desc':
            queryset = queryset.order_by('-birthday')

        paginator = MyModelPagination(page, page_size)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = BookLoverSerializer(result_page, many=True)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=BookLoverSerializer)
    def create(self, request):
        serializer = BookLoverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookLoverViewSetById(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_object(pk):
        try:
            return BookLover.objects.get(pk=pk)
        except BookLover.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: BookLoverSerializer()})
    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = BookLoverSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BookLoverSerializer)
    def update(self, request, pk):
        book_lover = self.get_object(pk)
        serializer = BookLoverSerializer(book_lover, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book_lover = self.get_object(pk)
        book_lover.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthViewSet(viewsets.ViewSet):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            Token.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        else:
            return Response({'error': 'Некорректные данные. Проверьте логин и пароль'},
                            status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: 'Successfully logged out'})
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'UNAUTHORIZED'}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def get_password(request):
        try:
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            return {"old_password": old_password, "new_password": new_password}
        except Exception:
            raise Http404
            # return {"old_password": None, "new_password": None}

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'old_password': openapi.Schema(type=openapi.TYPE_STRING),
            'new_password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        try:
            user = request.user
            passwords = self.get_password(request)
            old_password = passwords.get('old_password')
            new_password = passwords.get('new_password')

            if not user.check_password(old_password):
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password successfully changed'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'UNAUTHORIZED'}, status=status.HTTP_401_UNAUTHORIZED)


class PublisherViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_ordering(request):
        try:
            return request.GET.get('ordering')
        except Exception:
            return None

    @staticmethod
    def get_filter_name(request):
        try:
            return request.GET.get('name')
        except Exception:
            return None

    @staticmethod
    def get_pagination(request):
        try:
            page = int(request.GET.get('page'))
            page_size = int(request.GET.get('pagesize'))
            return {'page': page, 'page_size': page_size}
        except Exception:
            return None

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Ordering parameter ('asc' or 'desc')",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('pagesize', openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER),
        ],
        responses={200: PublisherSerializer(many=True)}
    )
    def list(self, request):
        ordering = self.get_ordering(request)
        filter_name = self.get_filter_name(request)
        pagination_data = self.get_pagination(request)
        if pagination_data:
            page = pagination_data['page']
            page_size = pagination_data['page_size']
        else:
            page = None
            page_size = None

        queryset = Publisher.objects.all()

        if filter_name:
            queryset = queryset.filter(name=filter_name)

        if ordering == 'asc':
            queryset = queryset.order_by('region')
        elif ordering == 'desc':
            queryset = queryset.order_by('-region')

        paginator = MyModelPagination(page, page_size)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PublisherSerializer(result_page, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PublisherSerializer)
    def create(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: PublisherSerializer()})
    def retrieve(self, request, pk=None):
        queryset = Publisher.objects.all()
        book = get_object_or_404(queryset, pk=pk)
        serializer = PublisherSerializer(book)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: PublisherSerializer()})
    def update(self, request, pk=None):
        book = Publisher.objects.get(pk=pk)
        serializer = PublisherSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        book = Publisher.objects.get(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_ordering(request):
        try:
            return request.GET.get('ordering')
        except Exception:
            return None

    @staticmethod
    def get_filter_name(request):
        try:
            return request.GET.get('title')
        except Exception:
            return None

    @staticmethod
    def get_pagination(request):
        try:
            page = int(request.GET.get('page'))
            page_size = int(request.GET.get('pagesize'))
            return {'page': page, 'page_size': page_size}
        except Exception:
            return None

    @staticmethod
    def get_filter_date(request):
        try:
            return request.GET.get('year')
        except Exception:
            return None

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('ordering', openapi.IN_QUERY, description="Ordering (asc or desc)", type=openapi.TYPE_STRING),
        openapi.Parameter('title', openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING),
        openapi.Parameter('year', openapi.IN_QUERY, description="Filter by year", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('pagesize', openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER),
    ], responses={200: BookSerializer()})
    def list(self, request):
        ordering = self.get_ordering(request)
        filter_title = self.get_filter_name(request)
        pagination_data = self.get_pagination(request)
        filter_date = self.get_filter_date(request)

        if pagination_data:
            page = pagination_data['page']
            page_size = pagination_data['page_size']
        else:
            page = None
            page_size = None

        queryset = Book.objects.all()

        if filter_title:
            queryset = queryset.filter(title=filter_title)
        if filter_date:
            queryset = queryset.filter(year_of_release=filter_date)

        if ordering == 'asc':
            queryset = queryset.order_by('id_book')
        elif ordering == 'desc':
            queryset = queryset.order_by('-id_book')

        paginator = MyModelPagination(page, page_size)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = BookSerializer(result_page, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: BookSerializer()})
    def retrieve(self, request, pk=None):
        queryset = Book.objects.all()
        publisher = get_object_or_404(queryset, pk=pk)
        serializer = BookSerializer(publisher)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=BookSerializer)
    def create(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: BookSerializer()})
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BookSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        queryset = Book.objects.all()
        instance = get_object_or_404(queryset, pk =pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
