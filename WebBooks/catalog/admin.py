from django.contrib import admin
from .models import Author, Book, Genre, Language, Status, BookInstance


# Регистрация справочных моделей
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)


# Author admin
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


admin.site.register(Author, AuthorAdmin)



class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


# Book admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # показываем title и удобные представления m2m полей через методы
    list_display = ('title', 'display_author', 'display_genre', 'language')
    list_filter = ('genre', 'language')
    inlines = [BooksInstanceInline]

    def display_author(self, obj):
        """
        Отображает авторов для ManyToMany поля author как строку.
        Если у вас поле называется иначе — поправьте имя.
        """
        try:
            return ", ".join(str(a) for a in obj.author.all())
        except Exception:
            return ""
    display_author.short_description = "Authors"

    def display_genre(self, obj):
        try:
            return ", ".join(str(g) for g in obj.genre.all())
        except Exception:
            return ""
    display_genre.short_description = "Genres"


# BookInstance admin — вынесен отдельно (не вложен в BookAdmin)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('book', 'status')
    list_display = ('book', 'status', 'due_back',"id","borrower")
    fieldsets = (
        ('Book', {
            'fields': ('book', 'imprint', 'inv_nom')
        }),
        ('Availability', {
            'fields': ('status', 'due_back',"borrower")
        }),
    )