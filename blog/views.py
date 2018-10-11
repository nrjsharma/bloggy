from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,Http404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render , get_object_or_404
from django.template.loader import render_to_string
from django.forms import modelformset_factory
from django.contrib import messages

# Create your views here.
def post_list(request):

    query=request.GET.get('q')

    if query:
        data=Post.objects.filter(
            Q(title__icontains=query)|
            Q(author__username=query)|
            Q(body__icontains=query)

        )
    else:

        data = Post.published.all()

    paginator = Paginator(data, 10)  # Show 10 contacts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # now if there are lot of posts which result in like 200 pages.Then rather than showing pages like 1.2.3.4...200 you can limit this line 1.2.3..10
    # and when some one click on page like 7 then list will be like 3.4.5.6.7.8...13

    if page is None:
        start_index=0
        end_index=7
    else:
        (start_index,end_index) = proper_pagination(posts,index=4)

    page_range = list(paginator.page_range)[start_index:end_index]



    context={
        'post' : posts,
        'query'    : query,
        'page_range':page_range
    }

    return render(request,'blog/post_list.html',context)

def proper_pagination(posts,index):
    start_index=0
    end_index=7

    if posts.number > index:
        start_index=posts.number - index
        end_index = start_index - end_index

    return (start_index, end_index)


def post_details(request,id,slug):

    # data = Post.objects.get(id=id)

    post = get_object_or_404(Post, id=id, slug=slug)
    comments = Comments.objects.filter(post=post,reply=None).order_by('-id')
    is_liked = False

    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    else:
        is_liked = False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comments.objects.get(id=reply_id)
            comment = Comments.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            # return HttpResponseRedirect(post.get_absolute_url())

    else:
        comment_form = CommentForm()


    context = {
        'post': post,
        'is_liked':is_liked,
        'total_likes':post.total_likes,
        'comments': comments,
        'comment_form': comment_form,

    }

    if request.is_ajax():
        html = render_to_string('blog/comment.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'blog/post_details.html', context)


def post_create(request):

        ImageFormset = modelformset_factory(Images, fields=('image',), extra=4)

        if request.method == 'POST':

            formm=PostCreateForm(request.POST)
            formset = ImageFormset(request.POST or None, request.FILES or None)
            if formm.is_valid() and formset.is_valid():
                post= formm.save(commit=False)
                post.author = request.user
                post.save()
                formm=PostCreateForm() #reseting form

                for f in formset:
                    print(f.cleaned_data)
                    try:

                        photo = Images(post=post, image=f.cleaned_data.get('image'))

                        if f.cleaned_data.get('image') is not None:
                            photo.save()

                    except Exception as e:
                        break
                messages.success(request,"Post has been successfully created")
                return redirect('post_list')

            else:
                print(formm.errors)

        else:
            formm = PostCreateForm()
            formset = ImageFormset(queryset=Images.objects.none())

        context={

            'form':formm,
            'formset': formset,

        }

        return render(request,'blog/post_create.html',context)


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    ImageFormset = modelformset_factory(Images, fields=('image',), extra=4, max_num=4)
    if post.author != request.user:
        raise Http404()
    if request.method == "POST":

        form = PostEditForm(request.POST or None, instance=post)

        formset = ImageFormset(request.POST or None, request.FILES or None)

        if form.is_valid() and formset.is_valid():

            form.save()

            print(formset.cleaned_data)


            data = Images.objects.filter(post=post)

            for index, f in enumerate(formset):

                if f.cleaned_data:

                    if f.cleaned_data['id'] is None:

                        photo = Images(post=post, image=f.cleaned_data.get('image'))

                        photo.save()

                    elif f.cleaned_data['image'] is False:

                        photo = Images.objects.get(id=request.POST.get('form-' + str(index) + '-id'))

                        photo.delete()

                    else:

                        photo = Images(post=post, image=f.cleaned_data.get('image'))

                        d = Images.objects.get(id=data[index].id)

                        d.image = photo.image

                        d.save()

            messages.success(request, "{} has been successfully updated!".format(post.title))
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
        formset = ImageFormset(queryset=Images.objects.filter(post=post))


    context = {
    'form': form,
    'post': post,
    'formset': formset,
    }
    return render(request, 'blog/post_edit.html', context)





def user_login(request):

    if request.method == 'POST':

        formm = UserLoginForm(request.POST)

        if formm.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request,user)
                    print('user login')
                    return redirect('post_list')
                else:
                    return HttpResponse('user not active')

            else:
                return HttpResponse('User name or password not matched')

    else:

        formm=UserLoginForm()

        context={
             'form':formm,
        }

        return render(request,'blog/login.html',context)


def user_logout(request):
    logout(request)
    return redirect('post_list')

def registration(request):

    if request.method == "POST":

            formm = UserRegistrationForm(request.POST)

            if formm.is_valid():
                new_user=formm.save(commit=False)
                new_user.set_password(formm.cleaned_data['password'])
                new_user.save()

                Profile.objects.create(user=new_user)  # create empty profile of new_user

                # after successful signup automatic login

                user = authenticate(request, username=formm.cleaned_data['username'], password=formm.cleaned_data['password'])

                if user is not None:

                    if user.is_active:
                        login(request, user)
                        print('user login')
                        return redirect('post_list')

                else:
                    return HttpResponse('User name or password not matched')


    else:
        formm=UserRegistrationForm()

        context={
            'form':formm,
        }

        return render(request,'registration/register.html',context)




@login_required(login_url='/')
def edit_profile(request):

    if request.method =="POST":

            user_Edit_form = UserEditForm(data=request.POST or None , instance=request.user)
            Profile_Edit_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)


            if user_Edit_form.is_valid() and Profile_Edit_form.is_valid():
                user_Edit_form.save()
                Profile_Edit_form.save()
                return redirect('edit_profile')

    else:

        user_Edit_form= UserEditForm(instance=request.user)
        Profile_Edit_form = ProfileEditForm(instance=request.user.profile)

        context={
            'user_form':user_Edit_form,
            'prfile_form':Profile_Edit_form,
        }

        return render(request,'blog/edit_profile.html',context)


def post_like(request):

    post=get_object_or_404(Post, id=request.POST.get('post_id'))

    is_liked=False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False

    else:
        post.likes.add(request.user)
        is_liked = True

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes
    }

    if request.is_ajax():
        html=render_to_string('blog/like_section.html',context,request=request)
        return JsonResponse({'form': html})


def post_delete(request, id):
    print(id)
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        print('inhere')
        raise Http404()
    # postImages.delete()
    post.delete()

    messages.warning(request, 'post has been successfully deleted!')
    return redirect('post_list')

