from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView, ListView
from taggit.models import Tag
from common.utils import TitleMixin
from core.forms import ProfileImageForm, CommentForm
from core.models import ProfileImage, Comment, Notification
from django.db.models import Q
from users.models import Profile
import redis
from django.conf import settings


class HomeView(TitleMixin, TemplateView):
    '''Главная страница'''

    template_name = 'core/home.html'
    title = 'Главная страница'


####################################    Image    ################################################################
# class ImageDetailView(DetailView):
#     '''Фотография'''
#
#     model = ProfileImage
#     template_name = 'core/image_detail.html'
#     context_object_name = 'photo'


# Соединение с redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class ImageDetailView(View):

    def get(self, request, slug, pk):
        image = ProfileImage.objects.get(profile__slug=slug, id=pk)

        # увеличить общее число просмотров изображения на 1
        total_views = r.incr(f'image:{image.id}:views')
        return render(request,
                      'core/image_detail.html',
                      {'title': f'Фото от {image.profile.first_name} {image.profile.last_name}',
                       'photo': image,
                       'total_views': total_views})


class AddImageView(TitleMixin, SuccessMessageMixin, CreateView):
    '''Добавить фото'''

    model = ProfileImage
    form_class = ProfileImageForm
    template_name = 'core/add_image.html'
    success_url = reverse_lazy('home')
    success_message = 'Фотография успешно загружена!'
    title = 'Новое фото'

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class ImageUpdateView(SuccessMessageMixin, UpdateView):
    '''Фотография'''

    model = ProfileImage
    form_class = ProfileImageForm
    template_name = 'core/image_update.html'
    success_message = 'Фото успешно отредактировано'

    def get_success_url(self):
        print(self.kwargs)
        return reverse('image_detail', kwargs={'slug': self.kwargs['slug'], 'pk': self.kwargs['pk']})


class ImageDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''Удаление фотографии'''

    model = ProfileImage
    success_message = 'Фотография успешно удалена!'

    def get_success_url(self):
        return reverse('users:profile', kwargs={'slug': self.request.user.profile.slug})


class ImageAddLikeView(LoginRequiredMixin, DetailView):
    '''Лайк к фото'''

    def post(self, request, slug, pk, *args, **kwargs):
        image = ProfileImage.objects.get(profile__slug=slug, pk=pk)
        if request.user not in image.likes.all():
            image.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user,
                                                       to_user=image.profile.user, image=image)
        else:
            image.likes.remove(request.user)

        return redirect('image_detail', slug=image.profile.slug, pk=image.pk)


class PopularImagesListView(ListView):
    model = ProfileImage
    template_name = 'core/popular-images-list.html'
    context_object_name = 'images'
    paginate_by = 10

    def get_queryset(self):
        return ProfileImage.objects.annotate(like_count=Count('likes')).order_by('-like_count')


##########################################     Comment Image   ##################################################
class AddCommentView(LoginRequiredMixin, View):
    '''Добавить комментарий к фото'''

    def post(self, request, slug, pk):
        form = CommentForm(request.POST)
        profile = Profile.objects.get(slug=slug)
        photo = ProfileImage.objects.get(profile=profile, pk=pk)

        if form.is_valid():
            form = form.save(commit=False)
            form.photo = photo
            form.text = request.POST.get('text')
            form.user = request.user
            messages.success(request, 'Ваш комментарий опубликован!')
            form.save()
            notification = Notification.objects.create(notification_type=2, from_user=request.user,
                                                       to_user=profile.user, image=photo)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class CommentEditUploadView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''Редактировать комментарий'''

    model = Comment
    form_class = CommentForm
    template_name = 'core/comment_edit.html'
    success_message = 'Комментарий успешно отредактирован!'

    def get_success_url(self):
        print(self.kwargs)
        return reverse('image_detail', kwargs={'slug': self.object.user.profile.slug, 'pk': self.object.photo_id})


class CommentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''Удалить комментарий'''

    model = Comment
    template_name = 'core/comment_delete.html'
    success_message = 'Комментарий успешно удален!'

    def get_success_url(self):
        print(self.kwargs)
        return reverse('image_detail',
                       kwargs={'slug': self.object.user.profile.slug, 'pk': self.object.photo_id})


class CommentAddLikeView(LoginRequiredMixin, DetailView):
    '''Лайк к комментарию'''

    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        if request.user not in comment.likes.all():
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=5, from_user=request.user,
                                                       to_user=comment.user)

        else:
            comment.likes.remove(request.user)

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


#########################################   Follower   #############################################################################

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        profile = Profile.objects.get(slug=slug)
        profile.followers.add(request.user)
        messages.success(request, f'Вы подписались на пользователя {profile.last_name} {profile.first_name}')
        notification = Notification.objects.create(notification_type=3, from_user=request.user,
                                                   to_user=profile.user)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        profile = Profile.objects.get(slug=slug)
        profile.followers.remove(request.user)
        messages.success(request, f'Вы успешно отписались от пользователя {profile.last_name} {profile.first_name}')
        notification = Notification.objects.create(notification_type=4, from_user=request.user,
                                                   to_user=profile.user)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class DeleteFollowerView(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        profile = Profile.objects.get(slug=slug)
        request.user.profile.followers.remove(profile.user)
        messages.success(request, f'Вы успешно удалили пользователя {profile.last_name} {profile.first_name}')
        notification = Notification.objects.create(notification_type=7, from_user=request.user,
                                                   to_user=profile.user)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class ListFollowers(View):
    ''' Подписчики '''

    def get(self, request, slug, *args, **kwargs):
        profile = Profile.objects.get(slug=slug)
        followers = profile.followers.all()

        context = {
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'core/followers_list.html', context)


class ListSubscriptionsView(View):
    ''' Подписки '''

    def get(self, request, slug):
        profile = Profile.objects.get(slug=slug)
        list_subscriptions = [user for user in User.objects.all() if profile.user in user.profile.followers.all()]
        context = {
            'profile': profile,
            'list_subscriptions': list_subscriptions
        }
        return render(request, 'core/subscriptions_list.html', context)


#########################################    Notification    #####################################################################


class NotificationView(View):
    '''Все уведомления'''

    def get(self, request):
        notifications = Notification.objects.filter(to_user=request.user).exclude(user_has_seen=True).order_by('-date')
        count = notifications.count()
        context = {
            'notifications': notifications, 'count': count
        }
        return render(request, 'core/notifications.html', context)


class NotificationHasSeenView(View):
    '''Сделать уведомление прочитанным'''

    def post(self, request, pk):
        notification = Notification.objects.get(pk=pk)
        notification.user_has_seen = True
        notification.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class AllNotificationHasSeenView(View):
    '''Сделать все уведомления прочитанными'''

    def post(self, request):
        notifications = Notification.objects.filter(to_user=request.user).exclude(user_has_seen=True).order_by(
            '-date')
        if notifications:
            notifications.update(user_has_seen=True)
            messages.success(request, 'Все уведомления успешно удалены!')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


#####################################  SEARCH PEOPLE  ####################################################################

class SearchResultView(TitleMixin, ListView):
    paginate_by = 3
    template_name = 'core/search-result.html'
    title = 'Результаты поиска'

    def get_queryset(self):
        person = self.request.GET.get('person')
        peoples = Profile.objects.filter(
            Q(first_name__icontains=person) | Q(last_name__icontains=person) | Q(user__username__icontains=person)
        )
        return peoples

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['people'] = self.request.GET.get('person')
        return context


#####################################  SEARCH TAG PHOTO  ####################################################################
class TagSearchResultView(View):
    def get(self, request, name):
        tag = get_object_or_404(Tag, slug=name)
        images = ProfileImage.objects.filter(tag__in=[tag])
        # images = ProfileImage.objects.all()
        context = {
            'tag': name,
            'title': f'Результат поиска по тегу {name}',
            'images': images
        }
        return render(request, 'core/tag-search-result.html', context)


############################################   ERRORS    ##########################################################################
def handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(request=request, template_name='errors/error_page.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': 'Страница не найдена',
    })


def handler500(request):
    """
    Обработка ошибки 500
    """
    return render(request=request, template_name='errors/error_page.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message': 'Внутренняя ошибка сайта, вернитесь на главную страницу',
    })


def handler403(request, exception):
    """
    Обработка ошибки 403
    """
    return render(request=request, template_name='errors/error_page.html', status=403, context={
        'title': 'Ошибка доступа: 403',
        'error_message': 'Доступ к этой странице ограничен',
    })
