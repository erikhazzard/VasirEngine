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
import random

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
    socket = context.socket(zmq.REP)
    #Bind the socket to a port
    socket.bind('tcp://127.0.0.1:5000')

    #-------------------------------------------------------------------------
    #PUBLISH (Broadcast game state on port 5001)
    #-------------------------------------------------------------------------
    pub_context = zmq.Context()
    socket_pub = pub_context.socket(zmq.PUB)
    socket_pub.bind("tcp://127.0.0.1:5001")
    
    #-------------------------------------------------------------------------
    #Poller
    #-------------------------------------------------------------------------
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    poller.register(socket_pub, zmq.POLLOUT)

    #-------------------------------------------------------------------------
    #Create a broadcast_message_timer counter to limit broadcast timings
    #-------------------------------------------------------------------------
    broad_cast_message_timer = 0

    #-------------------------------------------------------------------------
    #Create a game_loop_counter to limit game loop stuff
    #-------------------------------------------------------------------------
    game_loop_counter = 0

    #-------------------------------------------------------------------------
    #
    #Game AND ZMQ Server Loop
    #
    #-------------------------------------------------------------------------
    while True:
        #Get all available sockets from the poller
        socks = dict(poller.poll(1))

        #-------------------------------------------------------------------------
        #Increment counters 
        #-------------------------------------------------------------------------
        broad_cast_message_timer += 1
        game_loop_counter += 1

        #-------------------------------------------------------------------------
        #
        #Game Loop
        #
        #Execute the game loop
        #-------------------------------------------------------------------------
        if game_loop_counter > 10000:
            #Reset timer
            game_loop_counter = 0

            #Randomly move entities
            if len(Entity.Entity._entities) > 0:
                for entity in Entity.Entity._entities:
                    cur_entity = Entity.Entity._entities[entity]
                    cur_entity.perform_action(
                        action='move',
                        target=[
                            cur_entity.position[0] + random.randint(-1,1),
                            cur_entity.position[0] + random.randint(-1,1),
                            0,
                        ]
                    )

        #-------------------------------------------------------------------------
        #
        #BROADCAST socket
        #
        #Broadcasts the current game state at certain intervals
        #-------------------------------------------------------------------------
        if socket_pub in socks and socks[socket_pub] == zmq.POLLOUT:
            #Only send messages at specific intervals
            if broad_cast_message_timer >= 10000:
                #Reset timer
                broad_cast_message_timer = 0

                #Get all entities
                entities = Entity.Entity._entities

                #Create an array which we'll use to get all the entities and
                #   stuff in JSON text
                entities_json = []

                for entity in entities:
                    #Get the current JSON, but remove the first and trailing ( )'s
                    #   Because we'll want to return a list, not an individual
                    #   object
                    entities_json.append( entities[entity].get_info_json()[1:-1] )

                entities_json = ','.join(entities_json)
        
                #Send the entity info
                socket_pub.send('([%s])' % (entities_json) )

        #-------------------------------------------------------------------------
        #
        #REPLY socket
        #
        #Returns certain states or performs actions to the game based on messages
        #-------------------------------------------------------------------------
        if socket in socks and socks[socket] == zmq.POLLIN:
            msg = socket.recv()
            #When the socket receives a message, get it
            #msg = socket.recv()
            #Print the message
            print 'Received Message: %s' % (msg)

            #---------------------------------------------------------------------
            #
            #Perform actions based on message
            #
            #---------------------------------------------------------------------  
            #--------------------------------
            #Create Entity
            #--------------------------------
            if msg == 'create_entity':
                #Create a new entity and return its ID (We don't need to
                #   save the context or reference to it because it's handled
                #   through the class for us)
                temp_entity = Entity.Entity()

                print 'Created entity'
                
                #Send the message with the entity ID
                socket.send("({'entity_id': '%s'})" % (temp_entity.id))
            #--------------------------------
            #Get Entity Info
            #--------------------------------
            elif 'get_info_' in msg:
                #The msg will look like 'get_info_entityXYZ', so grab the entity
                #   by looking at the Class' _entities dict and the key is just
                #   the message with 'get_info_' replaced with '' so it would only
                #   contain the entity ID
                entity_id = msg.replace('get_info_', '')
                temp_entity = Entity.Entity._entities[entity_id]

                print 'Got entity info: %s' % (entity_id)

                #Send the entity info
                socket.send('%s' % (temp_entity.get_info_json()) )

            #--------------------------------
            #Get ALL entities
            #--------------------------------
            elif 'get_entities' in msg:
                #Get all entities
                entities = Entity.Entity._entities

                print 'Retrieved all %s entities' % (len(entities))

                #Create an array which we'll use to get all the entities and
                #   stuff in JSON text
                entities_json = []

                for entity in entities:
                    #Get the current JSON, but remove the first and trailing ( )'s
                    #   Because we'll want to return a list, not an individual
                    #   object
                    entities_json.append( entities[entity].get_info_json()[1:-1] )

                entities_json = ','.join(entities_json)
        
                #Send the entity info
                socket.send('([%s])' % (entities_json) )

            #--------------------------------
            #Get Game State
            #--------------------------------
            elif 'get_game_state' in msg:
                #Get all entities
                entities = Entity.Entity._entities

                if 'suppress_log' not in msg:
                    print 'Retrieved all %s entities' % (len(entities))

                #Create an array which we'll use to get all the entities and
                #   stuff in JSON text
                entities_json = []

                for entity in entities:
                    #Get the current JSON, but remove the first and trailing ( )'s
                    #   Because we'll want to return a list, not an individual
                    #   object
                    entities_json.append( entities[entity].get_info_json()[1:-1] )

                entities_json = ','.join(entities_json)
        
                #Send the entity info
                socket.send('([%s])' % (entities_json) )

            #--------------------------------
            #Set target entity
            #--------------------------------
            elif 'set_target' in msg:
                #Get all entities
                entities = Entity.Entity._entities

                entity_ids = msg.replace('set_target_', '').split(',')
                Entity.Entity._entities[entity_ids[0]].set_target(
                    target=entity_ids[1])

                print 'Setting target'
        
                #Send the entity info
                socket.send('("%s set target to %s")' % (
                    entity_ids[0], entity_ids[1]))

            #--------------------------------
            #converse
            #--------------------------------
            elif 'converse' in msg:
                #Get all entities
                entities = Entity.Entity._entities

                entity_id = msg.replace('converse_', '')
                print Entity.Entity._entities[entity_id].target
                if Entity.Entity._entities[entity_id].target is not None:
                    Entity.Entity._entities[entity_id].perform_action(
                        'converse') 

                    print 'Conversation performed'
        
                    #Send the entity info
                    socket.send('("conversation action performed")')
                else:
                    socket.send('{"error": "No target provided"}')

"""=============================================================================

INITIALIZE

============================================================================="""
if __name__ == '__main__':
    run_server()
