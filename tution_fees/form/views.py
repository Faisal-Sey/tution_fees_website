from django.shortcuts import render, redirect
from .forms import DetailsForm, LoginForm
from .models import Detail
from random import SystemRandom
from django.views.generic import View
from string import ascii_lowercase
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


class FormPage(View):
    def get(self, *args, **kwargs):
        form = DetailsForm()
        context = {"form": form}
        return render(self.request, "admission_form.html", context)

    def post(self, *args, **kwargs):
        Surname = self.request.POST.get("Surname")
        First_name = self.request.POST.get("First_name")
        Middle_name = self.request.POST.get("Middle_name")
        DOB = self.request.POST.get("DOB")
        Number = self.request.POST.get("Number")
        Email = self.request.POST.get("Email")
        print(Surname)

        r = SystemRandom()
        numbers = r.randint(100, 999)
        letter_0 = First_name[0]
        total = len(Surname)
        letters = r.sample(Surname, total-1)
        username = letter_0 + ''.join(letters) + str(numbers)

        l_letters = list(ascii_lowercase)
        key_2 = r.sample(l_letters, 6)
        first = r.randint(0, 9)
        second = r.randint(0, 9)
        result = [key_2[1], key_2[0], str(first), str(second), key_2[2], key_2[3], key_2[4], key_2[5]]
        result = r.sample(result, 8)
        password = ''.join(result)

        current = Detail(
            Surname=Surname,
            Middle_name=Middle_name,
            First_name=First_name,
            DOB=DOB,
            Number=Number,
            Email=Email,
            username=username,
            password=password
        )
        current.save()
        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect('login')


def login_page(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        login(request, user)

        client = Detail.objects.get(username=request.user.username)
        if client.Amount_paid is None:
            return redirect("pay_form")
        else:
            return redirect('form_page')

    context = {"form": form}
    return render(request, "login_admin.html", context)


def pay_form(request):
    details = Detail.objects.get(username=request.user.username)
    email = details.Email
    number = details.Number
    context = {
        'email': email,
        'number': number
    }
    return render(request, "pay_form.html", context)