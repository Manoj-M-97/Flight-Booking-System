# Python program to implement server side of chat room.
import socket
import select
import sys
import random
from thread import *
from copy import deepcopy as dc

 
"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()
 
# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])
 
# takes second argument from command prompt as port number
Port = int(sys.argv[2])
 
"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))
 
"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)


########### GLOBAL DECLARATIONS #############
 
list_of_clients = []
src=["BLR", "LHR", "CPH", "AUH"]
dest=["DXB", "MCI", "DEL", "CDG"]
route=[[569,"BLR", "DXB", 10.15,13.30, "25/11/2017"],[564,"BLR", "DXB", 2.15,7.00, "25/11/2017"], [678,"LHR", "MCI", 10.45,18.15, "26/11/2017"], [361,"CPH", "DEL", 1.30,9.30, "27/11/2017"], [297,"AUH", "CDG", 4.0,11.0, "28/11/2017"]] # [ F_ID, SRC, DEST, Time, Date ]
price=[]	# List of [flight id, economy_price, business_price]
seats=[]	# The list containing (lists of flight numbers and the (list seats available))
all_flights=[]  # Contains the Flight IDs of all flights (To check if the user has inputted the correct value)



for i in route:
	all_flights.append(i[0])

#print all_flights

for a in route:
	l1=[]
	l2=[]
	l3=[]
	for i in range(1, 21):# Initializes the seat availability to 120 for first to all plane IDs
		l1.append(i)
	for i in range(21, 121):
		l3.append(i)
	l2.append(a[0])
	l2.append(l1)
	l2.append(l3)
	seats.append(l2)
	
for a in all_flights :
	l5=[]
	eprice=random.randint(5000, 15000)
	bprice=random.randint(15000, 30000)
	l5.append(a)
	l5.append(eprice)
	l5.append(bprice)
	price.append(l5)

#print seats[len(seats)-1]



count=0;            

list_of_seats=[int (x) for x in range (10, 21)]
 
def clientthread(conn, addr):

    global price
    global count
    global src
    global dest
    global route
    global seats
    global all_flights
 
    # sends a message to the client whose user object is conn
    conn.send("Welcome to the Airline Reservation System")
 
    while True:
            try:
                if (1):               
                    conn.send("Source : ")
                    conn.send("\n")
                    conn.send("  ".join(src))
                    conn.send("\nDestination : ")
                    conn.send("\n")
                    conn.send("  ".join(dest))
                    conn.send("\n")
                    
                    conn.send("\nEnter Source : ")
                    s=str(conn.recv(2048))
                    
                    conn.send("Enter Destination : ")
                    d=str(conn.recv(2048))
                    
                    conn.send("Enter Date as DD/MM/YYYY")
                    date=str(conn.recv(2048))
                    conn.send("\nAvailable Flights\n\n")
                    
                    eco=0
                    bus=0
                    
                    test=0
                    
                    
                    for i in route:
                    	if (s.startswith(i[1]) and d.startswith(i[2]) and date.startswith(i[5])):
                    		test=test+1
                    		index=i[0]
                    		
                    		conn.send(str(i))
                    		for j in price:
                    			if (j[0]==index):
                    				conn.send("\nEconomy Price = "+str(j[1]))
                    				conn.send("\nBusiness Price = "+str(j[2]))
                    		conn.send("\n\n")
                    if (test==0):
                    	conn.send("\n\nSorry, No Flights available for the entered details\nThanks for trying\n")
                    	conn.send("CLOSE")
                    	###########	CLOSE CONNECTION	#########
                    	
                    else:
                    		
		            conn.send("Enter the flight Number to view seats")
		            fid=int(conn.recv(2048))
		            
		            conn.send("Enter the class 0 for ECO and 1 for BUS ")
		            flight_class=int(conn.recv(2048))
		            
		            
		            if (fid in all_flights):
		            	# Retrive seat Matix
		            	
		            	for q in price:
		            		if (q[0]==fid):
		            			eco=q[1]
		            			bus=q[2]
		            	
		            	for i in seats:
		            		if (i[0]==fid):
		            			l=i

				if (flight_class==0):	#Economy Class

				    	conn.send("\nSeat Availability")
				    	conn.send(str(l[2]))
				    	
				    	conn.send("\nEnter the number of seats required ")
				    	
				    	totseats=int(conn.recv(2048))

				    	
				    	if (totseats>len(l[2])):
						conn.send("Requested more seats than available")
				    		
				    	else :
				    	
					    	dummy=[]
					    	success=1
					    	k=0
					    	avseats=l[2]
					    	conn.send("\nPress 0 anytime to cancel the booking\n")
					    	while (k<totseats):
					    		
					    		conn.send("\nEnter the seat number "+str(k+1))
						    	sno=int(conn.recv(2048))  # Seat Number
						    	
						    	
						    	if (sno in avseats):
						    		avseats.remove(sno)
						    		dummy.append(sno)
						    		k=k+1
						    		continue
						    		
						    	elif (sno==0):
						    		success=0
						    		avseats=l[2]+dummy
						    		conn.send("\nThe Connection is terminated")
						    		conn.send("CLOSE")
						    		break
						    		
						    	elif (sno not in avseats):
						    		conn.send("Seat not Available")
						    		continue
						    		
						print "Client Address is "+addr[0]
						print "Seat Availablity After Reserving"
						print l[2]
					
					
				elif (flight_class==1):	#Business Class
				    		
				    	conn.send("\nSeat Availability")
				    	conn.send(str(l[1]))
				    	
					while (1):	
				    		conn.send("\nEnter the number of seats required ")
					    	
				    		totseats=int(conn.recv(2048))
						print(totseats)
				    		print(len(l[1]))
						    	
				    		if (totseats>len(l[1])):
							conn.send("Requested more seats than available")
							continue
					    		
				    		else :
				   		
						    	dummy=[]
						    	success=1
						    	k=0
						    	avseats=l[1]
						    	conn.send("\nAnytime press 0 to terminate\n")
						    	while (k<totseats):
							    		
						    		conn.send("\nEnter the seat number "+str(k+1))
							    	sno=int(conn.recv(2048))  # Seat Number
							    		
							    	
							    	if (sno in avseats):
							    		print "Inside if"
							    		avseats.remove(sno)
							    		dummy.append(sno)
							    		k=k+1
							    		continue
								    		
							    	elif (sno==0):
							    		print "Inside elif"
							    		success=0
							    		avseats=l[1]+dummy
							    		conn.send("\nThe Connection is terminated")
							    		conn.send("CLOSE")
							    		break
								    		
							    	elif (sno not in avseats):
							    		conn.send("Seat not Available")
							    		continue
								    		
							print "Client Address is "+addr[0]
							print "Seat Availablity After Reserving"
							print l[1]
						break	
		
			
				if (flight_class==0):
					conn.send("\nTotal price (eco class) = "+ str(totseats*eco))
				elif (flight_class==1):
					conn.send("\nTotal price (bus class) = "+str(totseats*bus))

			
		        
		        
		            	conn.send("\nEnter your Personal Information:")
				conn.send("\nName:")
				name=conn.recv(1024)
				conn.send("\nPhone No:")
				ph_no=conn.recv(100)
				conn.send("\nEmail:")
				email=conn.recv(120)

				conn.send("------------Booking Confirmed-------------")
				conn.send("\nName: "+str(name))
				conn.send("\nPhone No: "+str(ph_no))	
				conn.send("\nEmail: "+str(email))
				conn.send("\nSource: "+s)
				conn.send("\nDestination: "+d)
				conn.send("\nDate: "+str(date))
				conn.send("\nFlight No: "+str(fid))
				conn.send("\nSeats: "+str(dummy))	
				conn.send("\n----------------------------------------")	
			        conn.send("CLOSE")
				
		break	
    
                    
                
 
            except:
                continue
 

while True:
 
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept()
 
    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)
 
    # prints the address of the user that just connected
    print addr[0] + " connected"
 
    # creates an individual thread for every user that connects
    start_new_thread(clientthread,(conn,addr))    
    count=count+1
 
conn.close()
server.close()
