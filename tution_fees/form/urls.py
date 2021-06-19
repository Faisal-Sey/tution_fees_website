from django.conf.urls.static import static
from . import views
from .views import FormPage
from django.urls import path

urlpatterns = [
    path('', views.login_page, name="login"),
    path('apply', FormPage.as_view(), name='form_page'),
    path('pay_form', views.pay_form, name='pay_form'),
]