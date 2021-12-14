from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, GenericAPIView, ListAPIView
from django_currentuser.middleware import get_current_user
from .models import UserNode, SaleDetails, DebitSubCategory, DebitCategory, CreditCategory, CreditSubCategory, Debit, \
    Credit, BalanceTransfer, Balance
from .serializers import SaleCreateSerializer, SaleReadSerializer, DebitReadSerializer, CreditReadSerializer, \
    BalanceTransferCreateSerializer, BalanceTransferReadSerializer, SubCategoryListSerializer, UserNodeSerializer

from .forms import UserRecordForm


# Create your views here.

def dash_context(self, context, **kwargs):
    try:
        if self.request.user.id in find_parent(self.request.GET.get('id')):
            context['profile'] = UserNode.objects.get(auth_id=self.request.GET.get('id'))
            context['profile_auth'] = UserNode.objects.get(auth_id=self.request.GET.get('id')).auth
    except:
        context['profile'] = UserNode.objects.get(auth_id=self.request.user.id)
        context['profile_auth'] = self.request.user
    return context


def find_child(objid, ary=None) -> list:
    if ary is None:
        ary = []
    for i in UserNode.objects.filter(PID_id=objid):
        ary.append(i)
        find_child(i.auth.id, ary)
    return ary


def find_parent(Pobj, temp=None):
    if temp is None:
        temp = []
    obj = UserNode.objects.get(auth_id=Pobj)
    if Pobj not in temp:
        temp.append(Pobj)
    if obj.PID:
        temp.append(obj.PID.id)
        find_parent(obj.PID.id, temp)
    return temp


class SaleDetailView(TemplateView):
    template_name = 'sale_details.html'

    def get_context_data(self, **kwargs):
        context = super(SaleDetailView, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        obj = SaleDetails.objects.get(id=self.request.GET.get('d'))
        user_obj = SaleDetails.objects.filter(User=get_current_user())
        pr = 0
        c = 0
        po = 0
        bool = 0
        for i in user_obj:
            if bool:
                po = i.id
                break
            else:
                pr = c
                c = i.id
            if i.id == obj.id:
                bool = 1
        try:
            prev = SaleDetails.objects.get(id=pr)
        except:
            prev = None
        try:
            post = SaleDetails.objects.get(id=po)
        except:
            post = None
        context['sale'] = obj
        context['sale_prev'] = prev
        context['sale_post'] = post
        return context


class UserTreeView(TemplateView):
    template_name = 'TreeView.html'

    def get_context_data(self, **kwargs):
        context = super(UserTreeView, self).get_context_data(**kwargs)
        user_list = []
        user_object_list = find_child(self.request.user.id, [])
        for i in user_object_list:
            if not i.PID:
                i.PID.id = 0
            if not i.Position:
                i.Position = 'Empty'
            try:
                user_list.append({
                    'id': i.auth.id,
                    'pid': i.PID.id,
                    'name': str(i.auth.username),
                    'txt': '<a href= "/user/profile?id=' + str(i.auth.id) + '">' + str(i.auth.id) + '</a><br>' + str(
                        i.Position) + '<br>change PID:<input auth="' + str(
                        i.auth.id) + '" class="tree_pid" type="text" value="' + str(i.PID.id) + '">',
                    'img': "http://cdn.onlinewebfonts.com/svg/img_84627.png"
                })
            except Exception as e:
                user_list.append({
                    'id': i.auth.id,
                    'pid': 0,
                    'name': str(i.auth.username),
                    'txt': '<a href= "/user/profile?id=' + str(i.auth.id) + '">' + str(i.auth.id) + '</a><br>' + str(
                        i.Position) + '<br>PID:<input auth="' + str(
                        i.auth.id) + '" class="tree_pid" type="text" value="' + str(i.PID.id) + '">',
                    'img': "http://cdn.onlinewebfonts.com/svg/img_84627.png"
                })
        temp_obj = UserNode.objects.get(auth=self.request.user)
        if not temp_obj.Position:
            temp_obj.Position = 'Empty'
        temp_json = {
            'id': temp_obj.auth.id,
            'pid': 0,
            'name': str(temp_obj.auth.username),
            'text': str(temp_obj.Position),
            'img': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDkDbYsRFwYbcu2pe1QrQtf74PvXWwXL_Kkg&usqp=CAU"
        }
        user_list.insert(0, temp_json)
        context['tree'] = user_list
        return context


class LoginView(TemplateView):
    template_name = 'login.html'


class ProfileView(TemplateView):
    template_name = 'dash.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        user = None
        if self.request.GET.get('id'):
            user = UserNode.objects.get(id=self.request.GET.get('id')).auth
        else:
            user = get_current_user()

        # Sale context part
        sale = SaleDetails.objects.filter(User=user)
        total_sale = sale.count()
        total_income = 0
        last_sale_time = None
        first_sale_time = None
        brk = True
        for i in sale:
            if brk:
                first_sale_time = i.Date
                brk = False
            total_income += i.Amount
            last_sale_time = i.Date
        context['total_sale'] = total_sale
        context['last_sale_time'] = last_sale_time
        context['first_sale_time'] = first_sale_time

        # Balance/Cost Context part
        balance = Balance.objects.filter(User=user)
        total_balance = 0
        total_credit = 0
        total_debit = 0
        total_entry = 0
        credit_last_entry = None
        debit_last_entry = None
        for i in balance:
            if i.DebitOrCredit:
                total_balance += i.Amount
                total_credit += i.Amount
                credit_last_entry = i.Time
            else:
                total_balance -= i.Amount
                total_debit += i.Amount
                debit_last_entry = i.Time
            total_entry += 1
        context['total_balance'] = total_balance
        context['total_credit'] = total_credit
        context['total_debit'] = total_debit
        context['total_entry'] = total_entry
        context['credit_last_entry'] = credit_last_entry
        context['debit_last_entry'] = debit_last_entry

        return context


class SaleView(TemplateView):
    template_name = 'Sale.html'

    def get_context_data(self, **kwargs):
        context = super(SaleView, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        return context


class DebitView(TemplateView):
    template_name = 'debit.html'

    def get_context_data(self, **kwargs):
        context = super(DebitView, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        try:
            if self.request.user.id in find_parent(self.request.GET.get('id')):
                context['list'] = Debit.objects.filter(User_id=self.request.GET.get('id'))
                temp = DebitSubCategory.objects.filter(id=0)
                for i in UserNode.objects.get(auth=self.request.user).DebitCategory.all():
                    temp = temp | DebitSubCategory.objects.filter(Category=i)
                context['category'] = temp
        except:
            context['list'] = Debit.objects.filter(User=get_current_user())
            temp = DebitSubCategory.objects.filter(id=0)
            for i in UserNode.objects.get(auth=self.request.user).DebitCategory.all():
                temp = temp | DebitSubCategory.objects.filter(Category=i)
            context['category'] = temp
        return context


class CreditView(TemplateView):
    template_name = 'credit.html'

    def get_context_data(self, **kwargs):
        context = super(CreditView, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        try:
            if self.request.user.id in find_parent(self.request.GET.get('id')):
                context['list'] = Credit.objects.filter(User=self.request.GET.get('id'))
                temp = CreditSubCategory.objects.filter(id=0)
                for i in UserNode.objects.get(auth=self.request.user).CreditCategory.all():
                    temp = temp | CreditSubCategory.objects.filter(Category=i)
                context['category'] = temp
        except:
            context['list'] = Credit.objects.filter(User=get_current_user())
            temp = CreditSubCategory.objects.filter(id=0)
            for i in UserNode.objects.get(auth=self.request.user).CreditCategory.all():
                temp = temp | CreditSubCategory.objects.filter(Category=i)
            context['category'] = temp
        return context


class BalanceTransferView(TemplateView):
    template_name = 'balancetransfer.html'

    def get_context_data(self, **kwargs):
        context = super(BalanceTransferView, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        try:
            if self.request.user.id in find_parent(self.request.GET.get('id')):
                context['list'] = BalanceTransfer.objects.filter(
                    Q(User_id=self.request.GET.get('id'))
                    |
                    Q(Receiver_id=self.request.GET.get('id'))
                )
        except:
            context['list'] = BalanceTransfer.objects.filter(
                Q(User=self.request.user)
                |
                Q(Receiver=self.request.user)
            )
        return context


class ReceivedSaleView(TemplateView):
    template_name = 'received_list_sale.html'

    def get_context_data(self, **kwargs):
        context = super(ReceivedSaleView, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)

        sale = SaleDetails.objects.filter(Receiver_id=get_current_user().id).filter(Accept=False)
        context['sale'] = sale
        return context


class ReceiveBalanceView(TemplateView):
    template_name = 'received_list_balance.html'

    def get_context_data(self, **kwargs):
        context = super(ReceiveBalanceView, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)

        balance = BalanceTransfer.objects.filter(Receiver_id=get_current_user().id).filter(Accept=False)
        context['balance'] = balance
        return context


class CompanyProfile(TemplateView):
    template_name = 'company_profile.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyProfile, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        company = UserNode.objects.get(auth=get_current_user()).Company
        total_balance = 0
        total_employee = 0
        total_debit = 0
        total_credit = 0
        total_transaction = 0
        for i in UserNode.objects.filter(Company=company):
            for temp in Balance.objects.filter(User=i.auth):
                if temp.DebitOrCredit:
                    total_balance += temp.Amount
                    total_credit += temp.Amount
                else:
                    total_balance -= temp.Amount
                    total_debit += temp.Amount
                total_transaction += 1
            total_employee += 1

        context['balance'] = total_balance
        context['cost'] = total_debit
        context['income'] = total_credit
        context['saving'] = total_transaction

        return context


class SaleReport(TemplateView):
    template_name = 'sale_report.html'


    def get_context_data(self, **kwargs):
        context = super(SaleReport, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        company = UserNode.objects.get(auth=get_current_user()).Company
        sales = SaleDetails.objects.filter(Company=company)
        total_balance = 0
        total_employee = 0
        total_debit = 0
        total_credit = 0
        total_transaction = 0
        for i in UserNode.objects.filter(Company=company):
            for temp in Balance.objects.filter(User=i.auth):
                if temp.DebitOrCredit:
                    total_balance += temp.Amount
                    total_credit += temp.Amount
                else:
                    total_balance -= temp.Amount
                    total_debit += temp.Amount
                total_transaction += 1
            total_employee += 1

        context['balance'] = total_balance
        context['cost'] = total_debit
        context['income'] = total_credit
        context['saving'] = total_transaction
        context['sales'] = sales

        return context


class DebitReport(TemplateView):
    template_name = 'debit_report.html'

    def get_context_data(self, **kwargs):
        context = super(DebitReport, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        company = UserNode.objects.get(auth=get_current_user()).Company
        debit = Debit.objects.filter(Company=company)
        total_balance = 0
        total_employee = 0
        total_debit = 0
        total_credit = 0
        total_transaction = 0
        for i in UserNode.objects.filter(Company=company):
            for temp in Balance.objects.filter(User=i.auth):
                if temp.DebitOrCredit:
                    total_balance += temp.Amount
                    total_credit += temp.Amount
                else:
                    total_balance -= temp.Amount
                    total_debit += temp.Amount
                total_transaction += 1
            total_employee += 1

        context['balance'] = total_balance
        context['cost'] = total_debit
        context['income'] = total_credit
        context['saving'] = total_transaction
        context['debit'] = debit

        return context



class CreditReport(TemplateView):
    template_name = 'credit_report.html'

    def get_context_data(self, **kwargs):
        context = super(CreditReport, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        company = UserNode.objects.get(auth=get_current_user()).Company
        debit = Credit.objects.filter(Company=company)
        print(debit)
        total_balance = 0
        total_employee = 0
        total_debit = 0
        total_credit = 0
        total_transaction = 0
        for i in UserNode.objects.filter(Company=company):
            for temp in Balance.objects.filter(User=i.auth):
                if temp.DebitOrCredit:
                    total_balance += temp.Amount
                    total_credit += temp.Amount
                else:
                    total_balance -= temp.Amount
                    total_debit += temp.Amount
                total_transaction += 1
            total_employee += 1

        context['balance'] = total_balance
        context['cost'] = total_debit
        context['income'] = total_credit
        context['saving'] = total_transaction
        context['debit'] = debit

        return context



class BalanceTransferReport(TemplateView):
    template_name = 'balance_transfer_report.html'



class CreateCategory(TemplateView):
    template_name = 'd_c_category.html'

    def get_context_data(self, **kwargs):
        context = super(CreateCategory, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        context['credit'] = CreditCategory.objects.filter(Creator=get_current_user())
        context['debit'] = DebitCategory.objects.filter(Creator=get_current_user())
        return context


class EmployeeListView(TemplateView):
    template_name = 'emplyee.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)
        context['employee'] = UserNode.objects.filter(Company=UserNode.objects.get(auth=get_current_user()).Company)
        return context


class EmployeeEditView(TemplateView):
    template_name = 'employeedit.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeEditView, self).get_context_data(**kwargs)
        context = dash_context(self, context, **kwargs)

        context['credit_list'] = UserNode.objects.get(auth_id=self.request.GET.get('eid')).CreditCategory.all()
        context['debit_list'] = UserNode.objects.get(auth_id=self.request.GET.get('eid')).DebitCategory.all()

        context['credit_all'] = CreditCategory.objects.filter(Creator=get_current_user())
        context['debit_all'] = DebitCategory.objects.filter(Creator=get_current_user())

        context['employee'] = UserNode.objects.get(auth_id=self.request.GET.get('eid'))
        return context


def UserRecordView(request):
    if request.method == "POST":
        rqst = request.POST
        username = rqst.get('username')
        password = rqst.get('password')
        name = rqst.get('first_name') + ' ' + rqst.get('last_name')
        pid = rqst.get('pid')
        position = rqst.get('position')
        email = rqst.get('email')
        phone = rqst.get('phone')
        accept = rqst.get('accept')
        company = UserNode.objects.get(auth=get_current_user()).Company
        user_obj = User.objects.create_user(username=username, password=password)

        user_node_obj = UserNode(auth=user_obj, PID_id=pid, Company=company, Name=name, Phone=phone, Position=position)
        user_node_obj.save()
    else:
        pass
    context = {}
    try:
        if request.user.id in find_parent(request.GET.get('id')):
            context['profile'] = UserNode.objects.get(auth_id=request.GET.get('id'))
            context['profile_auth'] = UserNode.objects.get(auth_id=request.GET.get('id')).auth
    except:
        context['profile'] = UserNode.objects.get(auth_id=request.user.id)
        context['profile_auth'] = request.user

    return render(request, 'userrecord.html', context)


### APIs ###
class SaleApi(ListCreateAPIView):
    serializer_class = SaleCreateSerializer
    pagination_class = None

    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT' or method == 'POST':
            return SaleCreateSerializer
        else:
            return SaleReadSerializer

    def get_queryset(self):
        return SaleDetails.objects.filter(User_id=self.request.user.id).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(User=self.request.user, Company=UserNode.objects.get(auth=self.request.user).Company)


class DebitApi(ListCreateAPIView):
    serializer_class = DebitReadSerializer
    pagination_class = None
    queryset = Debit.objects.all()


class CreditApi(ListCreateAPIView):
    serializer_class = CreditReadSerializer
    pagination_class = None
    queryset = Credit.objects.all()


class BalanceTransferApi(ListCreateAPIView):

    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT' or method == 'POST':
            return BalanceTransferCreateSerializer
        else:
            return BalanceTransferReadSerializer

    def get_queryset(self):
        return BalanceTransfer.objects.filter(
            Q(User=self.request.user)
            |
            Q(Receiver=self.request.user)
        )


class ChangePIDAPI(GenericAPIView):
    def get(self, request):
        user = UserNode.objects.get(auth_id=request.GET.get('id'))
        user.PID_id = request.GET.get('pid')
        user.save()
        return Response({'method': 'GET NOT ALLOWED'})


class SaleAccept(GenericAPIView):
    def get(self, request):
        sale = SaleDetails.objects.get(id=request.GET.get('id'))
        sale.Accept = True
        sale.save()
        return Response({'method': 'GET NOT ALLOWED'})


class BalanceAccept(GenericAPIView):
    def get(self, request):
        sale = BalanceTransfer.objects.get(id=request.GET.get('id'))
        sale.Accept = True
        sale.save()
        return Response({'method': 'GET NOT ALLOWED'})


class AddCategory(GenericAPIView):
    def get(self, request):
        if self.request.GET.get('title'):
            if self.request.GET.get('cat'):
                CreditCategory.objects.create(Creator=get_current_user(), User=get_current_user(), Show=True,
                                              Title=self.request.GET.get('title')).save()
            else:
                DebitCategory.objects.create(Creator=get_current_user(), User=get_current_user(), Show=True,
                                             Title=self.request.GET.get('title')).save()
        return Response({'method': 'GET NOT ALLOWED'})


class DeleteCategory(GenericAPIView):

    def get(self, request):
        if self.request.GET.get('cat'):
            CreditCategory.objects.filter(id=self.request.GET.get('id')).delete()
        else:
            DebitCategory.objects.filter(id=self.request.GET.get('id')).delete()
        return Response({'method': 'GET NOT ALLOWED'})


class AddSubCategory(GenericAPIView):

    def get(self, request):
        if self.request.GET.get('cat'):
            CreditSubCategory.objects.create(Category_id=self.request.GET.get('id'),
                                             Title=self.request.GET.get('title')).save()
        else:
            DebitSubCategory.objects.create(Category_id=self.request.GET.get('id'),
                                            Title=self.request.GET.get('title')).save()
        return Response({'method': 'GET NOT ALLOWED'})


class DeleteSubCategory(GenericAPIView):

    def get(self, request):
        if self.request.GET.get('cat'):
            CreditSubCategory.objects.filter(id=self.request.GET.get('id')).delete()
        else:
            DebitSubCategory.objects.filter(id=self.request.GET.get('id')).delete()
        return Response({'method': 'GET NOT ALLOWED'})


class SubCategoryList(ListAPIView):
    serializer_class = SubCategoryListSerializer
    pagination_class = None

    def get_queryset(self):
        if self.request.GET.get('cat'):
            return CreditSubCategory.objects.filter(Category_id=self.request.GET.get('id'))
        else:
            return DebitSubCategory.objects.filter(Category_id=self.request.GET.get('id'))


class EmployeeList(ListAPIView):
    serializer_class = UserNodeSerializer
    pagination_class = None

    def get_queryset(self):
        user = UserNode.objects.filter(Company=UserNode.objects.get(auth=get_current_user()).Company)
        print(user)
        return user


class RemoveCategoryFromUser(GenericAPIView):

    def get(self, request):
        if self.request.GET.get('cat'):
            print(UserNode.objects.get(auth=User.objects.get(id=self.request.GET.get('id'))).CreditCategory)
            UserNode.objects.get(auth=User.objects.get(id=self.request.GET.get('id'))).CreditCategory.remove(
                CreditCategory.objects.get(id=self.request.GET.get('cat_id'))
            )
        else:
            UserNode.objects.get(auth=User.objects.get(id=self.request.GET.get('id'))).DebitCategory.remove(
                DebitCategory.objects.get(id=self.request.GET.get('cat_id'))
            )
        return Response({'method': 'GET NOT ALLOWED'})


class AddCategoryToUser(GenericAPIView):

    def get(self, request):
        if self.request.GET.get('cat'):
            print(UserNode.objects.get(auth=User.objects.get(id=self.request.GET.get('id'))).CreditCategory)
            UserNode.objects.get(auth=User.objects.get(id=self.request.GET.get('id'))).CreditCategory.add(
                CreditCategory.objects.get(id=self.request.GET.get('cat_id'))
            )
        else:
            UserNode.objects.get(auth=User.objects.get(id=self.request.GET.get('id'))).DebitCategory.add(
                DebitCategory.objects.get(id=self.request.GET.get('cat_id'))
            )
        return Response({'method': 'GET NOT ALLOWED'})


class ChangePosition(GenericAPIView):
    def get(self, request):
        obj = UserNode.objects.get(auth_id=self.request.GET.get('id'))
        obj.Position = self.request.GET.get('pos')
        obj.save()
        return Response({'method': 'GET NOT ALLOWED'})


class CompanySaleList(ListAPIView):
    serializer_class = SaleCreateSerializer
    pagination_class = None

    def get_queryset(self):
        company = UserNode.objects.get(auth=get_current_user()).Company
        return SaleDetails.objects.filter(Company=company)
