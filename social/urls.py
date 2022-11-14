from django.urls import path

from .views import PostListView, ProfileView, ProfileEditView, PostDetailView, \
    PostEditView, PostDeleteView, UserSearch, CommentDeleteView, AddLike, SharedPostView, AddFriend, \
    RemoveFriend, ListFriends, AcceptFriend, ListRequest

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),
    path('search/', UserSearch.as_view(), name='profile-search'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/share', SharedPostView.as_view(), name='share-post'),
    path('profile/<int:pk>/friends/add', AddFriend.as_view(), name='add-friend'),
    path('profile/<int:pk>/friends/remove', RemoveFriend.as_view(), name='remove-friend'),
    path('profile/<int:pk>/friends/accept', AcceptFriend.as_view(), name='accept-friend'),
    path('profile/<int:pk>/friends/', ListFriends.as_view(), name='friends-list'),
    path('profile/<int:pk>/friend_request/', ListRequest.as_view(), name='friend-request'),
]