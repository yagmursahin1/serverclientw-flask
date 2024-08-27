This is a client-server architecture that i create with using Flask and threading. 

The video shot on client1 is sent to the server with the post command.
Then, client2 gets this video from the server with the get command.
Converted to byte format using bytesio for video transfer.
At the same time, with the signal sent from client2 by pressing the s key, the servo is printed on the terminal of client1.
