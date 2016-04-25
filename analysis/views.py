from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
import os

def snpeff(file):
	javastring = str("java -d64 -Xms512m -Xmx4g -jar snpEff/snpEff.jar GRCh37.75 analysis/uploads/" + file + '_output.vcf' + ' > ' + 'analysis/uploads/' + file + '_annotated.vcf')
	output = os.system(javastring)
	return(output)

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
		snpeff(file+'outputtemp.vcf') #call snpEff function
	return(vcffile)


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
            post.vcfoutput = (str(post.file)+'_outputtemp.vcf')
            post.snpeffvcfoutput = (str(post.vcfoutput)+'_annotated.vcf')
            post.snpeffhtmloutput = (str(post.vcfoutput)+'_annotated.html')
            post.snpeffhtmlmissenseoutput = (str(post.vcfoutput)+'_missense.html')
            post.save()
            

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'analysis/post_edit.html', {'form': form})

