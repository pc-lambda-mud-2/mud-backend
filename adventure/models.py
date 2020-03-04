from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import csv

class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)

    def __str__(self):
        return f'Title: {self.title}'

    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()
    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()

class World(models.Model):
    grid = None
    width = 0
    height = 0

    # method to generate rooms
    def writerooms(self, rooms=[]):
        # open the adjectives file. Will be used to create the rooms.
        with open('adjectives.txt', 'r') as f:
            # we read teh file separating each line
            adjectives = f.read().splitlines()
            # we loop through the lines
            for line in adjectives:
                # we append each line to rooms List adding 'room
                rooms.append(f'{line} room')
        
        # we open the room file, that will be used as a table to save info to database
        with open('rooms.csv', 'w', newline='') as csvfile:
            # we need to write in it, separating each column with comma
            testwriter = csv.writer(csvfile, delimiter=',')
            # we loop 100 times (lenght of rooms List)
            for i in range(len(rooms)):
                # first line is the title: name of the room and description
                if i == 0:
                    # we write name and description title
                    testwriter.writerow(['name'] + ['description'])
                else:
                    # we write the name and the description of the room, separated by comma
                    testwriter.writerow([rooms[i]] + [f'It is a very {rooms[i]}'])

    # method to read the rooms csv file and save to a List which we will iterate to save to the database
    def roomreader(self, rooms=[]):
        # open the file
        with open('rooms.csv', newline='') as csvfile:
            # we read it
            roomfile = csv.reader(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # we set line count so we can skip the first line (titles)
            line_count = 0
            # we iterate over the rows of the file
            for row in roomfile:
                # we skip first line - title
                if line_count == 0:
                    line_count += 1
                else:
                    # we create a Room with the info of each row
                    rooms.append(Room(title=row[0], description=row[1]))
        return rooms


