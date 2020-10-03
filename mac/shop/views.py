from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Product,Contact,Order,OrderUpdate
from math import ceil
import json
from django.shortcuts import redirect
# Create your views here.
def index(request):

    catprods=Product.objects.values('category','id')
    cats={item["category"] for item in catprods}
    allProds=[]
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod,range(1,nslides),nslides])

    params={'allProds':allProds}
    return render(request,"shop/index.html",params)
def about(request):
    return render(request,"shop/about.html")
def contact(request):
    if request.method=='POST':
        print(request)
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact= Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
    return render(request, "shop/contact.html")
def tracker(request):
    print(request.method)
    if request.method=="POST":
     orderId=request.POST.get('orderId','')
     email=request.POST.get('email','')
     print(orderId,email)
     try:
         print(Order)
         order=Order.objects.filter(order_id=orderId,email=email)
         print("!",order)
         if (len(order)>0):

             update=OrderUpdate.objects.filter(order_id=orderId)
             updates=[]
             for item in update:
                 updates.append({'text':item.update_desc,'time':item.timestamp})
             print("yes",updates)    
             response=json.dumps({"status":"success","updates":updates,"itemsjson":order[0].item_json},default=str)
             return HttpResponse(response)
         else:
             return HttpResponse('{"status":"no item"}')
     except Exception as e:
         return HttpResponse('{"status":"Error"}')
    return render(request, "shop/tracker.html")


def prodView(request,myid):
    product = Product.objects.filter(id=myid)
    print(product)
    params={"product":product[0]}
    return render(request, "shop/prodView.html" ,params)
def searchquery(query,item):
    query=query.lower()

    print(query)
    if query in item.product_name.lower() or query in item.category.lower() or query in item.sub_category.lower() or query in item.desc.lower():
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search','')
    catprods = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catprods}
    allProds = []
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchquery(query,item)]
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!=0:
            allProds.append([prod, range(1, nslides), nslides])

    params = {'allProds': allProds}
    return render(request, "shop/index.html",params)
def checkout(request):
    print(request.method)
    if request.method == 'POST':
        items_json=request.POST.get('itemsJson','')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '')+" "+request.POST.get('address2', '')

        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        order = Order(item_json=items_json,name=name, email=email, phone=phone, address=address,city=city,state=state,zip_code=zip_code)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="Order has been Placed")
        update.save()
        id=order.order_id
        thank=True
        print(items_json)
        return render(request, "shop/checkout.html", {'thank': thank , 'id' : id  })
    return render(request,"shop/checkout.html")


def buy(request,myid):
    product = Product.objects.filter(id=myid)
    print(product)
    params={"product":product[0]}
    if request.method == 'POST':
        items_json=request.POST.get('itemsJson','')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '')+" "+request.POST.get('address2', '')

        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        order = Order(item_json=items_json,name=name, email=email, phone=phone, address=address,city=city,state=state,zip_code=zip_code)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="Order has been Placed")
        update.save()
        id=order.order_id
        thank=True
        return render(request, "shop/buy.html", {'thank': thank , 'id' : id  })
    return render(request, "shop/buy.html" ,params)



def handlelogin(request):
    if request.method=='POST':
        username=request.POST['Username']
        password=request.POST['passwordlogin']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Succesfully')
            account=True
            return render(request, "shop/index.html",{"account":account})
        else:
            account=False
            return render(request,"shop/login.html",{"account":account})
    account=True        
    return render(request,"shop/login.html",{"account":account})

def handlesignup(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        phone=request.POST['phone']
        email=request.POST['email']
        password=request.POST['password']
        myuser=User.objects.create_user(username,email,password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.phone=phone
        myuser.save()
        messages.success(request,"Account Created")
        success=True
        return render(request,"shop/index.html",{"Account":success})
    return render(request,"shop/signup.html")




def handlelogout(request):
    if request.method=='POST':
        logout(request)
        logoutt=True
        return render(request,"shop/login.html",{"logout":logoutt});

    return Httpresponse("404 NOT FOUND")    
