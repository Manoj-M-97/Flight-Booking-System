# Flight-Booking-System
This is an interface for flight booking implemented using client and server side networking.
It uses sockets to send data back and forth and manages the concurrency of booking for the same seat by blocking it until the user chooses it or not.
It is interactive as the server reacts to the choice given by the client.
It keeps the connection live until the transaction is done by an user and also manages parallel requests to the server (using threads). 
The connection is established with the unique combination of IP address and port number.

This can be run on two differnt terminals on the same host or terminals on two different hosts.

# To Run:
(To be run on different terminals or on different hosts)
python server.py
Python client.py
