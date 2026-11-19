from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book
from .pagination import RoleBasedPageSizePagination
from .permissions import IsEduDomainOrReadOnly
from .serializers import AuthorSerializer, BookSerializer


class TokenLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if hasattr(request, "auth") and request.auth:
            request.auth.delete()
        elif hasattr(request.user, "auth_token"):
            request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """Публічний довідник авторів: читати може будь-хто. Не змінюйте права тут."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsEduDomainOrReadOnly]
    pagination_class = RoleBasedPageSizePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author__name"]
    ordering_fields = ["price", "title"]

    def perform_create(self, serializer):
        owner = self.request.user if self.request.user.is_authenticated else None
        serializer.save(owner=owner)
