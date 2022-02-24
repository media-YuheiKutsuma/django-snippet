from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from snippets.models import Snippet, Comment
from django.contrib.auth.decorators import login_required
from snippets.forms import SnippetForm, CommentForm

# Create your views here.
def top(request):
    snippets = Snippet.objects.all() # Snippetの一覧を取得
    context = {
        "snippets": snippets 
    } # テンプレートに与えるPythonオブジェクト
    return render(request, "snippets/top.html", context)

# new
@login_required
def snippet_new(request):
    # POSTリクエスト
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)
    # GETリクエスト
    else:
        form = SnippetForm()
    return render(request, "snippets/snippet_new.html", {'form': form})

# edit
@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    print("---------------------------------")
    print(snippet.created_by_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden("このスニペットの編集は許可されていません。")

    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('snippet_detail', snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, 'snippets/snippet_edit.html', {'form': form})


def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    comment = Comment.objects.filter(commented_to=snippet.id).order_by('-commented_at')[:5]
    form = CommentForm()
    return render(request, 'snippets/snippet_detail.html', {
        'snippet':snippet,
        'form':form,
        'comment': comment,
    })
    


# 新規コメント登録
@login_required
def comment_new(request, snippet_id):
    form = CommentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            snippet = get_object_or_404(Snippet, pk=snippet_id)
            comment = form.save(commit=False)
            print(comment.text)
            comment.commented_to = snippet
            comment.commented_by = request.user
            comment.save()
            return redirect(snippet_detail, snippet_id=snippet_id)
    # GETリクエスト
    else:
        form = CommentForm()
    return render(request, "snippets/snippet_detail.html", {'snippet':snippet_id})