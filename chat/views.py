from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from chat import NTRU
import pickle
# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    N = 11
    p = 3
    q = 32

    f = [-1, 1, 1, 0, -1, 0, 1, 0, 0, 1, -1]
    g = [-1, 0, 1, 1, 0, 1, 0, 0, -1, 0, 1]

    D = [0] * (N + 1)
    D[0], D[N] = -1, 1

    encryptor = NTRU.NTRU(N, p, q, f, g)
    encryptor.gen_keys()
    pubkey = encryptor.get_pubkey()

    encmsg, l = NTRU.encrypt(new_message, p, q, D, pubkey)
    d = {1: encmsg, 2: l}
    msg1 = pickle.dumps(d)
    msg1.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):



    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)






    return JsonResponse({"messages":list(messages.values())})