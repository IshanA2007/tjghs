from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from requests_oauthlib import OAuth2Session
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_ID = "zlMe655n4YD3on047tNyessOhnZIemHmuPoP3WSA"
REDIRECT_URI = "http://localhost:8000/profile/"
CLIENT_SECRET = 'jpUSngc4sSyFp3S19XEIDvnErvqLQHMq4HgDLIV4uUybIz8bQbUqg5xiNZzbHakS5feHH2JY1aCCoL0XMq5zpGa80XaIO3qYwA36C1Z44FNqigCBhG0heXlhraxj3R0z'
oauth = OAuth2Session(CLIENT_ID,
                          redirect_uri=REDIRECT_URI,
                          scope=["read", "write"])
authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")

IS_SIGNED_IN = False


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signed_in"] = IS_SIGNED_IN
        return context

    template_name = "home.html"





class OfficersView(TemplateView):
    template_name = "officers.html"


class AboutView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signed_in"] = IS_SIGNED_IN
        return context
    template_name = "about.html"

def signin(request):
    return redirect(authorization_url)
def profile(request):
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
    IS_SIGNED_IN = True
    import json
    print(json.loads(profile.content.decode()))
    print(IS_SIGNED_IN)

    return render(request, "profile.html")


class EventsView(TemplateView):
    template_name = "events.html"
