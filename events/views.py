from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Count,Q
from .models import Event,Participant,Category
from .forms import EventModelForm,ParticipantModelForm,CategoryModelForm
from datetime import date


# Create your views here.
def home(request):
    today=date.today()
    events=Event.objects.select_related('category').prefetch_related('participants').order_by('date')[:6]
    
    context={
        "events":events,
        'today':today
    }
    return render(request,"home.html",context)
    

def organizer_dashboard(request):
    type=request.GET.get('type','today')
    today=date.today()
    
    counts=Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id',filter=Q(date__gt=today)),
        past=Count('id',filter=Q(date__lt=today)),
        today=Count('id',filter=Q(date=today)),
        
    )
    total_participant=Participant.objects.count()
    
    base_query=Event.objects.select_related('category').prefetch_related('participants')
    
    if type == 'upcoming':
        events=base_query.filter(date__gt=today)
    elif type == 'past':
        events=base_query.filter(date__lt=today)
    elif type == 'today':
        events=base_query.filter(date=today)
    elif type == 'total':
        events=base_query.all()
    else:
        events = base_query.all()
    # elif type == 'participant':
    #     events = Participant.objects.all() 
        
    context={
        'events':events,
        'counts':counts,
        'total_participant':total_participant,
        "type": type 
    }
    return render(request,'events/organizer_dashboard.html',context)


# event CRUD

def event_list(request):
    events=Event.objects.select_related('category').prefetch_related('participants')
    return render(request,"events/event_list.html",{'events':events})


def event_create(request):
    event_form=EventModelForm()
    if request.method == "POST":
        event_form=EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request,"Event Created Successfully")
            return redirect('event_list')
    
    return render(request,"events/form.html",{
        "event_form":event_form,
        "title":"event",
    })
    
def event_update(request,id):
    event=Event.objects.get(id=id)
    event_form=EventModelForm(instance=event)
    if request.method == "POST":
        event_form=EventModelForm(request.POST,instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request,"Update Event Successfully")
            return redirect("event_list")
        else:
            print(event_form.errors)
            
    return render(request,"events/form.html",{
        "event_form":event_form,
        "title":"Event"
    })
    
def event_delete(request,id):
    event=Event.objects.get(id=id)
    
    if request.method == "POST":
        event.delete()
        messages.success(request,"Event Delete Successfully")
        
    return redirect("event_list")    

def category_create(request):
    event_form=CategoryModelForm()
    
    if request.method == 'POST':
        event_form=CategoryModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request,"Category Created Successfully")
            return redirect("organizer_dashboard")
        
    return render(request,'events/form.html',{
        "event_form":event_form,
        "title":"Category"
    })
    
    
def participant_create(request,event_id):
    event=Event.objects.get(id=event_id)
    event_form = ParticipantModelForm()
    # event_form = ParticipantModelForm(initial={'event': [event.id]})
    if request.method == 'POST':
        event_form=ParticipantModelForm(request.POST or None, initial={'event':[event]})
        if event_form.is_valid():
            participant = event_form.save(commit=False)
            participant.save()
            participant.event.set([event])
            messages.success(request,"participant added Successfully")
            return redirect("organizer_dashboard")
        
    return render(request,'events/form.html',{
        "event_form":event_form,
        "title":f"Participant of {event.name}"
    })
    

    
