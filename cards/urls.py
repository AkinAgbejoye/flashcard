# cards/urls.py

from django.urls import path
from . import views 
from .views import get_name

urlpatterns = [
path(
    "manage",
    views.CardListView.as_view(),
    name="card-list"
),
path(
        "new",
        views.CardCreateView.as_view(),
        name="card-create"
    ),
    #  path(
    #     "new",
    #     views.CardCreateView.as_view(),
    #     name="card-create"
    # ),
    path(
        "edit/<int:pk>",
        views.CardUpdateView.as_view(),
        name="card-update"
    ),

     path(
        "delete/<int:id>",
        views.BoxView.delete_card,
        name="card-delete"
    ),

    path(
        "box/<int:box_num>",
        views.BoxView.as_view(),
        name="box"
    ),
     path(
        "deck/<str:deck>",
        views.BoxView.as_view(),
        name="deck"
    ),
    
    path('decks/', views.DeckListView.as_view(), name='deck_list'),
    path('add/', views.DeckCreateView.as_view(), name='deck_add'),
    path('deck/<int:id>/delete/', views.DeckCreateView.delete_deck, name='delete_deck'),
    path('', get_name, name='get_name'),
]