from django.contrib.admin import AdminSite
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _



"""============================CUSTOMIZING ADMIN SITE========================="""
class RentSiteAdmin(AdminSite):
    site_title = _('Rent admin')
    site_header = _('Rent admin site')
    index_title = _('Rent admin')

    index_template = "admin/index.html"

    app_index_template = "admin/app_index.html"


rent_site_admin = RentSiteAdmin()


"""================Defining admin models configurations======================="""

class PersonAmdin(admin.ModelAdmin):
    search_fields = ('surname', 'name', 'middle_name', 'email', 'phone_number')
    list_display = ('surname', 'name', 'middle_name')



class PropertyAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description', 'address', 'property_type', 'owner__name')
    list_display = ('name', 'property_type')




class ContractAdmin(admin.ModelAdmin):
    list_filter = ('rate_type', 'contract_status')
    search_fields = ('rate_type', 'rate_payment', 'start_time', 'end_time',
                     'property__name', 'renter__name')

    readonly_fields = ('paid',)

    list_display = ('id', 'property', 'renter', 'start_time', 'end_time', 'paid')




class PaymentAdmin(admin.ModelAdmin):
    search_fields = ('amount', 'contract__renter__name', 'payment_time')
    list_display = ('id', 'amount', 'payment_time')

    readonly_fields = ('payment_time',)



from rent_app import models

"""Register models configurations in Django admin"""

rent_site_admin.register(models.Person, PersonAmdin)
rent_site_admin.register(models.Property, PropertyAdmin)
rent_site_admin.register(models.Contract, ContractAdmin)
rent_site_admin.register(models.Payment, PaymentAdmin)





