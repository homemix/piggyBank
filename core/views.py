from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, WriteTransactionSerializer, ReadTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # queryset = Transaction.objects.all()
    # queryset = Transaction.objects.select_related('currency', 'category','user').all()
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('description',)
    ordering_fields = ('amount',)

    def get_queryset(self):
        return Transaction.objects.select_related(
            'currency', 'category', 'user'
        ).filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadTransactionSerializer
        return WriteTransactionSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
