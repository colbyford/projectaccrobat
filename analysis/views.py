from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm

# Create your views here.

def stringer(file):
	with open(str(file)) as f :
		output = f.readline()
	return(output)

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    return render(request, 'analysis/post_list.html', {'posts' : posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'analysis/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.output = stringer(str(post.file))
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'analysis/post_edit.html', {'form': form})

