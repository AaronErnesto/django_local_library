"""
from django import forms



 # Para revisar el rango de las fechas de renovacion



class RenewBookForm(forms.Form):
	renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

	def clean_renewal_date(self):
		data = self.cleaned_data['renewal_date']

		# Revias que la fecha no esté en el pasado
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - renewal in past'))

		# Revisar si el la fecha de renovacion está en el rango permitidpo por la libreria (+4 semanas).
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('Invalid date - renewal more tha 4 weeks ahead'))

			# Recuerda siempre regresar los datos ya limpios

		return data
"""
from django.forms import ModelForm
from .models import BookInstance
from django.utils.translation import ugettext_lazy as _
import datetime
from django.core.exceptions import ValidationError

class RenewBookModelForm(ModelForm):
	def clean_due_back(self):
		data = self.cleaned_data['due_back']
		#Check date is not past
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - renewal in past'))

		#Check if date is in range linrarian alowed to change
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('invalid date - renewal more than 4 weeks ahead'))

		#Remember to always return the cleanes data
		return data

	class Meta:
		model = BookInstance
		fields = ['due_back']
		labels = {'due_back': _('Renewal date'),}
		help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3)'),}