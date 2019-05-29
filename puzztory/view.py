from django.shortcuts import render
from PuzzModel.models import Fragment, UserExtension, Story
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
import time
import threading


index_dict = {
    'display': 'homepage',
    'story_list': '',
    'user_list': ''
}

# time allocated for user to add fragment: seconds
edit_time = 300


def homepage(request):
    index_dict['display'] = 'homepage'
    index_dict['story_list'] = Story.objects.order_by('-likescount')[:5]
    index_dict['user_list'] = UserExtension.objects.order_by('-experience')[:5]

    # for Pagination
    story_full_list = Story.objects.order_by('-updatetime')
    paginator = Paginator(story_full_list, 10)
    # if request.method == 'GET':
    page = request.GET.get('page', 1)
    # if page == None:
    #     page = 1
    page_obj = paginator.get_page(page)
    index_dict['paginator'] = paginator
    index_dict['page_obj'] = page_obj
    if(paginator.num_pages > 1):
        is_paginated = True
    else:
        is_paginated = False
    index_dict['is_paginated'] = is_paginated
    return render(request, 'index.html', index_dict)


def storypage(request, story_id):
    frag_full_list = Fragment.objects.filter(
        storyid=story_id).order_by('createtime')
    paginator = Paginator(frag_full_list, 7)
    # if request.method == 'GET':
    page = request.GET.get('page', 1)
    # if page is None:
    #     page = 1

    page_obj = paginator.page(page)
    if(paginator.num_pages > 1):
        is_paginated = True
    else:
        is_paginated = False

    scroll_to_frag_id = request.GET.get('scroll_to_frag_id', -1)

    # scroll_to_frag_id == -1 代表不需要片段滚动
    # 否则 scroll_to_frag_id 代表滚动到的片段id号

    story_dict = {
        'story': Story.objects.get(id=story_id),
        'paginator': paginator,
        'page_obj': page_obj,
        'is_paginated': is_paginated,
        'scroll_to_frag_id': scroll_to_frag_id
    }
    return render(request, 'story.html', story_dict)


def upload_story_page(request):
    index_dict['display'] = 'upload_story'
    index_dict['story_list'] = Story.objects.order_by('-likescount')[:5]
    index_dict['user_list'] = UserExtension.objects.order_by('-experience')[:5]
    return render(request, 'index.html', index_dict)


def deletefrag(request, frag_id, story_id, page):
    Fragment.objects.get(id=frag_id).delete()
    story_record = Story.objects.get(id=story_id)
    story_record.fragscount -= 1
    story_record.save()
    frag_full_list = Fragment.objects.filter(
        storyid=story_id).order_by('createtime')
    paginator = Paginator(frag_full_list, 7)
    if paginator.num_pages < page:
        page = paginator.num_pages

    # 置 last_frag_id 为当前页最后一个片段
    last_frag_id = paginator.page(page)[-1].id
    append = str(story_id) + "?page=" + str(page) + \
        "&scroll_to_frag_id=" + str(last_frag_id)
    return HttpResponseRedirect("/story/" + append)


def upload_frag(request, story_id):
    if request.method == 'POST':
        frag_text = request.POST['fcontent']
        frag_record = Fragment(
            content=frag_text, nickname=request.user.userextension.nickname,
            email=request.user.email, storyid=story_id)
        frag_record.save()
        story_record = Story.objects.get(id=story_id)
        story_record.fragscount += 1
        # unlock the story once the fragment is submitted
        # meanwhile refresh attribute editor, remains, updatetime
        story_record.lock = False
        story_record.remains = 0
        # story_record.updatetime = timezone.now
        story_record.updatetime = frag_record.createtime
        story_record.save()
        current_user = UserExtension.objects.get(id=request.user.id)
        current_user.experience += 2
        current_user.save()

    frag_full_list = Fragment.objects.filter(
        storyid=story_id).order_by('createtime')
    paginator = Paginator(frag_full_list, 7)
    # 置 last_frag_id 为当前页最后一个片段
    append = str(story_id) + "?page=" + str(paginator.num_pages) + \
        "&scroll_to_frag_id=" + str(frag_record.id)
    return HttpResponseRedirect("/story/" + append)


def upload_story(request):
    # keys in request.POST:
    # MUST HAVE: title, ffcontent
    # MAY HAVE: branch, modified -> 'on' if checkbox was checked
    # MAY HAVE: fragWordsLimit: the maximum number of words a fragment can have in current story
    # MAY HAVE: fragsCountLimit: the maximum number of fragments a story can have
    if request.method == 'POST':
        story_title = request.POST['title']
        first_frag_text = request.POST['ffcontent']
        frag_record = Fragment(
            content=first_frag_text, nickname=request.user.userextension.nickname,
            email=request.user.email, storyid=0)
        frag_record.save()
        story_record = Story(
            nickname=request.user.userextension.nickname, email=request.user.email,
            editor=request.user.email, title=story_title, ffid=frag_record.id, ffcontent=first_frag_text)

        if 'branch' in request.POST:
            story_record.branch = True
        if 'modified' not in request.POST:
            story_record.modified = False
        if 'fragWordsLimit' in request.POST:
            story_record.fragwordslimit = request.POST['fragWordsLimit']
        if 'fragsCountLimit' in request.POST:
            story_record.fragscountlimit = request.POST['fragsCountLimit']
        story_record.save()
        frag_record.storyid = story_record.id
        frag_record.save()
        current_user = UserExtension.objects.get(id=request.user.id)
        current_user.experience += 10
        current_user.save()

    return HttpResponseRedirect("/")


def system_message(request):
    index_dict['display'] = 'system_message'
    index_dict['story_list'] = Story.objects.order_by('-likescount')[:5]
    index_dict['user_list'] = UserExtension.objects.order_by('-experience')[:5]
    return render(request, 'index.html', index_dict)


def login_page(request):
    login_dict = {
        'emailNotExistedAlert': "",
        'passwordIncorrect': "",
        'useremail': ""
    }
    return render(request, 'login.html', login_dict)


def register_page(request):
    register_dict = {
        'emailExistedAlert': ""
    }
    return render(request, 'register.html', register_dict)


def lfcontent(request):
    request_id = request.GET.get('story_id')
    story = Story.objects.get(id=request_id)
    ret_dict = {}
    last_fragment = Fragment.objects.filter(
        storyid=request_id).order_by('-createtime')[0]
    if len(last_fragment.content) > 20:
        lfcontent_text = '...' + last_fragment.content[-20:]
    else:
        lfcontent_text = last_fragment.content
    ret_dict['lfcontent'] = lfcontent_text
    return JsonResponse(data=ret_dict)


def modifiedset(request):
    request_id = request.GET.get('story_id')
    story = Story.objects.get(id=request_id)
    ret_dict = {}
    ret_dict['lock'] = story.lock

    if not story.lock:
        # 翻转操作
        ret_dict['modified'] = story.modified
        story.modified = not story.modified
        story.save()

    return JsonResponse(data=ret_dict)


def lock(request):
    request_id = request.GET.get('story_id')
    story = Story.objects.get(id=request_id)
    ret_dict = {}
    ret_dict['submittimelimit'] = edit_time

    # if another user request arrives when it's locked
    if story.lock or not story.modified:
        ret_dict['lock'] = True

    # if story is not locked and user request to edit this story
    if not story.lock:
        story.lock = True
        # get ready for countdown
        story.editor = request.user.email
        story.remains = edit_time
        story.save()
        ret_dict['lock'] = False
        ret_dict['submitcountdown'] = story.remains

        last_fragment = Fragment.objects.filter(
            storyid=request_id).order_by('-createtime')[0]
        if len(last_fragment.content) > 20:
            lfcontent_text = '...' + last_fragment.content[-20:]
        else:
            lfcontent_text = last_fragment.content
        ret_dict['lfcontent'] = lfcontent_text

        # a timer thread to release lock after edit_time:seconds
        args = [request_id]
        timer = threading.Timer(1, count_down, args)
        timer.start()
    # if the same user requests for the second time
    elif request.user.email == story.editor:
        ret_dict['lock'] = False
        ret_dict['submitcountdown'] = story.remains

        last_fragment = Fragment.objects.filter(
            storyid=request_id).order_by('-createtime')[0]
        if len(last_fragment.content) > 20:
            lfcontent_text = '...' + last_fragment.content[-20:]
        else:
            lfcontent_text = last_fragment.content
        ret_dict['lfcontent'] = lfcontent_text

    return JsonResponse(data=ret_dict)


def count_down(request_id):
    # if the counting is not over
    story = Story.objects.get(id=request_id)
    if story.remains > 0:
        story.remains -= 1
        story.save()
        # start a new timer ever second
        args = [request_id]
        timer = threading.Timer(1, count_down, args)
        timer.start()
    # now the counting is over, unlock the story
    else:
        story = Story.objects.get(id=request_id)
        if story.lock:
            story.lock = False
        story.save()
