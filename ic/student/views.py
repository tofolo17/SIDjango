# Create your views here.
from django.shortcuts import render, get_object_or_404

from professor.models import Simulador


def simulator(request, token):
    sim = get_object_or_404(Simulador, token=token)
    return render(
        request,
        'student/simulator.html',
        {'simulator': sim}
    )
