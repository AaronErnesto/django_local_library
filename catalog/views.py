from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre, Language

def index(request):
	"""
	Funcion vista para la página inicio de sitio
	"""

	#Genera contadores de alagunos de los objetos principales
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	#Libros disponibles (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.count() #El all() está implícito por defecto


	# Númeo de visitas a esta vista, contadas en la sesion de variable}
	num_visits = request.session. get('num_visits',0)
	request.session['num_visits'] = num_visits+1

	#Libros del género 'clasico'
	num_genre_clasico = Book.objects.filter(genre__name__icontains='clasico').count()

	#Renderiza la plantilla HTML index.html con los datos de la variable contexto
	return render(
		request,
		'index.html',
		context = {'num_books':num_books, 'num_instances':num_instances, 'num_instances_available':num_instances_available, 'num_authors':num_authors, 'num_genre_clasico':num_genre_clasico, 'num_visits':num_visits}, # num_visists appended
	)

from django.views import generic

class BookListView(generic.ListView):
	"""docstring for BookListView"""
	model = Book
	paginate_by = 2

class BookDetailView(generic.DetailView):
	model = Book

class AuthorListView(generic.ListView):
	model = Author
	paginate_by=2

class AuthorDetailView(generic.DetailView):
	model = Author

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	"""
	Generic class-based view listing books on loan to current user.
	"""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
	permission_required = 'catalog.can_mark_returned'
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_all.html'
	paginate_by = 10

	def get_queryset(self):	
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
#from django.core.urlresolvers import reverse
import datetime

from .forms import RenewBookModelForm

"""

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):


	book_inst = get_object_or_404(BookInstance, pk = pk)

	# Si esta es una petición POST entonces procesa los datos del formulario
	if request.method == 'POST':

		# Crea una instancia de formilario y la llena con los datos del request (binding):
		form = RenewBookForm(request.POST)

		# Revisa si el formulario es válido.
		if form.is_valid():
			# Procesa los datos en form.cleaned_data de la froma requerida. 
			book_inst.due_back = form.cleaned_data['renewal_date']
			book_inst.save()

			# Redirigue hacia una nueva URL
			return HttpResponseRedirect(reverse('all-borrowed'))
	# Si esta esta es GET o cualquier otro método crea el formulario por default	
	else:
		proposed_renewed_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookForm(initial={'renewal_date': proposed_renewed_date,})
	return render(request, 'catalog/book_renew_librarian.html',{'form':form, 'bookinst':book_inst})

""" 

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(PermissionRequiredMixin, CreateView):
	permission_required = 'catalog.can_mark_returned'
	model = Author
	fields = '__all__'
	initial = {'date_of_death':'05/01/2018',}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'catalog.can_mark_returned'
	model = Author
	fields = ['first_name','last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'catalog.can_mark_returned'
	model = Author
	success_url = reverse_lazy('authors')
	

	
class BookCreate(PermissionRequiredMixin, CreateView):
	permission_required = 'can_mark_returned'
	model = Book
	fields = '__all__'

class BookUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'can_mark_returned'
	model = Book
	fields = '__all__'

class BookDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'can_mark_returned'
	model = Book
	success_url = 'books'