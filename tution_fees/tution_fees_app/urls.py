from django.urls import path
from . import views
from .views import Otp, email_redirect, payment, StudentListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('panel/', views.panel, name="panel"),
    path('details/', views.details, name="details"),
    path('payment/', payment.as_view(), name="payment"),
    path('details1/', views.details_one, name="details_one"),
    path('redirect/', views.redirect_page, name="redirect"),
    path('transaction/', views.transactions, name="transaction"),
    path('email_redirect/', email_redirect.as_view(), name="email_redirect"),
    path('loader/', views.loader, name="loader"),
    path('otp/', Otp.as_view(), name="otp"),
    path('add/', views.add_student, name="add"),
    path('listview/', StudentListView.as_view(), name="listview"),
    path('detailview/<slug:Slug>/', views.student_detailView, name="detailview")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
