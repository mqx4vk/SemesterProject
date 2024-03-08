from django.urls import path, include
from .views import LoginView, IndexView, SubmissionsTableView, logout_view
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'workplace_violation_app'

urlpatterns = [
    path('submissions_table/', SubmissionsTableView.as_view(), name='submissions_table'),
    path('login/', LoginView.as_view(), name='login'),
    path('', IndexView.as_view(), name='index'),
    path('', TemplateView.as_view(template_name="login.html")),
    path('accounts/', include('allauth.urls')),
    path('logout/', logout_view, name='logout')
]
