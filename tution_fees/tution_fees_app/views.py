from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Details, Transaction, StudentList
import requests, json
from random import SystemRandom
from django.utils import timezone
from .decorators import moderator_login_required
from django.views.generic import ListView, View, DetailView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from .forms import DetailsForm, EmailForm, StudentDetailsForm, OtpForm
# Create your views here.

code_resp = {}
def home(request):
    context = {}
    return render(request, 'base.html', context)


def loginPage(request):
    if request.method == 'POST':
        student = request.POST.get('studentid')
        pin = request.POST.get('pin')
        try:
            trans = Details.objects.get(studentid=student)
            try:
                user_det = User.objects.get(username=trans.studentid)
                if trans:
                    if user_det:
                        user1 = authenticate(request, username=student, password=pin)
                        login(request, user1)
                        if trans.email is not None and trans.mobile is not None:
                            return redirect('panel')
                        else:
                            return redirect('email_redirect')
                    else:
                        user = User.objects.create_user(username=student, password=pin)
                        user.save()
                        user1 = authenticate(request, username=student, password=pin)
                        login(request, user1)
                        if trans.email is not None and trans.mobile is not None:
                            return redirect('panel')
                        else:
                            return redirect('email_redirect')
            except:
                if trans:
                    user = User.objects.create_user(username=trans.studentid, password=str(trans.pin))
                    user.save()
                    user1 = authenticate(request, username=trans.studentid, password=str(trans.pin))
                    login(request, user1)
                    if trans.email is not None and trans.mobile is not None:
                        return redirect('panel')
                    else:
                        return redirect('email_redirect')

                else:
                    messages.info(request, 'Email or Password is incorrect')
        except:
            messages.info(request, 'Student ID or pin incorrect')
            return redirect('login')
    context = {}
    return render(request, 'accounts/login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('home')


def transactions(request):

    trans = Transaction.objects.filter(studentid=request.user.username)
    context = {'detail': trans}

    return render(request, "transactions.html", context)



def redirect_page(request):
    data = request.GET
    mod_json = (data.dict())
    print(mod_json)

    reference = mod_json["reference"]

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        'Authorization': "Bearer sk_live_9dc5dbd6e003c9c48b9260b9e6e291ff58f5e8d3"
    }

    req = requests.get(url, headers=headers)
    req_data = json.loads(req.content)
    print(req_data)
    print(req_data["data"]["status"])
    network = req_data["data"]["authorization"]["bank"]
    amount = req_data["data"]["amount"]
    if req_data["data"]["status"] == "success":
        det = Details.objects.get(studentid=request.user.username)
        trans_details = Transaction(
            fullname=det.full_name,
            amount=amount,
            created=timezone.now(),
            studentid=request.user.username,
            network=network,
            mobile=det.mobile,
            reference=reference
        )
        trans_details.save()

        lst = StudentList.objects.get(user=request.user)
        lst.transactions.add(trans_details)
        amount1 = det.amount_paid + int(amount)
        present = Details.objects.filter(studentid=request.user.username)
        if present.exists():
            profile = Details.objects.get(studentid=request.user.username)
            profile.amount_paid = profile.amount_paid + int(amount)
            profile.balance = 2000 - int(amount1)
            profile.save()
            try:
                lst = StudentList.objects.get(user=request.user)
                lst.details = profile
                lst.save()
            except:
                lst = StudentList(
                    user=request.user,
                    details=profile
                )
                lst.save()
            return redirect('panel')


    return render(request, 'redirect.html')


def panel(request):
    try:
        contxt = Details.objects.get(studentid=request.user.username)
        context = {'detail': contxt}
        return render(request, 'Panel.html', context)
    except:
        pass
    return render(request, 'Panel.html')


def details(request):
    form = StudentDetailsForm()
    details = Details.objects.filter(studentid=request.user.username)
    context = {'details': details,'form': form}
    if request.method == 'POST':
        details = Details.objects.filter(studentid=request.user.username)
        context = {'details': details, 'form': form}
        return render(request, 'details1.html', context)
    return render(request, 'details.html', context)


def details_one(request):
    if request.method == 'POST':
        if len(str(request.POST.get('pin'))) == 4:
            if len(str(request.POST.get('studentid'))) == 10:
                if request.POST.get('pin'):
                    user = User.objects.get(username=request.user.username)
                    user.username = request.POST.get('studentid')
                    user.password = request.POST.get('pin')
                    user.save()
                    details = Details.objects.get(studentid=request.user.username)
                    details.pin = request.POST.get('pin')
                    details.save()
                else:
                    user = User.objects.get(username=request.user.username)
                    user.username = request.POST.get('studentid')
                    user.save()
            else:
                messages.success(request, 'Wrong Mobile Number')
                return redirect('details')

        else:
            messages.success(request, 'Wrong Password')
            return redirect('details')

    return render(request, 'details1.html')


class payment(View):
    def get(self, *args, **kwargs):
        form = DetailsForm()
        det = Details.objects.filter(studentid=self.request.user.username)
        context = {'form': form, 'details': det}
        return render(self.request, 'payment.html', context)

    def post(self, *args, **kwargs):
        form = DetailsForm(self.request.POST)
        if form.is_valid():
            print("yes")
            secret_key = 'sk_live_9dc5dbd6e003c9c48b9260b9e6e291ff58f5e8d3'
            url = 'https://api.paystack.co/transaction/initialize'
            req_amount = form.cleaned_data['amount']
            if req_amount >= 50:
                req_email = self.request.POST.get('email')
                amount = int(req_amount) * 100
                email = req_email

                payload = {
                    'amount': f'{amount}',
                    'email': f'{email}',
                    "callback_url": "http://localhost:8000/redirect/"
                }

                payload_json = json.dumps(payload)

                headers = {
                    'Authorization': f'Bearer {secret_key}',
                    "Content-Type": "application/json"
                }
                req = requests.post(url, headers=headers, data=payload_json)

                data = json.loads(req.content)
                print(data)
                redirect_link = json.loads(req.content)["data"]["authorization_url"]
                print(redirect_link)
                html = "<!doctype html><html lang='en'><head>  <meta charset='utf-8'>  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'> <title>Redirect</title>  <link rel='canonical' href='https://getbootstrap.com/docs/4.5/examples/sign-in/'>  <!-- Bootstrap core CSS --><!-- CSS only --><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1' crossorigin='anonymous'><style>  .arrage{ margin-top: 250px; } .bd-placeholder-img {    font-size: 1.125rem;    text-anchor: middle;    -webkit-user-select: none;    -moz-user-select: none;    -ms-user-select: none;    user-select: none;  }  @media (min-width: 768px) {    .bd-placeholder-img-lg {      font-size: 3.5rem;    }  }</style><!-- Custom styles for this template --></head><body class='text-center'><div class='arrage'><h1 class='h3 mb-3 font-weight-normal'>Go to pay</h1>" + f"<a class='btn btn-lg btn-primary btn-block' href={redirect_link}>Continue to validate</a></div></body></html>"
                return HttpResponse(html)

            else:
                messages.info(self.request, 'Amount Should be GHC 50 or more')
                return redirect("payment")



class email_redirect(View):
    def get(self, *args, **kwargs):
        form = EmailForm()
        context = {'form': form}
        return render(self.request, 'email.html', context)

    def post(self, *args, **kwargs):
        form = EmailForm(self.request.POST)
        if form.is_valid():
            cleaned_email = form.cleaned_data["email"]
            cleaned_mobile = form.cleaned_data["phone"]
            data = Details.objects.get(studentid=self.request.user.username)
            data.email = cleaned_email
            data.mobile = cleaned_mobile
            data.save()
            return redirect("otp")



class Otp(View):
    def get(self, *args, **kwargs):
        form = OtpForm()
        randomize = SystemRandom()
        global code
        code = randomize.randint(10000, 99999)
        details = Details.objects.get(studentid=self.request.user.username)
        mobile = details.mobile
        url = f"https://apps.mnotify.net/smsapi?key=P6vcP5SiC2jijtuv2GFiT6h1b&to={mobile}&msg=Your Verification code for tutionfees is {code}&sender_id=PressStory"

        req = requests.post(url)
        global mod_req
        mod_req = json.loads(req.content)
        context = {'form': form}
        return render(self.request, 'otp.html', context)

    def post(self, *args, **kwargs):
        form = OtpForm(self.request.POST)
        if form.is_valid():
            cleaned_otp = form.cleaned_data["code"]
            if mod_req["message"] == "Message submitted successful":
                if cleaned_otp == str(code):
                    return redirect('loader')
                else:
                    messages.info(self.request, 'Incorrect Verification Code')
                    return redirect('otp')


def loader(request):
    context = {}
    return render(request, "loader.html", context)


class StudentListView(ListView):
    model = Details
    template_name = "accountants/Students.html"

    @method_decorator(moderator_login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentListView, self).dispatch(*args, **kwargs)

@moderator_login_required
def student_detailView(request, Slug=None):
    student = get_object_or_404(StudentList, Slug=Slug)
    context = {"student": student}
    return render(request, "accountants/detail_student.html", context)

def add_student(request):
    if request.method == "POST" or None:
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        department = request.POST.get("department")
        mobile = request.POST.get("mobile")
        studentid = request.POST.get("studentid")
        fees = request.POST.get("fees")
        amountpaid = request.POST.get("amountpaid")
        balance = request.POST.get("balance")

        student = Details(
            full_name=fullname,
            mobile=mobile,
            department=department,
            studentid=studentid,
            fees=fees,
            amount_paid=amountpaid,
            balance=balance,
            email=email
        )
        student.save()
        return redirect("listview")
    return render(request, "accountants/add.html")