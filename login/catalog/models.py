from django.db import models

class User(models.Model):
    """Model representing an user."""
    user_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    account = models.CharField(null=True, blank=True, max_length=10)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    bank_account = models.IntegerField(null=True, blank=True)
    bank_no = models.IntegerField(null=True, blank=True)
    
    USER_STATUS = (
        (1, 'Teacher'),
        (2, 'Student/Parents'),
    )

    status = models.IntegerField(
        choices=USER_STATUS,
    )

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.user_id}, {self.account}'
    
class Payment(models.Model):
    trade_no = models.CharField(max_length=100,primary_key=True)
    trade_amt = models.IntegerField(null=True, blank=True)
    trade_status =  models.CharField(max_length=100)
    trade_time = models.CharField(max_length=100,default='no record')
    CheckMacValue = models.CharField(max_length=300)
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.trade_no}'

class Class(models.Model):
    """Model representing an user."""
    class_id = models.IntegerField(primary_key=True, unique=True)
    class_serial = models.CharField(null=True, blank=True, max_length=10)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_class')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_class')
    
    SUBJECTS = (
        ('mth', 'Math'),
        ('chn', 'Chinese'),
        ('eng', 'English'),
        ('geo', 'Geography'),
        ('his', 'History'),
        ('cvc', 'Civics'),
        ('scl', 'Social'),
        ('es', 'Earth Science'),
        ('phy', 'Physics'),
        ('chem', 'Chemistry'),
        ('bio', 'Biography'),
        ('pnc', 'PhyChem'),
        ('prg', 'Programming'),
        ('art', 'Art'),
        ('oth', 'Others'),
    )
    subject = models.CharField(
        max_length=10,
        choices=SUBJECTS,
        blank=True,
        default='oth',
    )
    pay_per_class = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    pay_or_not = models.BooleanField(default = False)
    trade_no = models.ForeignKey(Payment, null=True, on_delete=models.SET_NULL)
 
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.class_id}, {self.class_serial}'

class Class_DayTime(models.Model):
    class_serial = models.ForeignKey(Class, on_delete=models.CASCADE)    
    WEEKDAYS = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )
    class_day = models.IntegerField(choices = WEEKDAYS, null=True)    
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.class_serial}'

class Class_details(models.Model):
    class_detail_id = models.IntegerField(primary_key=True, auto_created=True, unique=True)
    class_serial = models.ForeignKey(Class, on_delete=models.CASCADE)#, related_name='classes')
    class_date = models.DateField(null=True)
    description = models.CharField(max_length=100,null=True, blank=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    finish_or_not = models.BooleanField(default = False)
    fee = models.IntegerField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.class_detail_id}, {self.class_serial}'