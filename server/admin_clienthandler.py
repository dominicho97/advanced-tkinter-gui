import logging
import threading


class ClientHandler(threading.Thread):

    def __init__(self, socketclient):
        threading.Thread.__init__(self)
        self.socket_to_client = socketclient



        

    def run(self):

       


               #CATCH LOGIN client_to_server messge after login from client-side 
   
        io_stream_client = self.socket_to_client.makefile(mode='rw')
        io_stream_client.write("Thank you for connecting!\n")       #newline karakter niet vergeten!
        io_stream_client.flush()
        logging.info("CLH - started & waiting...")
        commando = io_stream_client.readline().rstrip('\n')


        
       
            

        # Catch LOGOUT client_to_server message after logout from client-side 
        my_writer_obj = self.socket_to_client.makefile(mode='r')
        client_logout_message = my_writer_obj.readline().rstrip('\n')
        logging.info(f"{client_logout_message}")
        my_writer_obj.flush()
        
        
        my_writer_obj = self.socket_to_client.makefile(mode='rw')

        name_from_client = my_writer_obj.readline().rstrip('\n')
                
        nickname_from_client = my_writer_obj.readline().rstrip('\n')
        email_from_client = my_writer_obj.readline().rstrip('\n')

        logged_in_client = "Name:"+str(name_from_client) + " Nickname:" + \
                        str(nickname_from_client)+" Email:"+str(email_from_client)
        logging.info(f"Client logged in: {logged_in_client}")
    
        my_writer_obj.flush()
        
 
        while commando != "CLOSE":
            io_stream_client.flush()
         

        logging.debug(f"CLH - Connection closed...")
        self.socket_to_client.close()
