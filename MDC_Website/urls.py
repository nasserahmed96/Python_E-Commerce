from django.conf.urls import url
from . import views

app_name = 'MDC_Website'
urlpatterns = [
        url(r'^$|^/$', views.index, name = 'index'),
        url(r'register$', views.register, name = 'register'),
        url(r'login$', views.login, name = 'login'),
        url(r'showProducts', views.showProducts, name='showProducts'),
        url(r'viewProduct/(?P<product_id>[\w]+)', views.viewProduct, name='viewProduct'),
        url(r'logout$', views.logout, name = 'logout'),
        url(r'account', views.account, name = 'account'),
        ]
