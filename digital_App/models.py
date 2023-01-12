from django.db import models
import datetime

# Create your models here.


gender_choices = (
    ('m', 'Male'),
    ('f', 'Female'),
)

class User(models.Model):
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=12)    

    class Meta:
        db_table = "User"

    def __str__(self) -> str:
        return self.Email

Select_Role = (
    ('M', 'member'),
    ('C', 'chairman'),
)
# Create your models here.
class Role(models.Model):
    # Role_Type = models.CharField(max_length=8,default=str())
    Role_Type = models.CharField(max_length=5, choices=Select_Role, default=str(), blank=True)
     
    class Meta:
        db_table="role"

    def __str__(self) -> str:
        return self.Role_Type


class Visitor(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)

    FullName = models.CharField(max_length=15, default=str(), blank=True)
    Mobile = models.CharField(max_length=10, default=str(), blank=True)
    Birthday = models.DateField(default="2022-11-20")
    
    class Meta:
        db_table = "Visitor"

    def __str__(self) -> str:
        return self.User.Email

class Member(models.Model):
    Visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)

    class Meta:
        db_table = "Member"

    def __str__(self) -> str:
        return self.Visitor.User.Email
        
class Chairman(models.Model):
    Visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    Type = models.CharField(max_length=10, default=str(), blank=True)

    class Meta:
        db_table = "Chairman"

    def __str__(self) -> str:
        return self.Visitor.User.Email


class Event(models.Model):
    
    AddEvent = models.CharField(max_length=50, default=str(), blank=True)    
    Date = models.DateField()

    class Meta:
        db_table = "Event"

    def __str__(self) -> str:
        return self.AddEvent

class Notice(models.Model):
    AddNotices = models.TextField(max_length=150, default=str(), blank=True)
    Date = models.DateField()
    
    class Meta:
        db_table = "Notice"

    def __str__(self) -> str:
        return self.AddNotices

class Notice_view(models.Model):
    Notices = models.ForeignKey(Notice, on_delete=models.CASCADE)
    

    class Meta:
        db_table = "Notice_view"



class Watchman(models.Model):
    
    FullName = models.CharField(max_length=(20), default=str(), blank=True)
    Mobile = models.CharField(max_length=10, default=str(), blank=True)
    

    class Meta:
        db_table = "Watchman"

    def __str__(self) -> str:
        return self.FullName


class Transaction(models.Model):

    
    class Meta:
        db_table = "Transaction"

