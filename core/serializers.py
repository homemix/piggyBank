from rest_framework import serializers

from core.models import Currency, Category, Transaction


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)


class WriteTransactionSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        queryset=Currency.objects.all(),
        slug_field='code'
    )

    class Meta:
        model = Transaction
        fields = ['date', 'amount', 'currency', 'category', 'description']


class ReadTransactionSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'amount', 'currency', 'category', 'description']
        read_only_fields = fields
