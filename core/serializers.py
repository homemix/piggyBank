from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Currency, Category, Transaction
from .reports import ReportParams


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


class ReportEntrySerializer(serializers.Serializer):
    category = CategorySerializer()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ReportParamsSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return ReportParams(**validated_data)
