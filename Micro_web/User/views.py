from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Profile
from itertools import chain
import datetime
from Blog.models import Post as postu


# Create your views here.


class ProfileListView(ListView):
    model = Profile
    template_name = 'User/personYouMayKnow.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'User/profile.html'
    context_object_name = 'profiles'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()

        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False
        context['follow'] = follow

        return context



def follow_and_unfollow(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)

        else:
            my_profile.following.add(obj.user)
    return redirect(request.META.get('HTTP_REFERER'))

def Posts_following(request):
    profile = Profile.objects.get(user=request.user)
    user = [user for user in profile.following.all()]
    posts = []
    qs = None
    for u in user:
        p = Profile.objects.get(user=u)
        p_posts = p.post_set.all()
        posts.append(p_posts)
    my_posts =profile.profiles_posts()
    posts.append(my_posts)

    if len(posts)>0:
        qs = sorted(chain(*posts),reverse=True, key = lambda obj: obj.time_upload)

    return render(request,'User/newsfeed.html',{'posts':qs})


def Trending(request):
    time =datetime.date.today()-datetime.timedelta(days=20)
    trends = postu.objects.filter(time_upload__gte = time).order_by('-view')
    contex={
     'trend':trends[:20],
    }
    return render(request,'User/trending.html',contex)

def Popular (request):
    time =datetime.date.today()-datetime.timedelta(days=365)
    popu = postu.objects.filter(time_upload__gte = time).order_by('-view')
    contex = {
    'trend': popu,
    }
    return render(request,'User/popular.html',contex)
