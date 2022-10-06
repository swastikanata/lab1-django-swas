import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from wishlist.models import ItemWishlist

# Create your views here.
@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_wishlist_item = ItemWishlist.objects.all()
    context = {
        'list_item': data_wishlist_item,
        'name': 'Swas',
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "wishlist.html", context)

@login_required(login_url='/wishlist/login/')
def show_wishlist_ajax(request):
    return render(request, "wishlist_ajax.html")

@login_required(login_url='/wishlist/login/')
def create_wishlist_ajax(request):
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        item_price = request.POST.get("item_price")
        description = request.POST.get("description")
        ItemWishlist.objects.create(item_name=item_name, item_price=item_price, description=description)
        return HttpResponse()
       
    else:
        return redirect("wishlist:show_wishlist_ajax'")

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

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully created!")
            print("masuk pak eko")
            return redirect("wishlist:login")
    
    context = {"form":form}
    return render(request, "register.html", context)

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, "Wrong Username or Password!")
    
    context = {}
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    response.delete_cookie('last_login')
    return response
