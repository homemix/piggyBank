from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Currency, Category, Transaction


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = fields


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ('id',)


class WriteTransactionSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        queryset=Currency.objects.all(),
        slug_field='code'
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = ['user', 'date', 'amount', 'currency', 'category', 'description']

    def __int__(self, *args, **kwargs):
        super().__int__(*args, **kwargs)
        self.fields['user'].queryset = Category.objects.filter(
            user=self.context['request'].user
        )


class ReadTransactionSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    category = CategorySerializer()
    user = ReadUserSerializer()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'date',
            'amount',
            'currency',
            'category',
            'description',
            'user'
        ]
        read_only_fields = fields
