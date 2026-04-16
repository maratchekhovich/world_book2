from django.shortcuts import render, redirect
from django.views import generic
from .models import Author,Book, BookInstance
from .forms import AuthorForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookUpdate(UpdateView):
        model = Book
        fields = '__all__'
        success_url = reverse_lazy('books')

class BookDelete(DeleteView):
            model = Book
            success_url = reverse_lazy('books')
def index(request):
    num_books = Book.objects.count()

class AuthorListView(generic.ListView):
    model = Author

# Главная страница
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_ordered = BookInstance.objects.filter(status__name='On loan').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_ordered': num_instances_ordered,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context)


# Добавление автора
def author_add(request):

    author = Author.objects.all()
    authorsform = AuthorForm()
    return render(request, 'catalog/authors_add.html',
                  {'form': authorsform, 'author': author})


# Список книг
class BookListView(generic.ListView):
    model = Book


# Детали книги
class BookDetailView(generic.DetailView):
    model = Book


# Список книг текущего пользователя
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status__name='В заказе'
        ).order_by('due_back')


from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # создаем пользователя без пароля
            user = form.save(commit=False)
            user.set_unusable_password()  # нельзя войти без сброса пароля
            user.save()

            reset_form = PasswordResetForm({'email': user.email})
            if form.is_valid():
                user = form.save(commit=False)
                user.set_unusable_password()
                user.save()

                send_reset_email(user, request)
                return redirect("login")

            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

def send_reset_email(user, request):
    reset_form = PasswordResetForm({'email': user.email})
    if reset_form.is_valid():
        reset_form.save(
            request=request,
            use_https=False,
            domain_override='127.0.0.1:8000',
            from_email='maratchekhovich@gmail.com',
            email_template_name='registration/password_reset_email.html',  # текстовая версия
            html_email_template_name='registration/password_reset_email.html'  # HTML версия
        )
