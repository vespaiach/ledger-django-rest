from django.urls import path

from . import views


urlpatterns = [
    path("reasons", views.ReasonView.as_view()),
    path("transactions/<int:id>", views.TransactionView.as_view()),
    path("transactions", views.TransactionsView.as_view()),
    path("doc", views.api_doc),
]
