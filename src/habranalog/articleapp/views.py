from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from articleapp.models import *
from django.contrib.auth.decorators import login_required
from articleapp.forms import * 
def home(request):
    user_filter_state=request.session.get('user_filter_state','up')
    data=Article.objects.filter(published=True).all().order_by('date_published')
    if request.GET.get('sort_by')=='up':
        request.session['user_filter_state']='up'
        user_filter_state=request.session['user_filter_state']
        data=Article.objects.filter(published=True).all().order_by('date_published')
    elif request.GET.get('sort_by')=='down':
        request.session['user_filter_state']='down'
        user_filter_state= request.session['user_filter_state']
        data=Article.objects.filter(published=True).all().order_by('-date_published')
    return render(request,'articleapp/home.html',{'articles':data,'user_filter_state':user_filter_state})


def view_art(request,art_id):
    if request.user.has_perm('articleapp.can_read_article'):
        viewscount=Views.objects.filter(article=art_id).count()
        data=get_object_or_404(Article,pk=art_id,published=True)
        try:
            v=Views.objects.create(user=request.user,article=data)
        except:
            pass
        blocks=ArticlesBlock.objects.filter(article=art_id)
        return render(request,'articleapp/view_art.html',{'article':data,'blocks':blocks,'viewscount':viewscount})
    else:
        return HttpResponse('<h2>Access denied</h2>')

@login_required
def create_article(request):
    if request.method=='GET':
        return render(request,'articleapp/create_article.html',{'form':CreateArticleForm()})
    else: 
        try:
            form=CreateArticleForm(request.POST,request.FILES)
            newart=form.save(commit=False)
            newart.author=request.user
            form.save()
            return redirect('articleapp:home')
        except ValueError:
            return render(request,'articleapp/create_article.html',{'form':CreateArticleForm(),'error':'неккоректные значения'})

@login_required
def change_article(request,art_id):
    article=get_object_or_404(Article,pk=art_id,author=request.user)
    if request.method=='GET':
          return render(request,'articleapp/change_article.html',{'article':article})
    else: 
        try:
            form=CreateArticleForm(request.POST,request.FILES,instance=article)
            form.save()
            return redirect('articleapp:home')
        except ValueError:
            return render(request,'articleapp/change_article.html',{'error':'неккоректные значения','article':article})


@login_required
def view_article(request,art_id): # переименовать view_art
    article_=get_object_or_404(Article,pk=art_id,author=request.user)
    articleblocks=ArticlesBlock.objects.filter(article=art_id)
    return render(request,'articleapp/view_article.html',{'article':article_,'articleblocks':articleblocks}) 

@login_required
def delete_article(request,art_id):
    article=get_object_or_404(Article,pk=art_id,author=request.user)
    if request.method=='POST':
        article.published=False
        article.save()
        return redirect('articleapp:home')
