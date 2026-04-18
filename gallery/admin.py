from django.contrib import admin
from .models import Photo, Comment
from .models import Photo, Comment, TicTacToeGame


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'created_at')
    search_fields = ('title', 'uploaded_by__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'photo', 'created_at')
    search_fields = ('author__username', 'photo__title', 'text')

@admin.register(TicTacToeGame)
class TicTacToeGameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player_x', 'player_o', 'current_turn', 'winner', 'is_draw', 'created_at')