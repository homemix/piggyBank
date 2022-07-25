from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .reports import transaction_report

from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, WriteTransactionSerializer, ReadTransactionSerializer, \
    ReportEntrySerializer, ReportParamsSerializer


class CurrencyListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
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


class TransactionReportApiView(APIView):

    @staticmethod
    def get(request):
        params_serializer = ReportParamsSerializer(data=request.GET, context={'request': request})
        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.save()

        data = transaction_report(params)
        serializer = ReportEntrySerializer(instance=data, many=True)
        return Response(data=serializer.data)
