from django.contrib.auth.models import User
from adventure.models import Player, Room, World

Room.objects.all().delete()

w = World()

w.writerooms()
room_array = w.roomreader()
for el in room_array:
  el.save()

players=Player.objects.all()
for p in players:
  p.currentRoom=room_array[0].id
  p.save()