from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm

# Create your views here.

def maftovcf(file):
	with open(file) as rawfile, open(file+'_outputtemp.vcf', 'a') as vcffile:	
		for line in rawfile.readlines():
			if line.startswith('Hugo_Symbol'):
				continue
			line = line.rstrip()
			columns = line.split("\t")
			chromo = ['chr'+columns[4]]
			start = [columns[5]]
			ID = [columns[13]]
			QUAL = ['.']
			Filter = ['.']
			ref = [columns[10]]
			alt = [columns[12]]
			INFO = [columns[15]]
			vcf = chromo+start+ID+ref+alt+QUAL+Filter+INFO
			vcff = "\t".join(vcf)
			if columns[8] == 'Missense_Mutation':
				vcffile.write(vcff+'\n')
		vcffile.close()
	return(vcffile)


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
            #post = Post(file=request.FILES['file'])
            post.author = request.user
            post.published_date = timezone.now()
            parse = maftovcf(post.file.url)
            post.output = (str(post.file)+'_outputtemp.vcf')
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'analysis/post_edit.html', {'form': form})

