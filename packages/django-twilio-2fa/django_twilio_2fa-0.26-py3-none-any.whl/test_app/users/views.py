from django.contrib.auth.decorators import login_required


@login_required
def index_view(request, *args, **kwargs):
    return "happy"
