from django.urls import path
from django.views.decorators.cache import cache_page

from core.views import HomeView, ImageDetailView, AddImageView, ImageUpdateView, ImageDeleteView, ImageAddLikeView, \
    AddFollower, RemoveFollower, ListFollowers, PopularImagesListView, AddCommentView, CommentEditUploadView, \
    CommentDeleteView, CommentAddLikeView, NotificationView, AllNotificationHasSeenView, NotificationHasSeenView, \
    ListSubscriptionsView, DeleteFollowerView, SearchResultView, TagSearchResultView

urlpatterns = [
    # path('', cache_page(30)(HomeView.as_view()), name='home'),
    path('', HomeView.as_view(), name='home'),

    #######################################     IMAGES    #############################################################
    path('add-image/', AddImageView.as_view(), name='add_image'),
    # path('user/<slug:slug>/image/<int:pk>', ImageDetailView.as_view(), name='image_detail'),
    path('user/<slug:slug>/image/<int:pk>', ImageDetailView.as_view(), name='image_detail'),
    path('user/<slug:slug>/image/<int:pk>/update', ImageUpdateView.as_view(), name='image_update'),
    path('user/<slug:slug>/image/<int:pk>/delete', ImageDeleteView.as_view(), name='image_delete'),
    path('user/<slug:slug>/image/<int:pk>/add-like', ImageAddLikeView.as_view(), name='image_add_like'),

    #######################################     COMMENTS    ############################################################
    path('user/<slug:slug>/image/<int:pk>/add-comment', AddCommentView.as_view(), name='add_comment'),
    path('comment/<int:pk>/edit', CommentEditUploadView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/add-like', CommentAddLikeView.as_view(), name='comment_add_like'),

    #######################################     FOLLOWERS     #########################################################
    path('user/<slug:slug>/followers/', ListFollowers.as_view(), name='list_followers'),
    path('user/<slug:slug>/followers/add', AddFollower.as_view(), name='add_follower'),
    path('user/<slug:slug>/followers/remove', RemoveFollower.as_view(), name='remove_follower'),
    path('followers/<slug:slug>/delete', DeleteFollowerView.as_view(), name='follower_delete'),

    path('user/<slug:slug>/subscriptions', ListSubscriptionsView.as_view(), name='list_subscriptions'),

    path('popular-images-list', PopularImagesListView.as_view(), name='popular_images_list'),

    #######################################     NOTIFICATIONS    ########################################################
    path('notifications/', NotificationView.as_view(), name='notifications_list'),
    path('notifications-all/has-seen', AllNotificationHasSeenView.as_view(), name='notifications_all_seen'),
    path('notifications-detail/<int:pk>', NotificationHasSeenView.as_view(), name='notifications_detail_seen'),

    #######################################     SEARCH   ###############################################################
    path('search/result', SearchResultView.as_view(), name='search_result'),
    path('tag/<name>/result', TagSearchResultView.as_view(), name='tag_search_result'),

]
