from django.http import HttpResponse


from django.db.models import Q

from django.template import loader

from .models import Property, Contract, Person

import django.utils.timezone as timezone

from .forms import PropertyForm, PersonForm

from json import dumps

"""Defining seconds constants"""
HOUR_SECONDS = 3600
DAY_SECONDS = 86400
MONTH_SECONDS = 2629743.83
YEAR_SECONDS = 31556926



def filter_property(status):
    if not status in ['A', 'I']:
        raise Exception("Property status can be only 'A' or 'I' values")


    available_properties = Property.objects.filter(contract__contract_status=status).distinct()

    items = []

    for property in available_properties:
        current_contract = Contract.objects.filter(Q(property=property) &
                                                   Q(start_time__lte=timezone.now()) &
                                                   Q(end_time__gte=timezone.now()) &
                                                   Q(contract_status=status))

        if len(current_contract) > 0:
            current_contract = current_contract[0]
        else:
            continue

        if current_contract.rate_type == 'H':
            divide_value = HOUR_SECONDS
        elif current_contract.rate_type == 'D':
            divide_value = DAY_SECONDS
        elif current_contract.rate_type == 'M':
            divide_value = MONTH_SECONDS
        elif current_contract.rate_type == 'Y':
            divide_value = YEAR_SECONDS

        elapsed_time = (timezone.now() - current_contract.start_time).total_seconds() / divide_value

        over_under_payment = round(float(current_contract.paid) - elapsed_time * float(current_contract.rate_payment),
                                   2)

        item = {'property': property}

        if over_under_payment >= 0:
            item['overpayment'] = over_under_payment
        else:
            item['underpayment'] = abs(over_under_payment)

        if (current_contract.end_time - timezone.now()).total_seconds() <= MONTH_SECONDS:
            item['expiring'] = True

        items.append(item)

    context = {'properties': items}

    return context



def index_available(request):
    template = loader.get_template('rent_app/index.html')
    context = filter_property('I')

    context['available'] = True

    return HttpResponse(template.render(context, request))

def index_unavailable(request):
    template = loader.get_template('rent_app/index.html')
    context = filter_property('A')

    context['unavailable'] = True

    return HttpResponse(template.render(context, request))


def property_form(request):
    template = loader.get_template('rent_app/add.html')
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            address = form.cleaned_data['address']
            property_type = form.cleaned_data['property_type']
            owner = form.cleaned_data['owner']

        p = Property(name=name, description=description, address=address,
                     property_type=property_type, owner=owner)
        p.clean()
        p.save()

        context = {'form':form, 'property':True, 'saved':True}

        return HttpResponse(template.render(context, ))
    else:
        form = PropertyForm()
        context = {'form': form, 'property':True}
        return HttpResponse(template.render(context, request))

def person_form(request):
    template = loader.get_template('rent_app/add.html')
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            surname_field = form.cleaned_data['surname']
            name_field = form.cleaned_data['name']
            middle_name_field = form.cleaned_data['middle_name']
            phone_number_field = form.cleaned_data['phone_number']
            email_field = form.cleaned_data['email']

            p = Person(surname=surname_field, name=name_field, middle_name=middle_name_field,
                         phone_number=phone_number_field, email=email_field)
            p.clean()
            p.save()

            context = {'form': form, 'person': True, 'saved': True}

            return HttpResponse(template.render(context, request))
        else:
            form.clean()

            context = {'form': form, 'person': True}
            return HttpResponse(template.render(context, request))
    else:
        form = PersonForm()
        context = {'form': form, 'person':True}
        return HttpResponse(template.render(context, request))

def get_json(request):
    items = Property.objects.all()

    dicts = [p.to_dict() for p in items]
    return HttpResponse(dumps({"Propery_items": dicts}), content_type='application/json')





