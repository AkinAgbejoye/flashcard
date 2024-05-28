# cards/urls.py

from django.urls import path


from . import views
 
urlpatterns = [
path(
    "",
    views.CardListView.as_view(),
    name="card-list"
),
path(
        "new",
        views.CardCreateView.as_view(),
        name="card-create"
    ),
     path(
        "new",
        views.CardCreateView.as_view(),
        name="card-create"
    ),
    path(
        "edit/<int:pk>",
        views.CardUpdateView.as_view(),
        name="card-update"
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
]