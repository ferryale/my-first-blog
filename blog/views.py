from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Document
from .forms import PostForm, CommentForm, DocumentForm

# Create your views here.

def post_list(request):
	posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})
	
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull = True).order_by('-created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})
	
def post_detail(request, pk):
	post = get_object_or_404(Post, pk = pk)
	return render(request, 'blog/post_detail.html',  {'post': post})

def authorization_error(request):
	return render(request, 'blog/authorization_error.html')
	
def information(request):
	return render(request, 'blog/information.html')
	
@login_required	
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit = False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk = post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required		
def post_edit(request, pk):
	post = get_object_or_404(Post, pk = pk)
	if(post.author == request.user):
		if request.method == "POST":
			form = PostForm(request.POST, instance = post)
			if form.is_valid():
				post = form.save(commit = False)
				post.author = request.user
				post.created_date = timezone.now()
				post.published_date = None
				post.save()
				return redirect('post_detail', pk = post.pk)		
		else:
			form = PostForm(instance = post)
	else:
		return redirect('authorization_error')	
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required	
def post_publish(request, pk):
	post = get_object_or_404(Post, pk = pk)
	if(post.author == request.user):
		post.publish()
	else:
		return redirect('authorization_error')
	return redirect('blog.views.post_list')
	
@login_required	
def post_remove(request, pk):
	post = get_object_or_404(Post, pk = pk)
	if(post.author == request.user):
		post.delete()
	else:
		return redirect('authorization_error')
	return redirect('blog.views.post_list')
	
def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk = pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
		    	comment = form.save(commit = False)
		    	comment.post = post
		    	if request.user.is_authenticated():
		    		comment.author = request.user
		    	comment.save()
		    	return redirect('blog.views.post_detail', pk = post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})
	
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', pk = comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk = post_pk)
 
def document_list(request):
    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(request, 'blog/document_list.html',{'documents': documents})

@login_required   
def document_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'], author = request.user, published_date = timezone.now())
            newdoc.save()
            # Redirect to the document list after POST
            return redirect('blog.views.document_list')       
    else:
        form = DocumentForm()  # A empty, unbound form

    documents = Document.objects.all()
    # Render list page with the documents and the form
    return render(request, 'blog/document_upload.html',{'documents': documents,'form': form})
    
@login_required	
def document_remove(request, pk):
	document = get_object_or_404(Document, pk = pk)
	if(document.author == str(request.user)):
		document.docfile.delete()
		document.delete()
	else:
		return redirect('authorization_error')
	return redirect('blog.views.document_list')
	
