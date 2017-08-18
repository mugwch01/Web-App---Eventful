#My name is Charles Mugwagwa
#This module contains functions that query the DB for the app.
#If main module,this module also tests the database by running queries against the DB.

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *
import time

#x_time = time.time()

#point of connection
engine = create_engine('postgres://ebijkishzoivzm:3f9895248f5db3ada7e76fefcce820c0e605428c3fe194aaef8af57f6f82e394@ec2-54-83-205-71.compute-1.amazonaws.com:5432/d66jtjpm2ktgq9', echo=True)

Session = sessionmaker(bind=engine) #creating session. point of communication with DB
Base = declarative_base() #class and table formats.

#Column(String(50)) -- length of varchar in the DB
class Event(Base):
    __tablename__ = 'events'
    id = Column(String,primary_key=True)
    url = Column(String)
    title = Column(String)
    description = Column(String)
    startTime = Column(String)
    stopTime = Column(String)
    price = Column(String)
    #events = relationship("Event", back_populates="eventsPerformers")
    def __repr__(self):
        return "<Event(id='%s',url='%s',title='%s',description='%s',startTime='%s',stopTime='%s',price='%s')>" % (self.id,self.url,self.title,self.description,self.startTime,self.stopTime,self.price)

class Performer(Base):
    __tablename__ = 'performers'
    id = Column(String,primary_key=True)
    url = Column(String)
    name = Column(String)
    shortBio = Column(String)
    demandMemberCount = Column(String)
    eventCount = Column(String)
    popularity = Column(String)
    #performers = relationship("Performer", back_populates="eventsPerformers")
    def __repr__(self):
        return "<Performer(id='%s',url='%s',name='%s',shortBio='%s',demandMemberCount='%s',eventCount='%s',popularity='%s')>" % (self.id,self.url,self.name,self.shortBio,self.demandMemberCount,self.eventCount,self.popularity)

class EventPerfomer(Base):
    __tablename__ = 'eventsPerformers'
    eventId = Column(String)
    performerId = Column(String)
    __table_args__ = (PrimaryKeyConstraint('eventId', 'performerId'),{},)

    def __repr__(self):
        return "<EventPerfomer(eventId='%s',performerId='%s')>" % (self.eventId,self.performerId)
    
class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, Sequence('comment_seq'), primary_key=True) 
    comment = Column(String)
    def __repr__(self):
        return "Comment id: %s comment: %s" % (self.id,self.comment)  

session = Session() #want to communicate with DB, create subsession
Base.metadata.create_all(engine) #creates tables in the DB if don't exist

def table_size(table_name):
    xy = session.query(table_name).all()
    yz = session.query(table_name).count()
    return yz

def who_is_performing_at_event(title_qry,like = False):
    if like:
        str1 = '%{}%'.format(title_qry)
        result = session.query(Event).filter(Event.title.ilike(str1)).all()
    else:
        result = session.query(Event).filter_by(title=title_qry).all() #one()
    return_lst = []
    for an_event in result:
        performers = session.query(EventPerfomer).filter_by(eventId=an_event.id).all()
        results = []
        for event_performer_x in performers:
            results.append(session.query(Performer).filter_by(id = event_performer_x.performerId).one())
        return_lst.append((an_event,results))
    return return_lst #list of 2-tuples:[(event,list_of_performers)]

def performing_at(name_qry,like=False):
    str1 = '%{}%'.format(name_qry)
    if like:
        the_performers = session.query(Performer).filter(Performer.name.ilike(str1)).all()
    else:
        the_performers = [session.query(Performer).filter_by(name=name_qry).one()]
    return_list = []
    for each_performer in the_performers:
        all_event_performers = session.query(EventPerfomer).filter_by(performerId=each_performer.id).all()
        results = []
        for event_performer_x in all_event_performers:
            results.append(session.query(Event).filter_by(id=event_performer_x.eventId).one())
        return_list.append((each_performer,results))
    return return_list #list of 2-tuples: [(performer,list_of_events)]

def list_all_events():
    return session.query(Event).order_by(Event.startTime).all()

def add_comment(c_string):
    a_comment = Comments(comment=c_string)
    session.add(a_comment)
    session.commit()    
    
def gather_comments():
    return session.query(Comments).all()

def main(fulltest=False):
    print("The tests begin!")
    all_comments = gather_comments()
    for each_com in all_comments:
        print(each_com)
    
    #add_comment("Hello Charly! You've got a decent application here. I would like you to make me web application for my business. What do you say?")    
    
    #all_comments = gather_comments()
    #for each_com in all_comments:
        #print(each_com)    

    #w = list_all_events()    
    #print(len(w))
    #for x in w:
        #print(x.startTime) #proves its sorted

    event_title_qry = " fischer "
    list_of_tuples = who_is_performing_at_event(event_title_qry,True) # --like operator used
    for event1,performers1 in list_of_tuples:
        print(event1,performers1)

    performer_name_qry = 'Cincinnati Bengals'
    output = performing_at(performer_name_qry)
    print(output)
    for r in output:
        print(r)

    performer_name_qry = 'Green'
    output = performing_at(performer_name_qry,True) #list of tuples e.g [(performer,list_of_events)]
    print(output)
    for r in output:
        print(r)

    if fulltest:
        p = session.query(Performer).all()
        for each_p in p:
            performer_name_qry = each_p.name
            a_performer,all_events = performing_at(performer_name_qry)
            print(a_performer,all_events)

        e = session.query(Event).all()
        for each_e in e:
            event_title_qry = each_e.title
            list_of_tuples = who_is_performing_at_event(event_title_qry) #[(event,list_of_performers)]
            for event1,performers1 in list_of_tuples:
                print(event1,performers1)
    t1 = table_size(Event)
    t2 = table_size(Performer)
    t3 = table_size(EventPerfomer)
    print("")
    print("********* Statistics **********")
    if (t1 == 396) and (t2 == 343) and (t3 == 528):
        print("Test passed!  <expected number of rows returned>")
        print("")
    print("Event rows: ",t1)
    print("Performer rows: ",t2)
    print("Event_Performer rows: ",t3)

def list_of_events_and_performers():
    #creating list of event_titles and performer names for searching using the drop down menu
    e_file = open('event_titles.txt','w')
    p_file = open('performer_names.txt','w')
    for each_e in e:
        e_file.write("'"+each_e.title+"',")
    for each_p in p:
        p_file.write("'"+each_p.name+"',")
    e_file.close()
    p_file.close()


if __name__ == '__main__':
    main(fulltest=True)

#y_time = time.time()
#timetaken = int(y_time - x_time)/60
#print("Time taken in mins: ",timetaken)
