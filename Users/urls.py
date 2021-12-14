from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (UserTreeView, LoginView, ProfileView, SaleView, SaleDetailView,
                    DebitView, CreditView, BalanceTransferView, SaleApi, DebitApi, CreditApi, BalanceTransferApi,
                    UserRecordView, ReceivedSaleView, ChangePIDAPI, SaleAccept, ReceiveBalanceView, BalanceAccept,
                    CompanyProfile, CreateCategory, AddCategory, DeleteCategory, AddSubCategory, DeleteSubCategory,
                    SubCategoryList, EmployeeListView, EmployeeList, EmployeeEditView, RemoveCategoryFromUser,
                    AddCategoryToUser, ChangePosition, CompanySaleList, SaleReport, DebitReport, CreditReport)
urlpatterns = [
    path('tree', login_required(UserTreeView.as_view())),
    path('login/', LoginView.as_view()),
    path('profile', login_required(ProfileView.as_view())),
    path('balance_transfer', login_required(BalanceTransferView.as_view())),
    path('sale/detail', login_required(SaleDetailView.as_view())),
    path('create', login_required(UserRecordView)),
    path('received/sale', login_required(ReceivedSaleView.as_view())),
    path('received/balance', login_required(ReceiveBalanceView.as_view())),
    path('company', login_required(CompanyProfile.as_view())),
    path('category', login_required(CreateCategory.as_view())),
    path('sale_report', login_required(SaleReport.as_view())),
    path('debit_report', login_required(DebitReport.as_view())),
    path('credit_report', login_required(CreditReport.as_view())),

    #Dinamic part
    path('sale', login_required(SaleView.as_view())),
    path('debit', login_required(DebitView.as_view())),
    path('credit', login_required(CreditView.as_view())),
    path('emplyee', login_required(EmployeeListView.as_view())),
    path('emplyee/edit', login_required(EmployeeEditView.as_view())),

    #API
    path('api/sale', login_required(SaleApi.as_view())),
    path('api/debit', login_required(DebitApi.as_view())),
    path('api/credit', login_required(CreditApi.as_view())),
    path('api/balance', login_required(BalanceTransferApi.as_view())),
    path('api/change_pid', login_required(ChangePIDAPI.as_view())),
    path('api/accept_sale', login_required(SaleAccept.as_view())),
    path('api/accept_balance', login_required(BalanceAccept.as_view())),
    path('api/add_category', login_required(AddCategory.as_view())),
    path('api/delete_category', login_required(DeleteCategory.as_view())),
    path('api/add_sub_category', login_required(AddSubCategory.as_view())),
    path('api/delete_sub_category', login_required(DeleteSubCategory.as_view())),
    path('api/sub_categorys', login_required(SubCategoryList.as_view())),
    path('api/remove_sub_categorys', login_required(RemoveCategoryFromUser.as_view())),
    path('api/add_sub_categorys', login_required(AddCategoryToUser.as_view())),
    path('api/employee', login_required(EmployeeList.as_view())),
    path('api/employee/change_position', login_required(ChangePosition.as_view())),
    path('api/company/sale', login_required(CompanySaleList.as_view())),
]
