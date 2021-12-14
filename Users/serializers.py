from .models import SaleDetails, Debit, Credit, BalanceTransfer, DebitSubCategory, CreditSubCategory, UserNode
from rest_framework.serializers import ModelSerializer


class SaleReadSerializer(ModelSerializer):
    class Meta:
        model = SaleDetails
        exclude = [ 'User',  'Accept', 'Company']
        read_only_fields = ('_init_Accept', '_init_delete')
        depth = 2


class SaleCreateSerializer(ModelSerializer):
    class Meta:
        model = SaleDetails
        exclude = [ 'User',  'Accept', 'Company']
        read_only_fields = ('_init_Accept', '_init_delete')


class DebitReadSerializer(ModelSerializer):
    class Meta:
        model = Debit
        fields = '__all__'


class CreditReadSerializer(ModelSerializer):
    class Meta:
        model = Credit
        fields = '__all__'


class BalanceTransferCreateSerializer(ModelSerializer):
    class Meta:
        model = BalanceTransfer
        fields = '__all__'


class BalanceTransferReadSerializer(ModelSerializer):
    class Meta:
        model = BalanceTransfer
        fields = '__all__'
        depth = 2


class SubCategoryListSerializer(ModelSerializer):
    class Meta:
        model = CreditSubCategory
        fields = '__all__'


class UserNodeSerializer(ModelSerializer):
    class Meta:
        model = UserNode
        fields = '__all__'

