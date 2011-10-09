"""=============================================================================
    Entity.py
    ------------
    Contains the entity class definition.  An entity could be a character, 
    monster, etc. The various attributes affect how the entity interacts
    with the world and other entities.
============================================================================="""
"""=============================================================================

IMPORTS

============================================================================="""
import time

#----------------------------------------
#Vasir Engine Imports
#----------------------------------------
import Entity

#----------------------------------------
#Third Party Imports
#----------------------------------------
import zmq


"""=============================================================================

FUNCTIONS

============================================================================="""
def run_server():
    '''run_server:
    --------------
    Starts up a basic server that will listen for messages (sent from django)
    using ZeroMQ.  When receiving messages, certain things will happen, allowing
    clients to interact with the engine'''

    print 'Server Started!'
    print '-' * 42

    #-------------------------------------------------------------------------
    #REPLY
    #-------------------------------------------------------------------------
    #Get context for ZeroMQ
    context = zmq.Context()
    #Get a socket. Use the REP method of zmq
    socket = context.socket(zmq.REQ)
    #Bind the socket to a port
    socket.connect('tcp://127.0.0.1:5000')

    #-------------------------------------------------------------------------
    #PUB
    #-------------------------------------------------------------------------
    pub_context = zmq.Context()
    socket_pub = pub_context.socket(zmq.PUB)
    socket_pub.bind("tcp://127.0.0.1:5001")

    while True:
        time.sleep(.5)
        socket.send('get_entities')
        msg = socket.recv()

        #Send received message
        socket_pub.send(msg)


"""=============================================================================

INITIALIZE

============================================================================="""
if __name__ == '__main__':
    run_server()
