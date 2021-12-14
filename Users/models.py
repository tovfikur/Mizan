from django.db import models
from django.contrib.auth.models import User
from django_currentuser.middleware import get_current_user
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

# Create your models here.
POSITION_CHOICE = (
    ("Owner", "Owner"),
    ("Admin", "Admin"),
    ("Employee", "Employee"),
)


def nested_tuple_text(index, x):
    for i in x:
        if i[0] == index:
            return i[1]


class UserRecord(models.Model):
    FirstName = models.CharField(max_length=30, null=True, blank=True)
    LastName = models.CharField(max_length=30, null=True, blank=True)
    EmailAddress = models.EmailField( null=True, blank=True)
    Active = models.BooleanField(default=False)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    pid = models.IntegerField(default=None, null=True, blank=True)
    Address = models.TextField(blank=True, null=True)
    Phone = PhoneNumberField(blank=True, null=True)
    Position = models.SmallIntegerField(choices=POSITION_CHOICE, null=True, blank=True)


class CompanyDetails(models.Model):
    Name = models.CharField(max_length=300, blank=True, null=True)
    Type = models.CharField(max_length=300, blank=True, null=True)


class UserNode(models.Model):
    auth = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    PID = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='PID')
    Company = models.ForeignKey(CompanyDetails, on_delete=models.DO_NOTHING, blank=True, null=True)
    Name = models.CharField(max_length=200, blank=True, null=True)
    Address = models.TextField(null=True, blank=True)
    Phone = PhoneNumberField(blank=True, null=True)
    Position = models.CharField(choices=POSITION_CHOICE, max_length=25, null=True, blank=True)
    CreditCategory = models.ManyToManyField('Users.CreditCategory', blank=True)
    DebitCategory = models.ManyToManyField('Users.DebitCategory', blank=True)

    def __str__(self):
        try:
            return str(self.auth.username) + ' -> ' + str(self.id)
        except:
            return str(self.auth.username)

    def is_admin(self):
        if self.Position == "Admin":
            return True
        return False

    def is_owner(self):
        if self.Position == "Owner":
            return True
        return False

    def is_employee(self):
        if self.Position == "Employee":
            return True
        return False


class Reminder(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    ReminderTime = models.DateTimeField(null=False, blank=False)
    Date = models.DateTimeField(auto_now_add=True)


class Balance(models.Model):
    Time = models.DateTimeField(auto_now_add=True, )
    Amount = models.IntegerField(blank=False, null=False)
    DebitOrCredit = models.BooleanField(choices=((True, 'Credit'), (False, 'Debit')), null=False, blank=False)
    Method = models.SmallIntegerField(choices=((1, 'BKash'), (2, 'Nagad'), (3, 'Bank A/C'), (4, 'Cash')), blank=False,
                                      null=False)
    Note = models.CharField(max_length=200, null=True, blank=True)
    SubCat = models.CharField(max_length=50, null=True, blank=True)
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)

    def __str__(self):
        return str(self.User.username) + ' ' + str(self.Amount) + ' ' + str(self.DebitOrCredit)


class BalanceTransfer(models.Model):
    Receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False,
                                 related_name='Receiver')
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='Sender', default=1)
    Accept = models.BooleanField(default=False)
    Method = models.SmallIntegerField(choices=((1, 'BKash'), (2, 'Nagad'), (3, 'Bank A/C'), (4, 'Cash')), blank=False,
                                      null=False)
    Amount = models.IntegerField(blank=False, null=False)
    Note = models.CharField(max_length=150, blank=True, null=True)
    Date = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(BalanceTransfer, self).__init__(*args, **kwargs)
        self._Accept = self.Accept

    def save(self, *args, **kwargs):
        if not get_current_user().id is self.User.id:
            self.Accept = self._Accept

        self.User = get_current_user()

        Debit.objects.create(
            User=self.User,
            Amount=self.Amount,
            Reason_id=1,
            Method=self.Method,
            Note=self.Note
        )

        Credit.objects.create(
            User=self.Receiver,
            Amount=self.Amount,
            Reason_id=1,
            Method=self.Method,
            Note=self.Note
        )
        return super(BalanceTransfer, self).save(*args, **kwargs)

    def method(self):

        if self.Method is 1:
            return 'BKash'
        elif self.Method is 2:
            return 'Nagad'
        elif self.Method is 3:
            return 'Bank A/C'
        elif self.Method is 4:
            return 'Cash'

    class Meta:
        ordering = ['-id']


class DebitCategory(models.Model):
    Creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='Debit_Creator')
    User = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    Title = models.CharField(max_length=300, null=True, blank=True, default='')
    Show = models.BooleanField(default=True)

    def __str__(self):
        return self.Title

    class Meta:
        ordering = ['-id']


class CreditCategory(models.Model):
    Creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='Credit_Creator')
    User = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    Title = models.CharField(max_length=300, null=True, blank=True, default='')
    Show = models.BooleanField(default=True)

    def __str__(self):
        return self.Title

    class Meta:
        ordering = ['-id']


class DebitSubCategory(models.Model):
    Title = models.CharField(max_length=300, null=True, blank=True, unique=True, default='')
    Category = models.ForeignKey(DebitCategory, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.Title + str(self.id)

    class Meta:
        ordering = ['-id']


class CreditSubCategory(models.Model):
    Title = models.CharField(max_length=300, null=True, blank=True, unique=True, default='')
    Category = models.ForeignKey(CreditCategory, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.Title + str(self.id)

    class Meta:
        ordering = ['-id']


class Credit(models.Model):
    Company = models.ForeignKey(CompanyDetails, on_delete=models.DO_NOTHING, null=True, blank=True)
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False, default=1)
    # Response = models.JSONField(null=True, blank=True)
    Amount = models.IntegerField(blank=False, null=False)
    Reason = models.ForeignKey(CreditSubCategory, on_delete=models.DO_NOTHING, blank=True, null=True)
    Method = models.SmallIntegerField(choices=((1, 'BKash'), (2, 'Nagad'), (3, 'Bank A/C'), (4, 'Cash')), blank=False,
                                      null=False)
    Note = models.TextField(null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.User.username) + ' ' + str(self.Amount) + ' ' + str(self.Date)

    def save(self, *args, **kwargs):
        print(self.Reason)
        Balance.objects.create(
            Amount=int(self.Amount),
            DebitOrCredit=True,
            User=self.User,
            Method=self.Method,
            SubCat=self.Reason.Title,
            Note=self.Note
        )
        return super(Credit, self).save(*args, **kwargs)

    def method_text(self):
        if self.Method == 1:
            return 'BKash'
        elif self.Method == 2:
            return 'Nagad'
        elif self.Method == 3:
            return 'Bank A/C'
        elif self.Method == 4:
            return 'Cash'
        else:
            return 'Undefined'

    class Meta:
        ordering = ['-id']


class Debit(models.Model):
    Company = models.ForeignKey(CompanyDetails, on_delete=models.DO_NOTHING, null=True, blank=True)
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    # Response = models.JSONField(null=True, blank=True)
    Amount = models.IntegerField(blank=False, null=False)
    Method = models.SmallIntegerField(choices=((1, 'BKash'), (2, 'Nagad'), (3, 'Bank A/C'), (4, 'Cash')), blank=False,
                                      null=False)
    Note = models.TextField(null=True, blank=True)
    Reason = models.ForeignKey(DebitSubCategory, on_delete=models.DO_NOTHING, blank=False, null=False)
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.User.username) + ' ' + str(self.Amount) + ' ' + str(self.Date)

    def save(self, *args, **kwargs):
        Balance.objects.create(
            Amount=int(self.Amount),
            DebitOrCredit=False,
            User=self.User,
            Method=self.Method,
            SubCat=self.Reason.Title,
            Note=self.Note
        )
        return super(Debit, self).save(*args, **kwargs)

    def method_text(self):
        if self.Method == 1:
            return 'BKash'
        elif self.Method == 2:
            return 'Nagad'
        elif self.Method == 3:
            return 'Bank A/C'
        elif self.Method == 4:
            return 'Cash'
        else:
            return 'Undefined'
    class Meta:
        ordering = ['-id']


class SaleDetails(models.Model):
    Company = models.ForeignKey(CompanyDetails, on_delete=models.DO_NOTHING, blank=True, null=True)
    Receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False, default=1,
                                 related_name='preReceiver')
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    Amount = models.IntegerField(blank=False, null=False, default=0)
    Sender = PhoneNumberField(max_length=100, null=True, blank=True, help_text='You must add +88 for operations')
    TrxID = models.CharField(max_length=156, null=False, blank=False,
                             default='Type Transaction id for your transaction')
    ModeOfPayment = models.SmallIntegerField(choices=((1, 'BKash'), (2, 'Nagad'), (3, 'Bank A/C'), (4, 'Cash')),
                                             null=False, blank=False, default=1)

    SalesID = models.CharField(max_length=150, null=True, blank=True)
    Note = models.CharField(max_length=200, null=True, blank=True)
    Accept = models.BooleanField(default=False)
    _init_Accept = models.BooleanField(default=False)
    _init_delete = models.BooleanField(default=False)
    Date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        Credit.objects.create(
            Company=self.Company,
            User=self.Receiver,
            Amount=self.Amount,
            Reason_id=1,
            Method=self.ModeOfPayment,
            Note='sale' + str(self.Note)
        )
        return super().save(*args, **kwargs)

    def mop(self):
        return nested_tuple_text(self.ModeOfPayment, ((1, 'BKash'), (2, 'Nagad'), (3, 'Bank A/C'), (4, 'Cash')))


class SaleTransfer(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    Receiver = models.ForeignKey('Users.UserNode', on_delete=models.DO_NOTHING, null=False, blank=False, default=1)
    Sale = models.ForeignKey(SaleDetails, on_delete=models.DO_NOTHING, blank=True, null=True)
    Date = models.DateTimeField(auto_now_add=True)


class PreOrderList(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    BuyerName = models.CharField(max_length=150, blank=True, null=True)
    BuyerPhone = PhoneNumberField(max_length=100, null=False, blank=False, help_text='You must add +88 for operations')
    ProductNote = models.TextField(help_text='Use code for product for better search result')
    Amount = models.IntegerField(null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True)


class DueList(models.Model):
    BuyerName = models.CharField(max_length=150, blank=True, null=True)
    BuyerPhone = PhoneNumberField(max_length=100, null=False, blank=False, help_text='You must add +88 for operations')
    ProductNote = models.TextField(help_text='Use code for product for better search result')
    Amount = models.IntegerField(null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)


class TransactionDetails(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    Amount = models.IntegerField(blank=True, null=True)
    ImportantText = models.CharField(blank=True, null=True, max_length=200)
    Note = models.TextField(null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True)


class PermissionTable(models.Model):
    pass
