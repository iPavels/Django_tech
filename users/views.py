from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import UserRegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("catalog:home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            send_mail(
                subject="Добро пожаловать!",
                message=(
                    f"Здравствуйте, {user.email}!\n\n"
                    "Регистрация прошла успешно. "
                    "Добро пожаловать в наш сервис!"
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(
                request,
                "Регистрация прошла успешно! Приветственное письмо отправлено.",
            )

            return redirect("users:login")

    else:
        form = UserRegisterForm()

    return render(
        request,
        "users/register.html",
        {"form": form},
    )