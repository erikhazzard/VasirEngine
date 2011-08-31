import Entity
import Action

a = Entity.Entity()
b = Entity.Entity()
print 'Entities created'
target_action = Action.Action.get_action(a,b)
print 'action got'
target_action.perform_action()
print 'action done'
print a,b
target_action.perform_action()
print 'action done'
print a,b
target_action.perform_action()
print 'action done'
print a,b
