import imp
from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]

def home(request):
    q = request.GET.get('q') 
    if request.GET.get('q') == None:
        q =''
    rooms = Room.objects.filter(topic__name__icontains=q)   # 이것은 쿼리셋 형식임. queryset = ModelName.objects.all()  object.filter(attribute='value')
    topics = Topic.objects.all()
    context = {'rooms' : rooms, 'topics':topics}
    return render(request, 'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room' : room}
    return render(request, 'base/room.html',context)


def createRoom(request):
    form = RoomForm   # 로컬 변수인 form에 RoomForm을 할당한다. 
    if request.method =='POST':   # 요청하는 형태가 POST라면, 
        form = RoomForm(request.POST) # Post data로 부터 instance를 만든다. 
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/room_form.html', {'form':form})

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method =='POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
           form.save()
           return redirect('home')
    context = {'form' : form}
    return render(request, 'base/room_form.html',context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj': room.name,'form':form, 'room' : room})




# def room(request,pk):
#     # room = None
#     # for i in rooms:
#     #     if i['id']==int(pk):
#     #         room=i
#     #         context={'room':room}
# #render : html로 응답하게 만드는 함수 
#     return render(request, 'base/room.html',context)
