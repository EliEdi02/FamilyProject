from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Photo, Comment, TicTacToeGame
from .forms import CommentForm, PhotoForm, TicTacToeCreateForm


def home(request):
    query = request.GET.get('q', '').strip()

    photos = Photo.objects.all().order_by('-created_at')

    if query:
        photos = photos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(uploaded_by__username__icontains=query)
        ).order_by('-created_at')

    paginator = Paginator(photos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gallery/home.html', {
        'photos': page_obj,
        'page_obj': page_obj,
        'query': query,
    })


def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    comments = photo.comments.all().order_by('-created_at')
    related_photos = Photo.objects.exclude(id=photo.id).order_by('-created_at')[:6]

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Du musst eingeloggt sein, um zu kommentieren.")
            return redirect('home')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.author = request.user
            comment.save()
            messages.success(request, "Kommentar erfolgreich gespeichert.")
            return redirect('photo_detail', photo_id=photo.id)
        else:
            messages.error(request, "Der Kommentar konnte nicht gespeichert werden.")
    else:
        form = CommentForm()

    return render(request, 'gallery/photo_detail.html', {
        'photo': photo,
        'comments': comments,
        'form': form,
        'related_photos': related_photos,
    })


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            photo.save()
            messages.success(request, "Bild erfolgreich hochgeladen.")
            return redirect('home')
        else:
            messages.error(request, "Das Bild konnte nicht hochgeladen werden.")
    else:
        form = PhotoForm()

    return render(request, 'gallery/upload_photo.html', {'form': form})


@login_required
def edit_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.user != photo.uploaded_by and not request.user.is_superuser:
        return HttpResponseForbidden("Du darfst dieses Bild nicht bearbeiten.")

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, "Bild erfolgreich bearbeitet.")
            return redirect('photo_detail', photo_id=photo.id)
        else:
            messages.error(request, "Die Änderungen konnten nicht gespeichert werden.")
    else:
        form = PhotoForm(instance=photo)

    return render(request, 'gallery/edit_photo.html', {
        'form': form,
        'photo': photo,
    })


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.user != photo.uploaded_by and not request.user.is_superuser:
        return HttpResponseForbidden("Du darfst dieses Bild nicht löschen.")

    if request.method == 'POST':
        photo.delete()
        messages.success(request, "Bild erfolgreich gelöscht.")
        return redirect('home')

    return render(request, 'gallery/delete_photo.html', {'photo': photo})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author and not request.user.is_superuser:
        return HttpResponseForbidden("Du darfst diesen Kommentar nicht bearbeiten.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Kommentar erfolgreich bearbeitet.")
            return redirect('photo_detail', photo_id=comment.photo.id)
        else:
            messages.error(request, "Der Kommentar konnte nicht bearbeitet werden.")
    else:
        form = CommentForm(instance=comment)

    return render(request, 'gallery/edit_comment.html', {
        'form': form,
        'comment': comment,
    })


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author and not request.user.is_superuser:
        return HttpResponseForbidden("Du darfst diesen Kommentar nicht löschen.")

    photo_id = comment.photo.id

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Kommentar erfolgreich gelöscht.")
        return redirect('photo_detail', photo_id=photo_id)

    return render(request, 'gallery/delete_comment.html', {
        'comment': comment,
    })


@login_required
def download_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return FileResponse(
        photo.image.open('rb'),
        as_attachment=True,
        filename=photo.image.name.split('/')[-1]
    )


@login_required
def my_photos(request):
    photos = Photo.objects.filter(uploaded_by=request.user).order_by('-created_at')

    paginator = Paginator(photos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gallery/my_photos.html', {
        'photos': page_obj,
        'page_obj': page_obj,
    })


@login_required
def tic_tac_toe_list(request):
    games = TicTacToeGame.objects.all().order_by('-created_at')
    form = TicTacToeCreateForm()

    if request.method == 'POST':
        game = TicTacToeGame.objects.create(player_x=request.user)
        messages.success(request, "Neues Tic-Tac-Toe-Spiel erstellt.")
        return redirect('tic_tac_toe_detail', game_id=game.id)

    open_games = []
    running_games = []
    finished_games = []

    for game in games:
        if game.winner or game.is_draw:
            finished_games.append(game)
        elif game.player_o is None:
            open_games.append(game)
        else:
            running_games.append(game)

    return render(request, 'gallery/tictactoe_list.html', {
        'games': games,
        'form': form,
        'open_games': open_games,
        'running_games': running_games,
        'finished_games': finished_games,
    })


def check_tictactoe_winner(board):
    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    for a, b, c in winning_combinations:
        if board[a] != '-' and board[a] == board[b] == board[c]:
            return board[a]

    return None


@login_required
def tic_tac_toe_detail(request, game_id):
    game = get_object_or_404(TicTacToeGame, id=game_id)

    if game.player_o is None and request.user != game.player_x:
        game.player_o = request.user
        game.save()
        messages.success(request, "Du bist dem Spiel als Spieler O beigetreten.")

    board = list(game.board)

    current_user_symbol = None
    if request.user == game.player_x:
        current_user_symbol = 'X'
    elif request.user == game.player_o:
        current_user_symbol = 'O'

    is_players_turn = (
        current_user_symbol is not None and
        game.current_turn == current_user_symbol and
        not game.winner and
        not game.is_draw and
        game.player_o is not None
    )

    opponent_name = None
    if current_user_symbol == 'X' and game.player_o:
        opponent_name = game.player_o.username
    elif current_user_symbol == 'O':
        opponent_name = game.player_x.username

    winner_name = None
    if game.winner == 'X':
        winner_name = game.player_x.username
    elif game.winner == 'O' and game.player_o:
        winner_name = game.player_o.username

    return render(request, 'gallery/tictactoe_detail.html', {
        'game': game,
        'board': list(enumerate(board)),
        'current_user_symbol': current_user_symbol,
        'is_players_turn': is_players_turn,
        'opponent_name': opponent_name,
        'winner_name': winner_name,
    })


@login_required
def tic_tac_toe_move(request, game_id, cell_index):
    game = get_object_or_404(TicTacToeGame, id=game_id)

    if game.winner or game.is_draw:
        messages.error(request, "Dieses Spiel ist bereits beendet.")
        return redirect('tic_tac_toe_detail', game_id=game.id)

    if game.player_o is None:
        messages.error(request, "Das Spiel hat noch keinen zweiten Spieler.")
        return redirect('tic_tac_toe_detail', game_id=game.id)

    if request.user == game.player_x:
        player_symbol = 'X'
    elif request.user == game.player_o:
        player_symbol = 'O'
    else:
        messages.error(request, "Du bist kein Spieler in diesem Spiel.")
        return redirect('tic_tac_toe_detail', game_id=game.id)

    if game.current_turn != player_symbol:
        messages.error(request, "Du bist gerade nicht am Zug.")
        return redirect('tic_tac_toe_detail', game_id=game.id)

    board = list(game.board)

    if cell_index < 0 or cell_index > 8:
        messages.error(request, "Ungültiges Feld.")
        return redirect('tic_tac_toe_detail', game_id=game.id)

    if board[cell_index] != '-':
        messages.error(request, "Dieses Feld ist bereits belegt.")
        return redirect('tic_tac_toe_detail', game_id=game.id)

    board[cell_index] = player_symbol
    winner = check_tictactoe_winner(board)

    if winner:
        game.board = ''.join(board)
        game.winner = winner
        game.save()
        messages.success(request, f"Spiel beendet. {winner} hat gewonnen.")
        return redirect('tic_tac_toe_detail', game_id=game.id)

    if '-' not in board:
        game.board = ''.join(board)
        game.is_draw = True
        game.save()
        messages.success(request, "Spiel beendet. Unentschieden.")
        return redirect('tic_tac_toe_detail', game_id=game.id)

    game.board = ''.join(board)
    game.current_turn = 'O' if game.current_turn == 'X' else 'X'
    game.save()

    return redirect('tic_tac_toe_detail', game_id=game.id)


@login_required
def tic_tac_toe_delete(request, game_id):
    game = get_object_or_404(TicTacToeGame, id=game_id)

    if request.user != game.player_x and request.user != game.player_o and not request.user.is_superuser:
        return HttpResponseForbidden("Du darfst dieses Spiel nicht löschen.")

    if request.method == 'POST':
        game.delete()
        messages.success(request, "Das Tic-Tac-Toe-Spiel wurde gelöscht.")
        return redirect('tic_tac_toe_list')

    return render(request, 'gallery/tictactoe_delete.html', {
        'game': game,
    })


@login_required
def tic_tac_toe_end(request, game_id):
    game = get_object_or_404(TicTacToeGame, id=game_id)

    if request.user != game.player_x and request.user != game.player_o and not request.user.is_superuser:
        return HttpResponseForbidden("Du darfst dieses Spiel nicht beenden.")

    if request.method == 'POST':
        if not game.winner and not game.is_draw:
            game.is_draw = True
            game.save()
            messages.success(request, "Das Spiel wurde beendet.")
        return redirect('tic_tac_toe_detail', game_id=game.id)

    return render(request, 'gallery/tictactoe_end.html', {
        'game': game,
    })