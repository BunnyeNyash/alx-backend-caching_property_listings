# from django.shortcuts import render
from django.views.decorators.cache import cache_page
# from .models import Property
from .utils import get_all_properties
from django.http import JsonResponse

# Create your views here.
# @cache_page(60 * 15)  # Cache for 15 minutes
# def property_list(request):
#     properties = Property.objects.all()
#     return render(request, 'properties/property_list.html', {'properties': properties})
@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = get_all_properties()
    # return render(request, 'properties/property_list.html', {'properties': properties})
    data = [
        {
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),  # Convert Decimal to string for JSON
            'location': prop.location,
            'created_at': prop.created_at.isoformat()  # Convert datetime to string
        }
        for prop in properties
    ]
    return JsonResponse({'data': data})
