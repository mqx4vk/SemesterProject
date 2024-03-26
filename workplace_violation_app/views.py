import base64

import boto3
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import generic
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import logout
from django.views import View
from .forms import AnonymousForm
from .models import Report
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .forms import AdminNotesForm
from django.shortcuts import redirect

class LoginView(AuthLoginView):
    template_name = 'workplace_violation_app/login.html'

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("workplace_violation_app:index"))  

class IndexView(generic.View):
    form = AnonymousForm()
    template_name = 'workplace_violation_app/index.html'
    def get(self, request):
        form = AnonymousForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        form = AnonymousForm(request.POST,request.FILES)
        if form.is_valid():
            if request.user.is_authenticated:
                user = request.user
                date = form.cleaned_data['report_date']
                text = form.cleaned_data['report_text']
                file = form.cleaned_data['report_file']

                anonymous_user = Report.objects.create(report_user=user,report_date =date, report_text=text, report_file=file)

                anonymous_user.save()

                return render(request, 'workplace_violation_app/submission.html')
            else:
                date = form.cleaned_data['report_date']
                text = form.cleaned_data['report_text']
                file = form.cleaned_data['report_file']

                anonymous_user = Report.objects.create(report_date=date, report_text=text,report_file=file)
                anonymous_user.save()
                return render(request, 'workplace_violation_app/submission.html')
        else:
            print("Form is not valid")
            print("Errors:", form.errors)
            
            return render(request, self.template_name, {'form':form})

class ViewReportView(View):
    template_name = 'workplace_violation_app/view_report.html'

    def get(self, request, report_number, *args, **kwargs):
        report = get_object_or_404(Report, pk=report_number)
        notes_form = AdminNotesForm(instance=report)
        if report.report_status == "New" or report.report_status == "new" :
            report.report_status = "In Progress"
            report.save()
        return render(request, self.template_name, {'report':report, 'notes_form': notes_form})
    
    def post(self, request, report_number, *args, **kwargs):
        report = get_object_or_404(Report, pk=report_number)
        notes_form = AdminNotesForm(request.POST, instance=report)
        if notes_form.is_valid():
            notes_form.save()
            return redirect('workplace_violation_app:view_report', report_number=report_number)
        return render(request, self.template_name, {'report': report, 'notes_form': notes_form})
    
    def mark_as_resolved(request, report_number):
        report = get_object_or_404(Report, report_number=report_number)
        report.report_status = 'Resolved'
        report.save()
        return redirect('workplace_violation_app:submissions_table')


class SubmissionsTableView(View):
    template_name = 'workplace_violation_app/submissions_table.html'
    def get(self, request, *args, **kwargs):
        submissions = Report.objects.all().order_by('-report_date')
        context = {'submissions':submissions}
        return render(request, self.template_name, context)
    
class ReportActionView(View):
    template_name = 'workplace_violation_app/report_action.html'

    def get(self, request, report_number, *args, **kwargs):
        report = get_object_or_404(Report, pk=report_number,report_user=request.user)
        return render(request,self.template_name, {'report':report})

    
    

class UserSubmissionsTableView(View):
    template_name = 'workplace_violation_app/user_submissions.html'
    def get(self, request, *args, **kwargs):
        file_path = kwargs.get('file_path')

        if file_path:
            report_file = get_object_or_404(Report, report_file=file_path)
            s3_url = report_file.url
            return HttpResponseRedirect(s3_url)

        submissions = Report.objects.all().order_by('-report_date')
        context = {'submissions': submissions}
        return render(request, self.template_name, context)
class DeleteSubmission(View):
    template_name = 'workplace_violation_app/user_submissions.html'
    def post(self, request, *args, **kwargs):
        report_id = request.POST.get('report_id')
        if report_id:
            report = get_object_or_404(Report, id=report_id)
            report.delete()
            submissions = Report.objects.all().order_by('-report_date')
            context = {'submissions': submissions}
            return render(request, self.template_name, context)
        else:
            submissions = Report.objects.all().order_by('-report_date')
            context = {'submissions': submissions}
            return render(request, self.template_name, context)
    # def get(self, request, *args, **kwargs):
    #     file_path = kwargs.get('file_path')
    #     report_id = request.GET.get('report_id')
    #     report = get_object_or_404(Report, id=report_id)
    #     report.delete()
        submissions = Report.objects.all().order_by('-report_date')
        context = {'submissions': submissions}
        return render(request, self.template_name, context)