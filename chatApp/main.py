#!/usr/bin/env python3

# reference: https://www.youtube.com/watch?v=uJC8A_7VZOA

from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "this_is_secret"
socketio = SocketIO(app)

# to keep track of which clients are in each chatroom
# keys = chatrooms, values = list of usernames
clients = {}

# url for the homepage
@app.route("/")
def homepage():
    chatroom_str = ""               # keep track of which chatrooms have been created and have people in them
    for c in clients.keys():        # for each chatroom in the dictionary
        chatroom_str += c + " , "    # add the chatroom followed by a comma to the string
    return render_template("index.html", chatrooms=chatroom_str)   # display index.html as output on the url and pass it the string of created chatrooms

# url for the chatroom page
@app.route("/chatroom")
def chatroom():
    username = request.args.get("username")   # get these from the url after filling in the form on the homepage
    chatroom = request.args.get("chatroom")

    if username and chatroom:   # if username and chatroom are not empty strings
        return render_template("chatroom.html", username=username, chatroom=chatroom)   # display chatroom.html as output on the url and pass it the username and chatroom
    else:
        return redirect("/")   # if username and chatroom are empty strings stay on the homepage

# when a client joins a chatroom
@socketio.on("join_chatroom")
def handle_join_chatroom_event(data):
    app.logger.info("{} has joined chatroom {}".format(data["username"], data["chatroom"]))   # print joined message in terminal
    join_room(data["chatroom"])                                                               # use built in function to have a client join a room
    add_client_to_dict(data["chatroom"], data["username"])                                    # add client's chatroom and username to dictionary
    socketio.emit("joined_chatroom_announcement", data, room=data["chatroom"])                # send a joined chatroom message to all clients in the chatroom
    socketio.emit("show_users", clients[data["chatroom"]], room=data["chatroom"])             # show the current users of the chatroom to all clients in the chatroom

# when a client sends a message
@socketio.on("send_message")
def handle_send_message_event(data):
    app.logger.info("{} has sent message \" {} \" to chatroom {}".format(data["username"], data["message"], data["chatroom"]))   # print message in terminal
    socketio.emit("receive_message", data, room=data["chatroom"])   # show the message to all clients in the chatroom

# when a client leaves a chatroom
@socketio.on("leave_chatroom")
def handle_leave_chatroom_event(data):
    app.logger.info("{} has left chatroom {}".format(data["username"], data["chatroom"]))   # print left message in terminal
    leave_room(data["chatroom"])                                                            # use built in function to have a client leave a room
    remove_client_from_dict(data["chatroom"], data["username"])                             # remove client's chatroom and username from dictionary
    socketio.emit("left_chatroom_announcement", data, room=data["chatroom"])                # send a left chatroom message to all clients in the chatroom
    if data["chatroom"] in clients:                                                         # if there are still clients in the chatroom
        socketio.emit("show_users", clients[data["chatroom"]], room=data["chatroom"])       # show the current users of the chatroom to all clients still in the chatroom

# add a client's chatroom and username to dictionary
def add_client_to_dict(chatroom, username):
    if chatroom not in clients:          # if the chatroom is not a key in the dictionary
        clients[chatroom] = []           # add it and set the value as an empty list
    clients[chatroom].append(username)   # add the client's username to the list of clients in the chatroom

# remove a client's username from dictionary (and the chatroom if it's now empty)
def remove_client_from_dict(chatroom, username):
    clients[chatroom].remove(username)   # remove the client's username from the list of clients in the chatroom
    if clients[chatroom] == []:          # if the chatroom is now empty
        del clients[chatroom]            # delete the chatroom from the dictionary


if __name__ == '__main__':
    socketio.run(app, debug=True)   # listening on 127.0.0.1:5000
