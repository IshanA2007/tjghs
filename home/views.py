# views.py
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, View
from requests_oauthlib import OAuth2Session
from .models import User, ServiceHoursForm
import os
import datetime
from .models import Submission
from .forms import SubmissionForm

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_ID = "zlMe655n4YD3on047tNyessOhnZIemHmuPoP3WSA"
REDIRECT_URI = "http://localhost:8000/profile/"
CLIENT_SECRET = 'jpUSngc4sSyFp3S19XEIDvnErvqLQHMq4HgDLIV4uUybIz8bQbUqg5xiNZzbHakS5feHH2JY1aCCoL0XMq5zpGa80XaIO3qYwA36C1Z44FNqigCBhG0heXlhraxj3R0z'
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["read", "write"])
authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signed_in"] = self.request.session.get('is_signed_in', False)
        return context

    template_name = "home.html"


class OfficersView(TemplateView):
    template_name = "officers.html"


class AboutView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signed_in"] = self.request.session.get('is_signed_in', False)
        return context

    template_name = "about.html"


def signin(request):
    return redirect(authorization_url)


class ProfileView(View):
    def get(self, request):
        if 'username' not in request.session or not request.session['username']:
            global IS_SIGNED_IN
            CODE = request.GET.get("code")
            token = oauth.fetch_token("https://ion.tjhsst.edu/oauth/token/",
                                      code=CODE,
                                      client_secret=CLIENT_SECRET)
            try:
                profile = oauth.get("https://ion.tjhsst.edu/api/profile")
            except TokenExpiredError as e:
                args = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
                token = oauth.refresh_token("https://ion.tjhsst.edu/oauth/token/", **args)
            request.session['is_signed_in'] = True
            import json
            profile_data = json.loads(profile.content.decode())
            username = profile_data.get('ion_username')

            user, created = User.objects.get_or_create(username=username)
            print(created)
            print(user.numServiceHours)
            if created:
                print("new user!")
                user.inductedDate = datetime.strptime("05/30/24", "%m/%d/%y").date()
                user.numServiceHours = 0
            user.save()
            request.session['username'] = username
            form = SubmissionForm()
            curusersubmissions = Submission.objects.filter(user=request.session['username'])
            return render(request, "profile.html",
                          {"user": user, "form": form, "curusersubmissions": curusersubmissions})
        else:
            user = User.objects.get(username=request.session['username'])
            form = SubmissionForm()
            submissions = Submission.objects.all()
            curusersubmissions = Submission.objects.filter(user=request.session['username'])
            return render(request, "profile.html", {"user": user, "form": form, "submissions": submissions,
                                                    "curusersubmissions": curusersubmissions})

    def post(self, request):
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)

            submission.user = request.session['username']
            print(request.session['username'])
            submission.save()
        user = User.objects.get(username=request.session['username'])

        submissions = Submission.objects.all()
        curusersubmissions = Submission.objects.filter(user=request.session['username'])
        # user.numServiceHours += submission.service_hours
        # user.save()
        return render(request, "profile.html", {"user": user, "form": form, "submissions": submissions,
                                                "curusersubmissions": curusersubmissions})


class EventsView(TemplateView):
    template_name = "events.html"


class ServiceHoursView(TemplateView):
    def get(self, request):
        form = ServiceHoursForm()

        return render(request, 'service_hours.html', {'form': form})

    def post(self, request):
        '''form = ServiceHoursForm(request.POST)
        if form.is_valid():
            service_hours = form.cleaned_data['service_hours']
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']
            print(service_hours)
            # Handle the form data as needed, e.g., save to the database
            # Assuming the User model has fields for service_hours, date, and description

            # Example code:
            print(request.session['username'])
            user = User.objects.get(username=request.session['username'])
            user.numServiceHours += service_hours
            print(user.numServiceHours)
            user.save()

            # Redirect back to the original page
            return redirect("http://localhost:8000/signin/")  # Assuming 'service_hours' is the name of your URL pattern
'''
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
        return redirect("http://localhost:8000/signin/")


def approve_submission(request):
    if request.method == 'POST':
        submission_user = request.POST.get('submission_user')
        submission_hours = request.POST.get('submission_service_hours')
        submission_id = request.POST.get('submission_id')
        user = User.objects.get(username=submission_user)
        user.numServiceHours += int(submission_hours)
        user.save()
        submission = Submission.objects.get(id=submission_id)
        submission.delete()
        return redirect("http://localhost:8000/profile#admin/")


def reject_submission(request):
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        submission = Submission.objects.get(id=submission_id)
        submission.delete()
    return redirect("http://localhost:8000/profile/")
