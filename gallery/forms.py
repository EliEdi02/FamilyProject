from django import forms
from .models import Comment, Photo, TicTacToeGame


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Schreibe einen Kommentar...'
            }),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Titel des Bildes'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Beschreibung (optional)'
            }),
        }

class TicTacToeCreateForm(forms.ModelForm):
    class Meta:
        model = TicTacToeGame
        fields = []