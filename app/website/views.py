from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import get_user_model
from threads.models import Thread
from jobs.models import JobPost
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


# Create your views here.


@login_required(login_url="/login/")
def index(request):
    user_count = User.objects.count()
    new_user = User.objects.filter(
        is_active=True, created_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    thread_count = Thread.objects.count()
    job_count = JobPost.objects.count()
    print("User count: ", user_count)

    context = {
        "segment": "index",
        "user_count": user_count,
        "new_user": new_user,
        "thread_count": thread_count,
        "job_count": job_count,
    }

    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def threads(request):
    threads = Thread.objects.all()
    context = {"threads": threads}
    context["segment"] = "threads"

    html_template = loader.get_template("home/threads.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))


def logout(request):
    context = {"segment": "logout"}

    html_template = loader.get_template("home/logout.html")
    return HttpResponse(html_template.render(context, request))
