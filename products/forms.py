from django import forms

from .models import Product, Attachment
# from category.models import Category

from multiupload.fields import MultiFileField


class ProductFilterForm(forms.Form):
	q = forms.CharField(label='Search', required=False)
	location = forms.CharField(label='Location (City & State or Zipcode)', required=False)
	distance_from = forms.CharField(label='Distance From Location (Miles)', widget=forms.TextInput(attrs={'type':'number'}), required=False)
	max_price = forms.DecimalField(decimal_places=2, max_digits=12, required=False)
	min_price = forms.DecimalField(decimal_places=2, max_digits=12, required=False)


class ProductModelForm(forms.ModelForm):
	zip_code_data = forms.CharField(label="Zip Code", required=True, max_length=5)

	#handle the multiple images
	files = MultiFileField(label="Images (Up to 30)", min_num=0, max_num=30, max_file_size=1024*1024*5)
	def save(self, commit=True):
		instance = super(ProductModelForm, self).save(commit)
		for each in self.cleaned_data['files']:
			Attachment.objects.create(file=each, product=instance)
		return instance

	class Meta:
		model = Product
		fields = [
			"title",
			"city",
			"description",
			"categories",
			"condition",
			# "media",
			"main_img",
			"files",
			"price",
			# "tags",
		]
		widgets = {
			"description": forms.Textarea(
					attrs={
						"placeholder": "Description"
					}
				),
			"title": forms.TextInput(
					attrs={
						"placeholder": "Title"
					}
				),
			"city": forms.TextInput(
					attrs={
						"placeholder": "City/Town"
					}
				)
		}

	def clean(self, *args, **kwargs):
		cleaned_data = super(ProductModelForm, self).clean(*args, **kwargs)
		return cleaned_data

	def clean_price(self):
		price = self.cleaned_data.get("price")
		if price < 0:
			raise forms.ValidationError("Price must be >= to $0.00")
		else:
			return price

	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(title) > 3:
			return title
		else:
			raise forms.ValidationError("Title must be greater than 3 characters long.")

class ProductModelUpdateForm(forms.ModelForm):
	zip_code_data = forms.CharField(label="Zip Code", required=True, max_length=5)

	class Meta:
		model = Product
		fields = [
			"title",
			"city",
			"description",
			"categories",
			"condition",
			"price",
		]
		widgets = {
			"description": forms.Textarea(
					attrs={
						"placeholder": "Description"
					}
				),
			"title": forms.TextInput(
					attrs={
						"placeholder": "Title"
					}
				),
			"city": forms.TextInput(
				attrs={
					"placeholder": "City/Town"
				}
			)
		}

	def clean(self, *args, **kwargs):
		cleaned_data = super(ProductModelUpdateForm, self).clean(*args, **kwargs)
		return cleaned_data

	def clean_price(self):
		price = self.cleaned_data.get("price")
		if price < 0:
			raise forms.ValidationError("Price must be >= to $0.00")
		else:
			return price

	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(title) > 3:
			return title
		else:
			raise forms.ValidationError("Title must be greater than 3 characters long.")