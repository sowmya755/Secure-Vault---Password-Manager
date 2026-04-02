from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignupForm, PasswordEntryForm
from .models import PasswordEntry 
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import PasswordEntry, UserPIN

# ---------------- HOME PAGE ----------------

def home_page(request):
    return render(request, 'home.html')


# ---------------- HELP PAGE ----------------

def help_page(request):
    return render(request, "help.html")


# ---------------- SIGNUP ----------------

def signup_page(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            return redirect("login")

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


# ---------------- USER LOGIN ----------------

def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

        else:
            return render(request, "login.html", {"error": "Invalid Credentials"})

    return render(request, "login.html")


# ---------------- USER DASHBOARD ----------------

@login_required
def dashboard(request):

    entries = PasswordEntry.objects.filter(user=request.user)

    return render(request, "dashboard.html", {"entries": entries})


# ---------------- ADD PASSWORD ----------------

@login_required
def add_password(request):

    if request.method == "POST":

        form = PasswordEntryForm(request.POST)

        if form.is_valid():

            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()

            return redirect("dashboard")

    else:
        form = PasswordEntryForm()

    return render(request, "add_password.html", {"form": form})


# ---------------- UPDATE PASSWORD ----------------

@login_required
def update_password(request, pk):

    entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)

    if request.method == "POST":

        form = PasswordEntryForm(request.POST, instance=entry)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = PasswordEntryForm(instance=entry)

    return render(request, "update_password.html", {"form": form})


# ---------------- DELETE PASSWORD ----------------

@login_required
def delete_password(request, pk):

    entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)

    if request.method == "POST":

        entry.delete()
        return redirect("dashboard")

    return render(request, "delete_password.html", {"entry": entry})


# ---------------- ENTER PIN (FIXED) ----------------


# @login_required
# def enter_pin(request, pk):
#     entry = get_object_or_404(PasswordEntry, id=pk)

#     # 🚫 block other users
#     if request.user != entry.user:
#         return redirect('dashboard')

#     # ✅ safe get
#     user_pin = UserPIN.objects.filter(user=request.user).first()

#     # 🚫 no PIN
#     if not PasswordEntry:
#         messages.warning(request, "Please set your PIN first")
#         return redirect('set_pin')

#     if request.method == "POST":
#         entered_pin = request.POST.get('pin')

#         if not entered_pin:
#             messages.error(request, "Please fill out the field")

#         elif entered_pin != user_pin.pin:
#             messages.error(request, "Wrong PIN")

#         else:
#             return redirect('vault', pk=entry.id)

#     return render(request, 'enter_pin.html')

@login_required
def enter_pin(request, pk):
    entry = get_object_or_404(PasswordEntry, id=pk)

    # 🚫 மற்ற user access block
    if request.user != entry.user:
        return redirect('dashboard')

    # 🔐 user PIN get
    user_pin = UserPIN.objects.filter(user=request.user).first()

    if request.method == "POST":
        entered_pin = request.POST.get('pin')

        # ❌ empty
        if not entered_pin:
            messages.error(request, "Enter PIN")

        # 🆕 first time → create PIN
        elif not user_pin:
            UserPIN.objects.create(user=request.user, pin=entered_pin)
            messages.success(request, "PIN set & unlocked")
            return redirect('vault', pk=entry.id)

        # ✅ correct PIN → unlock
        elif entered_pin == user_pin.pin:
            return redirect('vault', pk=entry.id)

        # ❌ wrong PIN
        else:
            messages.error(request, "Wrong PIN")

    return render(request, 'enter_pin.html')
# ----------------vault page------------------

@login_required
def vault_views(request, pk):
    entry = get_object_or_404(PasswordEntry, id=pk)

    if request.user != entry.user:
        return redirect('dashboard')

    return render(request, 'vault.html', {'entry': entry})

# ---------------- USER LOGOUT ----------------

def logout_user(request):

    logout(request)
    return redirect("login")