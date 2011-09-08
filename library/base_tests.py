import Entity
import Action

a = Entity.Entity()
b = Entity.Entity()

print a.position, b.position

a.set_target(b)
a.perform_action('converse')
#a.perform_action('move', b)
#a.perform_action('converse')

print a.get_nearest_entities()

print a.position, b.position
