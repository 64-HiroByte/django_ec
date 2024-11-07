from django.contrib.auth.views import LoginView


# Create your views here.
class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
