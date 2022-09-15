from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from wishlist.models import ItemWishlist

# Create your views here.
def show_wishlist(request):
    data_wishlist_item = ItemWishlist.objects.all()
    context = {
        'list_item': data_wishlist_item,
        'name': 'Swas'
    }
    return render(request, "wishlist.html", context)

def show_xml(request):
    data = ItemWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = ItemWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = ItemWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
    
def show_json_by_id(request, id):
    data = ItemWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")