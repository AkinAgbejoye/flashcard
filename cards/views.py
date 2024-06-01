# cards/views.py
import random
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
import logging
from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)
from django.shortcuts import get_object_or_404, redirect, render
from .models import Card, LearningHistory
from .forms import CardCheckForm
from .models import Deck
from .forms import DeckForm



class DeckListView(ListView):
    model = Deck
    template_name = 'cards/deck_list.html'
    context_object_name = 'cards'

class DeckCreateView(CreateView):
    model = Deck
    form_class = DeckForm
    template_name = 'cards/deck_form.html'
    success_url = reverse_lazy('card-list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            form = DeckForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('card-list')
               
        else:
            form = DeckForm()

    def delete_deck(request, id):
        deck = get_object_or_404(Deck, id=id)
        deck.delete()
        return redirect('card-list')
    
    def get_context_data(self, **kwargs):
    # Get the default context data from the superclass method
        context = super().get_context_data(**kwargs)

        # Retrieve the name from the session, or use a default value
        name = self.request.session.get('name', 'Guest')

        # Add the name to the context
        context['name'] = name

        return context
        


    

class CardListView(ListView):
    model = Card
    queryset = Card.objects.all()
    template_name = 'all_card.html'  # Ensure you have this template
    context_object_name = 'card_list'
    paginate_by = 9

    def get_context_data(self, **kwargs):
    # Get the default context data from the superclass method
        context = super().get_context_data(**kwargs)

        # Retrieve the name from the session, or use a default value
        name = self.request.session.get('name')
        wrong = self.request.session.get('wrong')
        correct = self.request.session.get('correct')
         
        # Add the name to the context
        context['name'] = name
        context['wrong'] = wrong
        context['correct'] = correct

        return context
    
 


class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer","deck", "box"]
    deck = forms.ModelChoiceField(queryset=Deck.objects.all())
    widget = {
        "question":forms.Textarea(attrs={'class':'form-control', 'cols': 100, 'rows': 5}),
        "answer":forms.Textarea(attrs={'class':'form-control','cols': 100, 'rows': 5}),
        "deck":forms.Select(attrs={'class':'form-control'}),
        "box":forms.Select(attrs={'class':'form-control d-none'})
    }
    success_url = reverse_lazy("card-create")

    

    def get_context_data(self, **kwargs):
    # Get the default context data from the superclass method
        context = super().get_context_data(**kwargs)

        # Retrieve the name from the session, or use a default value
        name = self.request.session.get('name')

        # Add the name to the context
        context['name'] = name

        return context


# class CardCreateView(CreateView):
#       model = Card
#       fields = ["question", "answer", "box"]
#       success_url = reverse_lazy("card-create")

class CardUpdateView(CardCreateView, UpdateView):
     success_url = reverse_lazy("card-list")

class BoxView(CardListView):
    template_name = "cards/box.html"
    form_class = CardCheckForm
    # def get_queryset(self):
    #     return Card.objects.filter(box=self.kwargs["box_num"])
    def get_queryset(self):
        card_ids = filter_learning_history()
        logger = logging.getLogger(__name__)
        logger.info(f"card_ids: {card_ids}")
        deck = Deck.objects.get(name=self.kwargs["deck"])
        return Card.objects.filter(deck=deck).exclude(id__in=card_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card_list = list(self.get_queryset())
        if self.object_list:
            context["check_card"] = random.choice(self.object_list)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])
            card.move(form.cleaned_data["solved"])
            id=form.cleaned_data["card_id"]
            solved = form.cleaned_data["solved"] 
            # print("Debug information:", solved)
            if solved == True:             
               request.session['correct'] = request.session['correct'] + 1
               LearningHistory(card=id, known=solved,queried_at=timezone.now()).save()
            else:
                request.session['wrong'] = request.session['wrong'] + 1
        

        return redirect(request.META.get("HTTP_REFERER"))
    
    def delete_card(request, id):
        card = get_object_or_404(Card, id=id)
        card.delete()
        return redirect('card-list')

    def display_name(request):
        name = request.session.get('name')
        return name



def filter_learning_history():
    # Calculate the timestamp for 48 hours ago
    time_threshold = timezone.now() - timedelta(hours=48)

    # Filter LearningHistory records where queried_at is within the last 48 hours and known is True
    recent_known_records = LearningHistory.objects.filter(
        queried_at__gte=time_threshold,
        known=True
    )

    # Aggregate and filter groups of entries having the same card with a count of exactly 2
    card_counts = recent_known_records.values('card').annotate(card_count=Count('card')).filter(card_count__gte=2)
    print( card_counts)
    # Get the card IDs that match the above criteria
    card_ids = [entry['card'] for entry in card_counts]
    
    # Retrieve the corresponding LearningHistory records
    filtered_records = LearningHistory.objects.filter(card__in=card_ids, queried_at__gte=time_threshold, known=True)
    
    # Render the results to a template (or handle as needed)
    return card_ids

def get_name(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')  # Get the value of the 'name' field from the form
        request.session['name'] = name  # Store the name in the session (optional)
        request.session['wrong'] = 0
        request.session['correct'] = 0
        return redirect('card-list')  # Redirect to another view to display the name

    return render(request, 'cards/player_form.html')

def quit(request):
    request.session['name'] = ""  
    request.session['wrong'] = 0
    request.session['correct'] = 0
    return redirect('get_name')



    
