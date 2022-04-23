from django.contrib.auth.models import User
from django.contrib.auth.models import User as OriginUser
from django.db import models
from django.forms import ValidationError
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Reason(BaseModel):
    text = models.CharField(unique=True, max_length=255, blank=False)

    # https://www.sqlite.org/faq.html#:~:text=(9)%20What%20is%20the%20maximum,all%20500%2Dmillion%20characters%20intact.
    # SQLite doesn't enforce the length of varchar
    def clean(self):
        if not self.text or len(self.text) == 0:
            raise ValidationError(
                "Please enter reason text.")

        if len(self.text) > 255:
            raise ValidationError(
                "Reason text shouldn't be more than 255 characters.")

    class Meta:
        ordering = ["text"]

    def __str__(self):
        return f"id:{self.id}|text:{self.text}"


class Transaction(BaseModel):
    amount = models.IntegerField(blank=False)
    date = models.DateTimeField(blank=False)
    note = models.CharField(max_length=511, blank=True)

    reasons = models.ManyToManyField(Reason, blank=False)

    def clean(self):
        if self.note and len(self.note) > 511:
            raise ValidationError(
                "Note shouldn't be more than 511 characters.")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"id:{self.id}|amount:{self.amount}|date:{self.date}"


class Token(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iat = models.IntegerField(blank=False)
