from django.urls import path
from . import views
from .views import Login, Signup, OrderView, SearchView

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("authors/<authors>/<n_book>/", views.buy, name="buy_order"),
    path("authors/<authors>/", views.authors, name="authors_book"),
    path("authors/", views.books, name="author"),
    path("login", Login.as_view(), name="login"),
    path("signup", Signup.as_view(), name="signup"),
    path('logout', views.logout, name='logout'),
    path('orders', OrderView.as_view(), name='orders'),
    path("search/", SearchView.as_view(), name="search"),
     path("search/<authors>/<n_book>/", views.buy, name="buy_order2"),
]

