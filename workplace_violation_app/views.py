from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import logout
from django.views import View
from .forms import AnonymousForm
from .models import AnonReportInfo

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
            date = form.cleaned_data['report_date']
            text = form.cleaned_data['report_text']
            file = form.cleaned_data['report_file']

            anonymous_user = AnonReportInfo.objects.create(report_date =date,report_text=text,report_file=file)

            anonymous_user.save()

            return render(request, 'workplace_violation_app/submission.html')
        
        else:
            print("Form is not valid")
            print("Errors:", form.errors)
            
            return render(request, self.template_name, {'form':form})
        
class SubmissionsTableView(View):
    template_name = 'workplace_violation_app/submissions_table.html'
    def get(self, request):
        return render(request, self.template_name)
