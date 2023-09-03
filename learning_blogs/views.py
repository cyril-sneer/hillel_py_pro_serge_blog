from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string

from .models import Topic, Entry
from .forms import TopicForm, EntryForm, ContactUsForm
from .tasks import contact_us_email


def index(request):
    """Домашняя страница приложения Learning Blog."""
    return render(request, 'learning_blogs/index.html')


@login_required
def topics(request):
    """Выводит список тем."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_blogs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    if not check_topic_owner(topic, request.user):
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_blogs/topic.html', context)


@login_required
def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_blogs:topics')

    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'learning_blogs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)
    if not check_topic_owner(topic, request.user):
        raise Http404

    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.is_published = True
            new_entry.save()
            return redirect('learning_blogs:topic', topic_id=topic_id)

    # Вывести пустую или недействительную форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_blogs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if not check_topic_owner(topic, request.user):
        raise Http404

    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_blogs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_blogs/edit_entry.html', context)


def check_topic_owner(topic: Topic, user):
    return True if topic.owner == user else False


def contact_us(request):
    """Отправляет сообщение администрации сайта"""

    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        cu_form = ContactUsForm()
    else:
        # Отправлены данные POST; обработать данные.
        cu_form = ContactUsForm(data=request.POST)
        if cu_form.is_valid():
            contact_us_email.apply_async(
                kwargs={"subject": cu_form.cleaned_data['user_subject'],
                        "message": cu_form.cleaned_data['user_message'],
                        "from_email": settings.NO_REPLY_EMAIL,
                        "recipient_list": [cu_form.cleaned_data['user_email'], ],
                        },
            )
            return redirect('learning_blogs:index')

        # Вывести пустую или недействительную форму.
    context = {'cu_form': cu_form}
    return render(request, 'learning_blogs/contact_us.html', context)


def save_contact_us_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            pass  # Тут будет вся логика
        else:
            data['form_is_valid'] = False
    content = {'form': form}
    data['html_form'] = render_to_string(template_name, content, request=request)
    return JsonResponse(data)


def contact_us_modal(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
    else:
        form = ContactUsForm()
    return save_contact_us_form(request, form, 'learning_blogs/contact_us_modal.html')
