from django.urls import path, include
from .views import *
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'workplace_violation_app'

urlpatterns = [
    path('submissions_table/', SubmissionsTableView.as_view(), name='submissions_table'),
    path('user_submissions/', UserSubmissionsTableView.as_view(), name='user_submissions'),
    path('login/', LoginView.as_view(), name='login'),
    path('', IndexView.as_view(), name='index'),
    path('', TemplateView.as_view(template_name="login.html")),
    path('accounts/', include('allauth.urls')),
    path('logout/', logout_view, name='logout'),
    path('submissions_table/serve_file/<str:file_path>/', SubmissionsTableView.as_view(), name='serve_file'),
    path('delete_submission', DeleteSubmission.as_view(), name="delete_submission"),
    path('view_report/<uuid:report_number>/', ViewReportView.as_view(), name='view_report'),
    path('user_report_action/<uuid:report_number>/', ReportActionView.as_view(), name='view_action'),
    path('report/mark_resolved/<uuid:report_number>/', ViewReportView.mark_as_resolved, name='mark_as_resolved'),
    path('user_report_view/<uuid:report_number>/', UserReportView.as_view(), name='user_report_view'),
    path('info', InfoView.as_view(), name='info'),
    path('case_search', CaseSearchView.as_view(), name='case_search'),
    path('confirm_delete/<uuid:report_number>/', ConfirmDelete.as_view(), name='confirm_delete')
]
