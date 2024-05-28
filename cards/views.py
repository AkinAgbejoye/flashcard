# cards/views.py
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
import logging
from django import forms

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
    success_url = reverse_lazy('deck_list')

class CardListView(ListView):
    model = Card
    queryset = Card.objects.all()


class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer","deck", "box"]

    widget = {
        "question":forms.Textarea(attrs={'class':'form-control', 'cols': 100, 'rows': 5}),
        "answer":forms.Textarea(attrs={'class':'form-control','cols': 100, 'rows': 5}),
        "deck":forms.Select(attrs={'class':'form-control'}),
        "box":forms.Select(attrs={'class':'form-control d-none'})
    }
    success_url = reverse_lazy("card-create")

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
        return Card.objects.filter(deck=self.kwargs["deck"]).exclude(id__in=card_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card_list = list(self.get_queryset())
        
        current_index = self.request.GET.get('current_index', 0)
        try:
            current_index = int(current_index)
        except ValueError:
            current_index = 0

        if card_list:
            if 0 <= current_index < len(card_list):
                context["check_card"] = card_list[current_index]
            else:
                context["check_card"] = None
        else:
            context["check_card"] = None
        
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])
            card.move(form.cleaned_data["solved"])
            id=form.cleaned_data["card_id"]
            solved = form.cleaned_data["solved"] 
            # print("Debug information:", solved)
            LearningHistory(card=id, known=solved,queried_at=timezone.now()).save()
        

        return redirect(request.META.get("HTTP_REFERER"))



def filter_learning_history():
    # Calculate the timestamp for 48 hours ago
    time_threshold = timezone.now() - timedelta(hours=48)

    # Filter LearningHistory records where queried_at is within the last 48 hours and known is True
    recent_known_records = LearningHistory.objects.filter(
        queried_at__gte=time_threshold,
        known=True
    )

    # Aggregate and filter groups of entries having the same card with a count of exactly 2
    card_counts = recent_known_records.values('card').annotate(card_count=Count('card')).filter(card_count=2)
    
    # Get the card IDs that match the above criteria
    card_ids = [entry['card'] for entry in card_counts]
    
    # Retrieve the corresponding LearningHistory records
    filtered_records = LearningHistory.objects.filter(card__in=card_ids, queried_at__gte=time_threshold, known=True)
    
    # Render the results to a template (or handle as needed)
    return card_ids
