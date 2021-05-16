import json

from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
from django.views import View

from .models import KpiChans
from .forms import ChanForm

from redis import Redis

redis = Redis(host='localhost', port=6379)


class ChanCreateView(View):
    def get(self, request):
        chans = KpiChans.objects.all()
        form = ChanForm()

        return render(request, 'create_chan.html', {
            'form': form.as_p(),
            'chans': chans,
        })

    def post(self, request):
        form = ChanForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')


class ChanEditView(View):
    def get(self, request, pk):
        cached_chan = redis.get(pk)
        if cached_chan is not None:
            chan = KpiChans.from_dict(json.loads(cached_chan))
        else:
            chan = KpiChans.objects.get(pk=pk)
            redis.set(pk, json.dumps(chan.as_dict()))

        form = ChanForm(instance=chan)

        return render(request, 'edit_chan.html', {
            'form': form.as_p(),
        })

    def post(self, request, pk):
        chan = KpiChans.objects.get(pk=pk)
        form = ChanForm(request.POST, instance=chan)

        if form.is_valid():
            form.save()
            redis.delete(pk)
            return HttpResponseRedirect('/')


class ChanDeleteView(View):
    def post(self, request, pk):
        chan = KpiChans.objects.get(pk=pk)
        chan.delete()
        redis.delete(pk)
        return HttpResponseRedirect('/')
