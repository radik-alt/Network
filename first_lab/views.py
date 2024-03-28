from django.contrib.auth import authenticate
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
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
    regions = Region.objects.all()
    print(regions.values())

    return HttpResponse("Hello world!")


class RegionViewSet(viewsets.ViewSet):

    def get(self, request):
        try:
            page = int(request.GET.get('page'))
            page_size = int(request.GET.get('pagesize'))
        except:
            page = None
            page_size = None

        queryset = Region.objects.all()
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
            return Response(status=status.HTTP_404_NOT_FOUND)

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
            self.page = 10

        if page_size is not None:
            self.page_size = page_size
        else:
            self.page_size = 100

    page = 10
    page_size_query_param = 'page_size'
    page_size = 100


class BookLoverViewSet(viewsets.ViewSet):

    def get(self, request):
        try:
            page = int(request.GET.get('page'))
            page_size = int(request.GET.get('pagesize'))
        except:
            page = None
            page_size = None

        filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
        filterset_fields = ['name', 'age']  # Поля для фильтрации
        ordering_fields = ['name', 'age']  # Поля для сортировки

        queryset = BookLover.objects.all()
        paginator = MyModelPagination(page, page_size)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = BookLoverSerializer(result_page, many=True)
        return Response(data=serializer.data)


class BookLoverViewSetById(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        try:
            return BookLover.objects.get(pk=pk)
        except Region.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = BookLoverSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class PublisherViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        queryset = Publisher.objects.all()
        serializer = PublisherSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Publisher.objects.all()
        book = get_object_or_404(queryset, pk=pk)
        serializer = PublisherSerializer(book)
        return Response(serializer.data)

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

    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Book.objects.all()
        publisher = get_object_or_404(queryset, pk=pk)
        serializer = BookSerializer(publisher)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BookSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
