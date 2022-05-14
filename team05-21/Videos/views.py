from django.shortcuts import render, redirect


# Create your views here.
def list_videos_page(request):
    if request.user.is_authenticated:
        return render(request, 'Videos/list-videos.html')
    
    return redirect('/login/')


# POST VIDEO PAGE RELATED
def post_video_page(request):
    if request.user.is_authenticated:
        return render(request, 'Videos/post-video.html')

    return redirect('/login/')  # must be done for every one (mixins are hard)


def post_video_form(request):
    print("hi")


def one_video_page(request):
    if request.user.is_authenticated:
        return render(request, 'Videos/one-video.html')
    
    return redirect('/login/')
    
def saved_videos_page(request):
    if request.user.is_authenticated:
        return render(request, 'Videos/list-videos.html')
    
    return redirect('/login/')

