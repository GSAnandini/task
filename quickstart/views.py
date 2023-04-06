from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Book, BookIssue
from .serializers import BookSerializer, BookIssueSerializer
from rest_framework import generics, permissions
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from datetime import date
from django.http import request
from django.shortcuts import get_object_or_404
from .models import BookIssue


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
         # Generate a unique username
        user = User(username=username, email=email, password=make_password(password))
        user.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookCreate(generics.CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]


class BookIssueCreate(APIView):
    serializer_class = BookIssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        book = request.data.get('book')
        stat = request.data.get('stat')
        return_date = request.data.get('return_date')

        try:
            book = Book.objects.get(id=book)
        except Book.DoesNotExist:
            return Response({'error': 'Invalid book ID'}, status=status.HTTP_400_BAD_REQUEST)

        book_issue = BookIssue(user=user, book=book, stat=stat, return_date=return_date)
        book_issue.save()

        return Response({'message': 'Book issued successfully'}, status=status.HTTP_201_CREATED)






class BookReturnUpdate(generics.UpdateAPIView):
    serializer_class = BookIssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            # Get the BookIssue instance with the given pk
            book_issue = BookIssue.objects.get(pk=pk)
        except BookIssue.DoesNotExist:
            return Response({'error': 'BookIssue does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update the status and return_date fields
        book_issue.stat = 'returned'
        book_issue.return_date = date.today()
        book_issue.save()
        
        return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)





@api_view(['GET'])
def user_book_list(request):
    user = request.user
    books = BookIssue.objects.filter(user=user)
    serializer = BookIssueSerializer(books, many=True)
    return Response(serializer.data)