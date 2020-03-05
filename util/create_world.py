from django.contrib.auth.models import User
from adventure.models import Player, Room, World
import random

Room.objects.all().delete()

w = World(width=5, height=5)

w.writerooms()
room_array = w.roomreader()
# all_rooms = Room.objects.all()
for el in room_array:
  el.save()

room_array_2 = Room.objects.all()
w.connect_rooms(room_array_2)

# new_grid = w.connect_rooms(room_array_2)
# for el in new_grid:
#   el.save()


players=Player.objects.all()
for p in players:
  p.currentRoom=room_array[0].id
  p.save()
# numbers = []

# world = Room.objects.all()
# for el in world:
#   numbers.append(el.id)

# length_num = len(numbers)
# rand_num = random.randrange(0, length_num)

# for room in world:






