from django.contrib.auth.models import User
from adventure.models import Player, Room, World
import random

Room.objects.all().delete()

w = World(width=10, height=10)

w.writerooms()
room_array = w.roomreader()

for el in room_array:
  el.save()

room_array_2 = Room.objects.all()
w.connect_rooms(room_array_2)

players=Player.objects.all()
for p in players:
  p.currentRoom=room_array[0].id
  p.save()






