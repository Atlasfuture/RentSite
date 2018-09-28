from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, DecimalValidator
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

import django.utils.timezone as timezone



"""Defining validators"""
letters_validator = RegexValidator(regex='^[a-zA-ZА-Яа-яІіЇїЄє]+$',
                              message=_("Only letters are allowed"))


digits_validator = RegexValidator(regex='^\d+$', message=_("Only digits are allowed"))


phone_num_validator = RegexValidator(regex='^\+?1?\d{9,15}$',
                                        message=_("Only digits and '+' are allowed in phone number"))




class Person(models.Model):
    surname = models.CharField(max_length=35, validators=[letters_validator])
    name = models.CharField(max_length=35, validators=[letters_validator])
    middle_name = models.CharField(max_length=35, validators=[letters_validator])
    phone_number = models.CharField(max_length=15, validators=[phone_num_validator])
    email = models.EmailField()



    def __str__(self):
        return "{} {} {}".format(self.surname, self.name, self.middle_name)




class Property(models.Model):
    """Defining property type choices"""
    RESIDENTIAL = "Res"
    COMMERCIAL = "Comm"

    PROPERTY_TYPE_CHOICES = (
        (RESIDENTIAL, 'Residential'),
        (COMMERCIAL, 'Commercial')
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    property_type = models.CharField(max_length=4,
                                     choices=PROPERTY_TYPE_CHOICES)

    owner = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)


    def to_dict(self):
        """Allow to represent Property data like
        a serializable dictionary for JSON"""
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "address": self.address,
                "property_type": self.property_type}



    def __str__(self):
        return self.name


class Contract(models.Model):
    """Defining contract status choices"""
    ACTIVE = "A"
    INACTIVE = "I"

    CONTRACT_STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive")
    )

    contract_status = models.CharField(max_length=1,
                                       choices=CONTRACT_STATUS_CHOICES)


    """Defining rate type choices"""
    HOUR = "H"
    DAY = "D"
    MONTH = "M"
    YEAR = "Y"

    RATE_TYPE_CHOICES = (
        (HOUR, "Hour"),
        (DAY, "Day"),
        (MONTH, "Month"),
        (YEAR, "Year")
    )

    rate_type = models.CharField(max_length=1,
                                 choices=RATE_TYPE_CHOICES)


    rate_payment = models.DecimalField(max_digits=10, decimal_places=2)

    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)



    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


    property = models.ForeignKey(Property, null=True, on_delete=models.SET_NULL)
    renter = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)


    """Overidding clean for cross table data validation"""
    def clean(self):
        error = {}

        try:
            super(Contract, self).clean_fields()
        except ValidationError as e:
            error = e.error_dict
            print("error {}".format(error))


        if not any(item in error for item in ['start_time', 'end_time']) and \
                        self.start_time >= self.end_time:
                error['end_time'] = ValidationError(_("End contract time must be greater than start time"))

        if not 'renter' in error and self.property.owner == self.renter:
                error['renter'] = ValidationError(_("Landlord cant be renter at the same property"))

        if len(error) > 0:
            raise ValidationError(error)


    def __str__(self):
        return "{}".format(self.id)



class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    payment_time = models.DateTimeField(default = timezone.now)


    def clean(self):
        error = {}

        try:
            super(Payment, self).clean_fields()
        except ValidationError as e:
            error = e.error_dict


        if not any(item in error for item in ['payment_time', 'contract']) and \
                        self.contract.start_time >= self.payment_time:
            error['payment_time'] = ValidationError(_("Payment Stime have to be later than start contract time"))


        if len(error) > 0:
            raise ValidationError(error)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.contract.paid += self.amount
            self.contract.save(update_fields=['paid'])

        super(Payment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)




















