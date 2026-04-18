from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Kommentar von {self.author.username} zu {self.photo.title}'
    



class TicTacToeGame(models.Model):
    player_x = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_x')
    player_o = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_as_o')

    board = models.CharField(max_length=9, default='---------')
    current_turn = models.CharField(max_length=1, default='X')
    winner = models.CharField(max_length=1, blank=True, null=True)
    is_draw = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        opponent = self.player_o.username if self.player_o else "offen"
        return f"{self.player_x.username} vs {opponent}"

    def board_list(self):
        return list(self.board)