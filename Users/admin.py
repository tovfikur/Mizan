from django.contrib import admin
from .models import UserNode, SaleDetails, \
    CompanyDetails, DebitSubCategory, DebitCategory, Balance, \
    CreditSubCategory, CreditCategory, Credit, Debit, BalanceTransfer, UserRecord
# Register your models here.

admin.site.register(UserNode)
admin.site.register(SaleDetails)
admin.site.register(CompanyDetails)
admin.site.register(DebitSubCategory)
admin.site.register(CreditSubCategory)
admin.site.register(DebitCategory)
admin.site.register(CreditCategory)
admin.site.register(Balance)
admin.site.register(BalanceTransfer)
admin.site.register(Credit)
admin.site.register(Debit)
admin.site.register(UserRecord)
