from django import forms
from forwarding.models import Transmission, Statistic, Clients, Messages



class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_published":
                field.widget.attrs["class"] = "form-control"


class TransmissionCreateForm(StyleFormMixin, forms.ModelForm):
    """Form for create transmission"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].empty_label = "Select Message"

    class Meta:
        model = Transmission
        fields = ["title", "time", "frequency", "message", "clients"]


class ClientCreateForm(StyleFormMixin, forms.ModelForm):
    """Form for create client"""

    class Meta:
        model = Clients
        fields = ["full_name", "email", "comment"]



class StatisticForm(forms.ModelForm):
    """Show statistic of transmission"""

    class Meta:
        model = Statistic
        fields = ["time", "status", "mail_answer"]


class ClientsForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['full_name', 'comment']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ClientsCreateForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['full_name', 'email', 'comment']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['theme', 'body', 'owner']
        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'owner': forms.Textarea(attrs={'class': 'form-control'}),
        }


class MessagesFormUpdate(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['theme', 'body']
        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class MessagesCreateForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['theme', 'body']
        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TransmissionForm(forms.ModelForm):
    class Meta:
        model = Transmission
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }