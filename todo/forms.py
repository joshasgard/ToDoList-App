from django.forms import ModelForm
from .models import Todo



class TodoForm():
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']