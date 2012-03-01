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
import threading
import random

#----------------------------------------
#Vasir Engine Imports
#----------------------------------------
import Entity

#----------------------------------------
#Third Party Imports
#----------------------------------------
#Note: ZeroMQ is used to receive messages from Django for requests to modify
#   game state, redis is used to put game state updates to node (via
#   publish / subscribe)
import zmq
import redis


"""=============================================================================

FUNCTIONS

============================================================================="""
class Server(threading.Thread): 
    '''Server:
    --------------
    This extends the Thread class so we can run the game loop in a non
    blocking manner.  The run() method is the primary method - it runs the game
    loop and uses zeromq polling to listen / send messages (to Django in this
    case - the client sends and gets messages through django)
    '''
    def __init__(self):
        '''When this class is instaniated, we'll set up the redis client,
        ZeroMQ, and any other pre-loop configurations we need to do'''
        #-----------------------------------------------------------------------
        #Redis
        #-----------------------------------------------------------------------
        self.client = redis.StrictRedis(
            host='localhost',
        )

        #-----------------------------------------------------------------------
        #REPLY
        #-----------------------------------------------------------------------
        #Get context for ZeroMQ
        self.context = zmq.Context()
        #Get a socket. Use the REP method of zmq
        self.socket = self.context.socket(zmq.REP)
        #Bind the socket to a port
        self.socket.bind('tcp://127.0.0.1:5000')

        #-----------------------------------------------------------------------
        #Poller
        #-----------------------------------------------------------------------
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)


    def run(self):
        '''Starts up a basic server that will listen for messages (sent from 
        django) using ZeroMQ.  When receiving messages, certain things will 
        happen, allowing clients to interact with the engine.
        
        This run function will execute then call itself (after some delay) to
        continually run'''

        #Get all available sockets from this object's poller
        socks = dict(self.poller.poll(1))

        #-----------------------------------------------------------------------
        #
        #Game Loop
        #
        #-----------------------------------------------------------------------
        #Randomly move entities
        if len(Entity.Entity._entities) > 0:
            for entity in Entity.Entity._entities:
                cur_entity = Entity.Entity._entities[entity]
                #set x and y 
                move_x = cur_entity.position[0] + random.randint(-1,1)
                if move_x < 0:
                    move_x = move_x * -1
                move_y = cur_entity.position[0] + random.randint(-1,1)
                if move_y < 0:
                    move_y = move_y * -1

                cur_entity.perform_action(
                    action='move',
                    target=[
                        move_x,
                        move_y,
                        0,
                    ]
                )
        #-----------------------------------------------------------------------
        #
        #Publish key updates to redis
        #   Publish latest game state
        #
        #-----------------------------------------------------------------------
             
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
        self.client.publish(
            'game_state:world',
            '([%s])' % (entities_json),
        )

        #-----------------------------------------------------------------------
        #
        #REPLY socket
        #
        #Returns certain states or perform actions to the game based on messages
        #-----------------------------------------------------------------------
        if self.socket in socks and socks[self.socket] == zmq.POLLIN:
            msg = self.socket.recv()
            #When the socket receives a message, get it
            #msg = socket.recv()
            #Print the message
            print 'Received Message: %s' % (msg)

            #-------------------------------------------------------------------
            #
            #Perform actions based on message
            #
            #------------------------------------------------------------------- 
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
                self.socket.send("({'entity_id': '%s'})" % (temp_entity.id))
            #--------------------------------
            #Get Entity Info
            #--------------------------------
            elif 'get_info_' in msg:
                #The msg will look like 'get_info_entityXYZ', so grab the entity
                #   by looking at the Class' _entities dict and the key is just
                #   the message with 'get_info_' replaced with '' so it would 
                # only contain the entity ID
                entity_id = msg.replace('get_info_', '')
                try:
                    temp_entity = Entity.Entity._entities[entity_id]

                    print 'Got entity info: %s' % (entity_id)

                    #Send the entity info
                    self.socket.send('%s' % (temp_entity.get_info_json()) )
                except KeyError:
                    print 'Invalid entity passed in'
                    self.socket.send('{}')

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
                self.socket.send('([%s])' % (entities_json) )

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
                self.socket.send('([%s])' % (entities_json) )

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
                self.socket.send('("%s set target to %s")' % (
                    entity_ids[0], entity_ids[1]))

            #--------------------------------
            #converse
            #--------------------------------
            elif 'converse' in msg:
                #Get all entities
                entities = Entity.Entity._entities

                entity_id = msg.replace('converse_', '')
                if Entity.Entity._entities[entity_id].target is not None:
                    Entity.Entity._entities[entity_id].perform_action(
                        'converse') 

                    print 'Conversation performed'
        
                    #Send the entity info
                    self.socket.send('("conversation action performed")')
                else:
                    self.socket.send('{"error": "No target provided"}')

        #--------------------------------
        #Delay execution
        #--------------------------------
        time.sleep(.08)

        #--------------------------------
        #Call itself to it continually executes
        #--------------------------------
        self.run()

"""=============================================================================

INITIALIZE

============================================================================="""
if __name__ == '__main__':
    #Create a server object and run it
    game_server = Server()
    game_server.run()
