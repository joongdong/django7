import imp
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists!')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password does not exists...')
        context = {}
        return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q')
    if request.GET.get('q') == None:  # 아무 선택이 없을 때는 q=''공백이다.
        q = ''
    rooms = Room.objects.filter(    # 먼저 django.db.models에서 Q를 임포트 해서 사용한다.
        # Q는 찾을 필터를 복수로 지정할 수 있게 한다. |를 붙인다. (or의 뜻)
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    #   이것은 쿼리셋 형식임. queryset = ModelName.objects.all()  object.filter(attribute='value')
    topics = Topic.objects.all()
    # 룸의 갯수를 계산한다. home.html에는 {{room_count}}를 삽입한다.
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm   # 로컬 변수인 form에 RoomForm을 할당한다.
    if request.method == 'POST':   # 요청하는 형태가 POST라면,
        form = RoomForm(request.POST)  # Post data로 부터 instance를 만든다.
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/room_form.html', {'form': form})


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room.name, 'form': form, 'room': room})


# def room(request,pk):
#     # room = None
#     # for i in rooms:
#     #     if i['id']==int(pk):
#     #         room=i
#     #         context={'room':room}
# #render : html로 응답하게 만드는 함수
#     return render(request, 'base/room.html',context)
