from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='ShopHome'),
    path("about/",views.about,name='about'),
    path("contact/",views.contact,name='contact'),
    path("search",views.search,name='search'),
    path("tracker",views.tracker,name='tracker'),
    path("products/<int:myid>",views.prodView,name='productview'),
    path("checkout",views.checkout,name='checkout'),
    path("buy/<int:myid>",views.buy,name='buy'),
    path("login",views.handlelogin,name='login'),
    path("signup",views.handlesignup,name='signup'),
    path("logout",views.handlelogout,name='logout')
]

