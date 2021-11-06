from django.shortcuts import render
from datacenter.models import format_duration
from datacenter.models import Passcard
from datacenter.models import Visit


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.filter(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    # Программируем здесь
    this_passcard_visits = []
    for visit in visits:
        this_passcard_visits.append({
            'entered_at': visit.entered_at,
            'duration': format_duration(visit.get_duration()),
            'is_strange': visit.is_long(minutes=60)
        })

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
