
#from sqlalchemy import create_engine
#from sqlalchemy import Column, Integer, String
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import inspect #for inspecting object states
#from sqlalchemy.orm import aliased


#xy = session.query(EventPerfomer).all()
#yz = session.query(EventPerfomer).count()
#print("Events: ",xy)
#print("Events rows: ",yz)


#queries -- causes flashes
#session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()
#session.query(Class).filter_by(attribute='value').first() --first() to get 1 object from the list of results
#our_event_performer = session.query(EventPerfomer).filter_by(eventId='E0-001-099856392-4').first()
#print(our_event_performer)
#print(our_event_performer is test_p) #getting identical objects

#adding multiple objects that have the same class
#session.add_all([
    #User(name='wendy', fullname='Wendy Williams', password='foobar'),
    #User(name='mary', fullname='Mary Contrary', password='xxg527'),
    #User(name='fred', fullname='Fred Flinstone', password='blah')])
    
#updating DB fields
#our_event_performer.eventId = 'newId'

#checking state of the session
#session.dirty, session.new

#commit pending changes - flushes out everything. If had sequence objects, will have seq number after commiting. before -> None. New transaction created after commit()
#session.commit()

#object states: transient, pending, persistent, deleted,detached. 
#Transient - an instance that’s not in a session, and is not saved to the database.
#Pending - when you add() a transient instance, it becomes pending.
#Persistent - An instance which is present in the session and has a record in the database. Get persistent by flushing/query DB for data already existing.
#Deleted - An instance which has been deleted within a flush, but the transaction has not yet completed. If rolled back, deleted to persistent

#checking state of objects
#from sqlalchemy import inspect
#insp = inspect(my_object)
#insp.persistent #boolean. insp.transient,insp.pending,insp.deleted,insp.detached.

#session.rollback()

#Queries:
#session.query(Class.attr,Class.attr).first()
#session.query(Class.attr,Class.attr).one() --raises error if more than one row/no row
#session.query(Class.attr,Class.attr).one_or_none() -- like one(). returns none instead of raising an error
#session.query(Class.attr,Class.attr).all () --returns list
#query(Class.attr).filter(text("id<224")) --from sqlalchemy import text -->USING TEXT!
#session.query(Class).from_statement(text("SELECT * FROM users where name=:name")).params(name='ed').all()
#session.query(Class).order_by(Class.attribute) #like select.specifies columns desired
#session.query(Class.attr,Class.attr) --> get tuple in return
#session.query(Class.attr.label('name_label')).all()
#user_alias = aliased(Class, name='user_alias')
#session.query(Class).order_by(Class.attr)[1:3]
#session.query(Class.attr).filter_by(fullname='Ed Jones') --> uses key words
#session.query(Class.attr).filter(Class.attr=='Ed Jones') #can use python operators = ['==','!=','.ilike('%ed%')','in_()','is_(None)','isnot(None)']
#query.filter(User.name == 'ed', User.fullname == 'Ed Jones') --> AND
#query.filter(or_(User.name == 'ed', User.name == 'wendy')) --from sqlalchemy import or_ --> OR
#query.filter(User.name.match('wendy')) --> MATCH
#query returns query object. can run other queries. e.g 
    #session.query(User).filter(User.name=='ed').filter(User.fullname=='Ed Jones') --> sql AND operator inbetween

#Querying with JOINS
#u, a in session.query(ClassA, ClassB).filter(ClassA.attr==ClassB.attr).filter(ClassB.email_address=='jack@google.com').all()
#session.query(User).join(Address).filter(Address.email_address=='jack@google.com').all() -- returns User type
#query.join(Address, User.id==Address.user_id) --> more explicit
