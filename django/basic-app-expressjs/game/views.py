from django.http import JsonResponse
from .models import GameOption
from django.views import generic

# API views


def GameEndpoint(request):
    return JsonResponse({"questions": list(GameOption.objects.values())}, safe=False)


class IndexView(generic.ListView):
    model = GameOption
    template_name = "game/index.html"
    context_object_name = "gameoptions_list"
