# Imports
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime, now
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from .models import Post, UserProfile, Comment
from .forms import PostForm, CommentForm, ShareForm
from django.http import HttpResponseRedirect, HttpResponse


# Class for listing post in the database
class PostListView(View):
    # GET post
    def get(self, request, *args, **kwargs):
        # Orders the post
        posts = Post.objects.all().order_by('-created_on')
        # Form for entering text in the post
        form = PostForm()
        # Form for entering text in the share post
        share_form = ShareForm()
        # Contect for use in HTML files
        context = {
            'post_list': posts,
            'form': form,
            'shareform': share_form,
        }
        # Redirects to home
        return render(request, 'social/post_list.html', context)

    # Same function as above, but POST request
    def post(self, request, *args, **kwargs):
        posts = Post.objects.all()
        form = PostForm(request.POST)
        share_form = ShareForm()
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
        context = {
            'post_list': posts,
            'form': form,
            'shareform': share_form,
        }
        return render(request, 'social/post_list.html', context)


# View a post in detail
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        # Gets the primary key of the post
        post = Post.objects.get(pk=pk)
        # Gets the comment form
        form = CommentForm()
        # Gets the share form
        share_form = ShareForm()
        # Sorts the comments on a post
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        # Context for use in HTML
        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'shareform': share_form,
        }
        # Redirects to post detail page
        return render(request, 'social/post_detail.html', context)

    # Same as above, but for POST request
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')
        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'social/post_detail.html', context)


# View a profile in detail
class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        # Gets currently viewed profiles primary key
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        # Gets profiles post
        posts = Post.objects.filter(author=user).order_by('-created_on')

        # Gets profiles friends
        friends = profile.friends.all()
        friend_request = profile.friend_request.all()

        # How many friends
        if len(friends) == 0:
            is_friend = False

        # Check if viewed profile and request profile are already friends
        for friend in friends:
            # Are friends
            if friend == request.user:
                is_friend = True
                break
            # Are not friends
            else:
                is_friend = False
        number_of_friends = len(friends)

        # Context for HTML
        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'number_of_friends': number_of_friends,
            'is_friend': is_friend,
            'friend_request': friend_request,
        }
        # Redirects to profile
        return render(request, 'social/profile.html', context)


# Add a friend
class AddFriend(LoginRequiredMixin, View):
    # POST add friend
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.friend_request.add(request.user)
        return redirect('profile', pk=profile.pk)


class AcceptFriend(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # Gets the currently viewed profile
        from_user = UserProfile.objects.get(pk=pk)
        to_user = request.user
        # Adds the request user to friends
        to_user.friends.add(from_user)
        from_user.friends.add(to_user)
        # Redirects to current profile
        return redirect('profile', request.user.pk)


# Remove a friend
class RemoveFriend(LoginRequiredMixin, View):
    # POST remove friend
    def post(self, request, pk, *args, **kwargs):
        # Gets profile currently being viewed
        profile = UserProfile.objects.get(pk=pk)
        # Removes a friend
        profile.friends.remove(request.user)
        # Redirects to current profile
        return redirect('profile', pk=profile.pk)


# View a profiles friends
class ListFriends(View):
    def get(self, request, pk, *args, **kwargs):
        # Gets the profile currently being viewed
        profile = UserProfile.objects.get(pk=pk)
        # Gets profiles friends
        friends = profile.friends.all()
        # Context for HTML
        context = {
            'profile': profile,
            'friends': friends,
        }
        # Redirects to friends list
        return render(request, 'social/friends_list.html', context)


class ListRequest(View):
    def get(self, request, pk, *args, **kwargs):
        # Gets the profile currently being viewed
        profile = UserProfile.objects.get(pk=pk)
        # Gets profiles friends
        friend_request = profile.friend_request.all()
        # Context for HTML
        context = {
            'profile': profile,
            'friend_request': friend_request,
        }
        # Redirects to friends list
        return render(request, 'social/friend_request.html', context)


# Edit a profile
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Gets the profile model
    model = UserProfile
    # Fields that the model contain
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    # Edit profile template
    template_name = 'social/profile_edit.html'

    # If success
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


# Search for a user
class UserSearch(View):
    def get(self, request, *args, **kwargs):
        # Receives a search query entered into textbox
        query = self.request.GET.get('query')
        # List all profiles that matches the query
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
        )
        context = {
            'profile_list': profile_list
        }
        return render(request, 'social/search.html', context)


# Edit a post
class PostEditView(UpdateView):
    # Gets the post model
    model = Post
    # Fields for post model
    fields = ['body']
    # Template for post model
    template_name = 'social/post_edit.html'

    # If success
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})


# Delete a post
class PostDeleteView(DeleteView):
    # Gets the post model
    model = Post
    # Template for deleting post
    template_name = 'social/post_delete.html'
    # Redirects to home if success
    success_url = reverse_lazy('post-list')


# Delete a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # Gets the comment model
    model = Comment
    # Template for deleting comment
    template_name = 'social/comment_delete.html'

    # If success
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class SharedPostView(View):
    def post(self, request, pk, *args, **kwargs):
        original_post = Post.objects.get(pk=pk)
        form = ShareForm(request.POST)
        if form.is_valid():
            new_post = Post(
                shared_body=self.request.POST.get('body'),
                body=original_post.body,
                author=original_post.author,
                created_on=original_post.created_on,
                shared_on=localtime(now()),
                shared_user=request.user
            )
            new_post.save()
        return redirect('post-list')
