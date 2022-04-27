from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


UserModel = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        raise NotImplementedError("")

    class Meta:
        abstract = True


class Reason(BaseModel):
    # https://www.sqlite.org/faq.html#:~:text=(9)%20What%20is%20the%20maximum,all%20500%2Dmillion%20characters%20intact.
    # SQLite doesn't enforce the length of varchar
    text = models.CharField(unique=True, max_length=255, blank=False)

    class Meta:
        ordering = ["text"]

    def __str__(self):
        return f"id:{self.id}|text:{self.text}"

    def to_dict(self):
        return dict(id=self.id, text=self.text)


class Transaction(BaseModel):
    amount = models.IntegerField(blank=False)
    date = models.DateTimeField(blank=False)
    note = models.CharField(max_length=511, blank=True)

    reasons = models.ManyToManyField(Reason, blank=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=False)

    class Meta:
        ordering = ["-date"]

    def get_reasons(self):
        return self.reasons.all()

    def to_dict(self):
        return dict(
            id=self.id, amount=self.amount, date=self.date, note=self.note, reasons=[
                r.to_dict() for r in self.get_reasons()]
        )

    def __str__(self):
        return f"id:{self.id}|amount:{self.amount}|date:{self.date}"
