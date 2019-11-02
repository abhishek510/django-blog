from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,CreateView,DetailView
from .models import *
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from itertools import zip_longest

# Create your views here.



# view to create a new blog 
class CreateBlogView(LoginRequiredMixin,CreateView):
    model=Blog
    template_name='blog/create.html'
    fields=['title','text']
# validates the form 
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)




# main page displays blogs,likes,views,dislikes
def dashboard(request):
    blogs=Blog.objects.all()
    likes=Like.objects.values('blog').annotate(Count('blog')).order_by('blog')
    l=[]
    for i in likes:
        l.append(i.get('blog__count'))
    dislikes=Dislike.objects.values('blog').annotate(Count('blog')).order_by('blog')
    dl=[]
    for i in dislikes:
        dl.append(i.get('blog__count'))
    comments=Comment.objects.values('blog').annotate(Count('blog')).order_by('blog')
    c=[]
    for i in comments:
        c.append(i.get('blog__count'))
    v=[]
    blog_views=UrlHit.objects.values('url').annotate(Count('url')).order_by('url')
    for i in blog_views:
        v.append(i.get('url__count'))
    data=zip_longest(blogs,l,dl,c,v,fillvalue=0)
    return render(request,'blog/dashboard.html',{'dataset':data})



class HomeView(LoginRequiredMixin,ListView):
    model=Blog
    template_name='blog/index.html'

    def get(self,request):
        return dashboard(request)



class ViewDashboard(LoginRequiredMixin,ListView):
    model=Blog
    template_name='blog/index.html'

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)
        

def AddComment(request,pk):
    blog=get_object_or_404(Blog,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)#dont save to db here future changes will be made
            comment.blog=blog
            comment.name=blog.author.username
            comment.save()
            return redirect('blog-details',pk=pk)#after adding comment redirect to detail view of blog
    else:
        form=CommentForm()
        
    return render(request,'blog/create_comment.html',{'form':form})



def add_like(request, pk):
    new_like, created = Like.objects.get_or_create(user=request.user, blog_id=pk)
    if not created:
        pass
        # the user already liked this before
    else:
        new_like.save()
    return redirect('blog-details',pk=pk)



def add_dislike(request, pk):
    new_dislike, created = Dislike.objects.get_or_create(user=request.user, blog_id=pk)
    if not created:
        pass
        # the user already disliked this before
    else:
        new_dislike.save()
    return redirect('blog-details',pk=pk)



# returns ip address of user requesting
# tracking hits on a page is done with ip addresses to deny multiple hits by same source
def get_ip(request):
    x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip



def hit_count(request):
    if not request.session.session_key:
        request.session.save()
    s_key=request.session.session_key
    ip=get_ip(request)
    url,url_created=UrlHit.objects.get_or_create(url=request.path)

    if url_created:
        track,created=HitCount.objects.get_or_create(url_hit=url,ip=ip,session=s_key)
        if created:
            url.increase()
            request.session[ip]=ip
            request.sessions[request.path]=request.path
    else:
        if ip and request.path not in request.session:
            track,created=HitCount.objects.get_or_create(url_hit=url,ip=ip,session=s_key)
            if created:
                url.increase()
                request.session[ip]=ip
                request.session[request.path]=request.path
    return url.hit



#renders the detail view of each blog
def BlogView(request,pk):
    blog=Blog.objects.get(pk=pk)
    a=hit_count(request)
    # increase hit count when user opens a blog in detail view
    likes=Like.objects.filter(blog=blog)
    dislikes=Dislike.objects.filter(blog=blog)
    return render(request,'blog/blog_detail.html',{'object':blog,'likes':likes,'dislikes':dislikes})
    


# renders top blog page with most likes,dislikes,comments
def top_blogs(request):
    blogs=Blog.objects.all()
    blog_likes=[]
    blog_dislikes=[]
    blog_comments=[]
    likes=Like.objects.values('blog').annotate(Count('blog')).order_by('blog__count')
    dislikes=Dislike.objects.values('blog').annotate(Count('blog')).order_by('blog__count')
    comments=Comment.objects.values('blog').annotate(Count('blog')).order_by('blog__count')
    for like in likes:
        blog_likes.append((Blog.objects.get(pk=like.get('blog')),like.get('blog__count')))
    for dislike in dislikes:
        blog_dislikes.append((Blog.objects.get(pk=dislike.get('blog')),dislike.get('blog__count')))
    for comment in comments:
        blog_comments.append((Blog.objects.get(pk=comment.get('blog')),comment.get('blog__count')))
    return render(request,'blog/top_blogs.html',{'likes':blog_likes,'dislikes':blog_dislikes,'comments':blog_comments})
