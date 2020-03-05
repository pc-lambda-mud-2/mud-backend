from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import csv
import random

class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    # def __str__(self):
    #     return f'Title: {self.title}'

    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        print(destinationRoomID, direction, "<<< in connectrooms method, next room id")
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
            print(destinationRoom, "<<<<< inside the try")
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
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    # method to generate rooms
    def writerooms(self, rooms=[]):
        # open the adjectives file. Will be used to create the rooms.
        with open('adjectives.txt', 'r') as f:
            # we read teh file separating each line
            adjectives = f.read().splitlines()
            # we loop through the lines
            for line in range((self.width * self.height) + 1):
                # we append each line to rooms List adding 'room
                rooms.append(f'{adjectives[line]} room')
        
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
        x = 0
        x_max = self.width
        y = self.height -1
        room_id = 1
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
                    rooms.append(Room(id=room_id, title=row[0], description=row[1], x=x, y=y))
                    room_id += 1
                    x += 1
                    if x == x_max:
                        x = 0
                        y -= 1
        return rooms

    def connect_rooms(self, grid):
        # array where we store the rooms
        array_rooms = []
        # we set the available directions for each case scenario

        # first rom - direction cannot be north
        directions = {
            "usual": ['n', 'e', 's', 'w'],
            "first_row_and_first_column": ['e', 's'],
            "first_row": ['e', 's', 'w'],
            "first_row_and_last_column": ['s', 'w'],
            "first_column": ['n', 'e', 's'],
            "last_column": ['n', 's', 'w'],
            "last_row_and_first_column": ['n', 'e'],
            "last_row": ['n', 'e', 'w'],
            "last_row_and_last_column": ['n', 'w'],            
        }

        opposites = {
            "n": "s",
            "s": "n",
            "e": "w",
            "w": "e"
        }


        # we iterate over rows
        for index, room in enumerate(grid):
            to_the_north = index - self.width
            to_the_east = index + 1
            to_the_south = index + self.width
            to_the_west = index - 1

            print(room.title, room.x, room.y, "<<<<<<")


            # if first row,
            if room.y == 5:
                if room.x == 0: # first row first column
                    random_index = random.randrange(0, len(directions["first_row_and_first_column"]))
                    direction_to_be_set = directions["first_row_and_first_column"][random_index]
                    # e_to
                    if direction_to_be_set == 'e':
                        room.connectRooms(grid[to_the_east], direction_to_be_set)
                        grid[to_the_east].connectRooms(room, opposites[direction_to_be_set])
                    # s_to
                    else:
                        room.connectRooms(grid[to_the_south], direction_to_be_set)
                        grid[to_the_south].connectRooms(room, opposites[direction_to_be_set])

                elif room.x == 5:
                    random_index = random.randrange(0, len(directions["first_row_and_last_column"]))
                    direction_to_be_set = directions["first_row_and_last_column"][random_index]
                    # w_to
                    if direction_to_be_set == 'w':
                        room.connectRooms(grid[to_the_west], direction_to_be_set)
                        grid[to_the_west].connectRooms(room, opposites[direction_to_be_set])
                    # s_to
                    else:
                        room.connectRooms(grid[to_the_south], direction_to_be_set)
                        grid[to_the_south].connectRooms(room, opposites[direction_to_be_set])
                else:
                    random_index = random.randrange(0, len(directions["first_row"]))
                    direction_to_be_set = directions["first_row"][random_index]
                    # w_to
                    if direction_to_be_set == 'w':
                        room.connectRooms(grid[to_the_west], direction_to_be_set)
                        grid[to_the_west].connectRooms(room, opposites[direction_to_be_set])
                    # e_to
                    elif direction_to_be_set == 'e':
                        room.connectRooms(grid[to_the_east], direction_to_be_set)
                        grid[to_the_east].connectRooms(room, opposites[direction_to_be_set])
                    # s_to
                    else:
                        room.connectRooms(grid[to_the_south], direction_to_be_set)
                        grid[to_the_south].connectRooms(room, opposites[direction_to_be_set])
            # if last row
            elif room.y == 0:
                if room.x == 0: # first row last column
                    random_index = random.randrange(0, len(directions["last_row_and_first_column"]))
                    direction_to_be_set = directions["last_row_and_first_column"][random_index]
                    # e_to
                    if direction_to_be_set == 'e':
                        room.connectRooms(grid[to_the_east], direction_to_be_set)
                        grid[to_the_east].connectRooms(room, opposites[direction_to_be_set])
                    # n_to
                    else:
                        room.connectRooms(grid[to_the_north], direction_to_be_set)
                        grid[to_the_north].connectRooms(room, opposites[direction_to_be_set])

                elif room.x == 5:
                    random_index = random.randrange(0, len(directions["last_row_and_last_column"]))
                    direction_to_be_set = directions["last_row_and_last_column"][random_index]
                    # w_to
                    if direction_to_be_set == 'w':
                        room.connectRooms(grid[to_the_west], direction_to_be_set)
                        grid[to_the_west].connectRooms(room, opposites[direction_to_be_set])
                    # n_to
                    else:
                        room.connectRooms(grid[to_the_north], direction_to_be_set)
                        grid[to_the_north].connectRooms(room, opposites[direction_to_be_set])
                   
                else:
                    random_index = random.randrange(0, len(directions["last_row"]))
                    direction_to_be_set = directions["last_row"][random_index]
                    # w_to
                    if direction_to_be_set == 'w':
                        room.connectRooms(grid[to_the_west], direction_to_be_set)
                        grid[to_the_west].connectRooms(room, opposites[direction_to_be_set])
                    # e_to
                    elif direction_to_be_set == 'e':
                        room.connectRooms(grid[to_the_east], direction_to_be_set)
                        grid[to_the_east].connectRooms(room, opposites[direction_to_be_set])
                    # n_to
                    else:
                        room.connectRooms(grid[to_the_north], direction_to_be_set)
                        grid[to_the_north].connectRooms(room, opposites[direction_to_be_set])

            # if middle rows
            else:
                if room.x == 0: # middle rows first column
                    random_index = random.randrange(0, len(directions["first_column"]))
                    direction_to_be_set = directions["first_column"][random_index]
                    # e_to
                    if direction_to_be_set == 'e':
                        room.connectRooms(grid[to_the_east], direction_to_be_set)
                        grid[to_the_east].connectRooms(room, opposites[direction_to_be_set])
                    # s_to
                    elif direction_to_be_set == 's':
                        room.connectRooms(grid[to_the_south], direction_to_be_set)
                        grid[to_the_south].connectRooms(room, opposites[direction_to_be_set])
                    # n_to
                    else:
                        room.connectRooms(grid[to_the_north], direction_to_be_set)
                        grid[to_the_north].connectRooms(room, opposites[direction_to_be_set])

                elif room.x == 5:
                    random_index = random.randrange(0, len(directions["last_column"]))
                    direction_to_be_set = directions["last_column"][random_index]
                    # w_to
                    if direction_to_be_set == 'w':
                        room.connectRooms(grid[to_the_west], direction_to_be_set)
                        grid[to_the_west].connectRooms(room, opposites[direction_to_be_set])
                    # s_to
                    elif direction_to_be_set == 's':
                        room.connectRooms(grid[to_the_south], direction_to_be_set)
                        grid[to_the_south].connectRooms(room, opposites[direction_to_be_set])
                    # n_to
                    else:
                        room.connectRooms(grid[to_the_north], direction_to_be_set)
                        grid[to_the_north].connectRooms(room, opposites[direction_to_be_set])
                   
##
                else:
                    random_index = random.randrange(0, len(directions["usual"]))
                    direction_to_be_set = directions["usual"][random_index]
                    # w_to
                    if direction_to_be_set == 'w':
                        room.connectRooms(grid[to_the_west], direction_to_be_set)
                        grid[to_the_west].connectRooms(room, opposites[direction_to_be_set])
                    # e_to
                    elif direction_to_be_set == 'e':
                        room.connectRooms(grid[to_the_east], direction_to_be_set)
                        grid[to_the_east].connectRooms(room, opposites[direction_to_be_set])
                    # s_to
                    elif direction_to_be_set == 's':
                        room.connectRooms(grid[to_the_south], direction_to_be_set)
                        grid[to_the_south].connectRooms(room, opposites[direction_to_be_set])
                    # n_to
                    else:
                        room.connectRooms(grid[to_the_north], direction_to_be_set)
                        grid[to_the_north].connectRooms(room, opposites[direction_to_be_set])

            array_rooms.append(room)
        
        return grid
                

            # if first column

                # set available directions

            # if last column

                # set available directions

            # else

                # set available directions

        # if last row,

            # if first column

                # set available directions

            # if last column

                # set available directions

            # else

                # set available directions

        # else

            # set available directions


