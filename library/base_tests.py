import Entity
import Action

a = Entity.Entity()
b = Entity.Entity()

print a.position, b.position

print 'Entities created'
a.perform_action('move', b)
print 'moved'
a.set_target(b)
a.perform_action('converse')

print a.get_nearest_entities()

print a.position, b.position
