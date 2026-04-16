
from django.db import models
from django.urls import reverse
import uuid
from  django.contrib.auth.models import User
from datetime import date
class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    author = models.ManyToManyField(Author)
    summary = models.TextField(max_length=1000)
    isbn = models.CharField(max_length=13, unique=True)

    def display_author(self):
        return ",".join([author.first_name for author in self.author.all()])

    display_author.short_description = "Авторы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class BookInstance(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True
    )

    inv_nom = models.CharField(
        max_length=20,
        null=True,
        help_text="Инвентарный номер книги",
        verbose_name="Инвентарный номер книги"
    )

    imprint = models.CharField(
        max_length=20,
        help_text="Введите издательство и год выпуска",
        verbose_name="Издательство"
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=True,
        help_text="Изменить состояние экземпляра",
        verbose_name="Статус экземпляра книги"
    )

    due_back = models.DateField(
        null=True,
        blank=True,
        help_text="Введите конец срока статуса",
        verbose_name="Дата окончания статуса"
    )


    borrower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Выберите заказчика книги",
        verbose_name="Заказчик"
    )


    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


    def __str__(self):
        return f"{self.id} ({self.book})"
