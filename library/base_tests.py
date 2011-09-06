import Entity
import Action

a = Entity.Entity()
b = Entity.Entity()
print 'Entities created'
a.get_target()
target_action = a.get_action()
print 'action got'
a.perform_action(action=target_action)
print 'action done'
print a,b
a.perform_action(action=target_action)
print 'action done'
print a,b
a.perform_action(action=target_action)
print 'action done'
print a,b
print a.print_info()
