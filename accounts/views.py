from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View


class UserLogin(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            redirect_url = request.GET.get("next") or "dashboard:index"
            return redirect(redirect_url)
        context = {
            'message': 'Wrong password or username, please check and try again.'
        }
        return render(request, self.template_name, context)


def logout_user(request):
    logout(request)
    return redirect('accounts:login')
