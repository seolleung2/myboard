from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import Paginator

from member.models import BoardMember
from .models import Board
from tag.models import Tag
from .forms import BoardForm

def board_list(request):
    all_boards  = Board.objects.all().order_by('-id')
    page        = int(request.GET.get('p', 1))
    pagenator   = Paginator(all_boards, 5)
    boards      = pagenator.get_page(page)
    return render(request, 'board_list.html', {"boards":boards})

def board_write(request):
    if not request.session.get('user'):
        return redirect('/member/login/')

    if request.method == "POST":
        form = BoardForm(request.POST)

        if form.is_valid():
            user_id         = request.session.get('user')
            member          = BoardMember.objects.get(pk=user_id)

            tags            = form.cleaned_data['tags'].split(',')

            board = Board()
            board.title     = form.cleaned_data['title']
            board.contents  = form.cleaned_data['contents']
            board.writer    = member
            board.save()

            for tag in tags:
                if not tag:
                    continue

                _tag, _ = Tag.objects.get_or_create(name=tag)
                board.tags.add(_tag)

            return redirect('/board/list/')

    else:
        form = BoardForm()

    return render(request, 'board_write.html', {'form':form})

def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'board_detail.html', {'board':board})
