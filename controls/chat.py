# -*- coding: utf-8 -*-
import os
import time
import logging
import datetime
from databases.chat import *
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

enableGetUser = True

class MessageSolver(webapp.RequestHandler):

    def sendMessage(self):
        text = self.request.get('text')
        roomname = self.request.get('room').strip()
        user = users.get_current_user()
        ntuusers = NtuUser.gql("where user = :1" ,user)
        if ntuusers.count() == 0:
            return
        rooms = Room.gql("where name = '" + roomname + "'")
        if rooms.count() == 0:
            return
        ntuuser = ntuusers.get()
        room = rooms.get()
        message = Message()
        message.text = text
        message.room = room
        message.user = ntuuser
        message.time += datetime.timedelta(hours=8)
        message.put()
        cacheName = "roomChat_" + roomname
        memcache.delete(cacheName)

    def getMessage(self):
        roomname = self.request.get('room').strip()
        cacheName = "roomChat_" + roomname
        result = memcache.get(cacheName)
        if result is None:
            result = ''
            rooms = Room.gql("where name = '" + roomname + "'")
            if rooms.count() > 0:
                messages = Message.gql('where room = :1 order by time desc limit 30', rooms.get())
                path = os.path.join(os.path.dirname(__file__), '../templates/chat.html')
                result = template.render(path, {'messages':messages})
                if memcache.set(cacheName, result) == False:
                    logging.error("Can not set cache " + cacheName)
        user = NtuUser.gql("where user = :1" ,users.get_current_user())
        if user.count() > 0:
            user.get().timestamp = int(time.time())
            self.response.out.write(result)

    def post(self, order):
        if order == "send":
            self.sendMessage()
        else:
            self.getMessage()

class RoomSolver(webapp.RequestHandler):

    def getUserList(self):
        if not enableGetUser:
            self.response.out.write('Not enabled.')
            return
        roomname = self.request.get('room').strip()
        cacheName = 'roomUsers_' + roomname
        result = memcache.get(cacheName)
        if result is None:
            obset = Room.gql("where name = '" + roomname + "'")
            if obset.count() > 0:
                result = ''
                ob = obset.get()
                now = int(time.time())
                for ntuuser in ob.ntuuser_set:
                    if now - ntuuser.timestamp <= 120:
                        result += ntuuser.user.nickname() + "\n"
                    else:
                        ntuuser.room = None
                        ntuuser.put()
                if memcache.set(cacheName, result) == False:
                    logging.error('Can not set cache ' + cacheName)
            else:
                result = 'Room not exist.'
        self.response.out.write(result)

    def getNumberOfUser(self):
        if not enableGetUser:
            self.response.out.write('Not enabled.')
            return
        result = ''
        for room in Room.all():
            result += str(room.ntuuser_set.count()) + ' ' + room.name + "\n"
        self.response.out.write(result[:-1])

    def createRoom(self):
        roomname = self.request.get('room').strip()
        if Room.gql("where name = '" + roomname + "'").count() > 0:
            self.response.out.write('Repeated roomname.')
        else:
            newRoom = Room()
            newRoom.name = roomname
            newRoom.put()
            self.response.out.write('AC')

    def joinRoom(self):
        roomname = self.request.get('room').strip()
        #logging.error(roomname)
        rooms = Room.gql("where name = '" + roomname + "'")
        if rooms.count() == 0:
            if Room.all().count() == 0:
                lobby = Room(name='lobby')
                lobby.put()
            else:
                self.response.out.write('Room not exist.')
        user = users.get_current_user()
        ntuusers = NtuUser.gql("where user = :1" ,user)
        if ntuusers.count() == 0:
            ntuuser = NtuUser()
            ntuuser.user = user 
        else:
            ntuuser = ntuusers.get()
            lastroom = ntuuser.room
            if lastroom and lastroom.name != roomname:
                if enableGetUser:
                    cacheName = "roomUsers_" + lastroom.name
                    memcache.delete(cacheName)
                if lastroom.ntuuser_set.count() == 1 and lastroom.name != "lobby":
                    memcache.delete('roomChat_' + lastroom.name)
                    db.delete(Message.gql("where Room = :1" ,lastroom))
                    db.delete(lastroom)

        ntuuser.timestamp = int(time.time())
        ntuuser.room = rooms.get()
        ntuuser.put()
        if enableGetUser:
            cacheName = "roomUsers_" + roomname
            memcache.delete(cacheName)
        self.response.out.write('AC')

    def getRoomList(self):
        result = memcache.get('roomList')
        if result is None:
            result = ''
            for room in Room.all():
                result += room.name + "\n"
        self.response.out.write(result[:-1])

    Mapping = {'getUserList':getUserList,
            'getNumberOfUser':getNumberOfUser,
            'createRoom':createRoom,
            'joinRoom':joinRoom,
            'getRoomList':getRoomList}

    def post(self, order):
        self.Mapping[order](self)


urlList = [('/chat/(get|send)Message', MessageSolver),
        ('/chat/(.*)', RoomSolver)]

application = webapp.WSGIApplication(urlList, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
