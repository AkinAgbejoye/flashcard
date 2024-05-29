# cards/models.py

from django.utils import timezone
from django.db import models

NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)

def getDecks():
    deck_names_queryset = Deck.objects.values_list('name', flat=True)

    # Convert the queryset to a list
    deck_names_list = list(deck_names_queryset)

    # Create choices tuple
    deck_choices = [(name, name) for name in deck_names_list]

    return deck_choices

class Deck(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Card(models.Model):
    question = models.TextField()
    answer = models.TextField()
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    date_created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.question
    
    def move(self, solved):
         new_box = self.box + 1 if solved else BOXES[0]
  
         if new_box in BOXES:
              self.box = new_box
              self.save()
  
         return self
    
class LearningHistory(models.Model):
    card = models.IntegerField()
    queried_at = models.DateTimeField(auto_now_add=True)
    known = models.BooleanField()

    def __str__(self):
        return f"{self.card} - {self.known} - {self.queried_at}"





  