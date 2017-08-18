#My name is Charles Mugwagwa.
#This module parses the data and creates the tables using SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *
from xml.dom import minidom
import time

x_time = time.time()

#===============================================================================
#creating DB tables
#===============================================================================

#point of connection
engine = create_engine('postgres://ebijkishzoivzm:3f9895248f5db3ada7e76fefcce820c0e605428c3fe194aaef8af57f6f82e394@ec2-54-83-205-71.compute-1.amazonaws.com:5432/d66jtjpm2ktgq9', echo=True)

#creating session. point of communication with DB
Session = sessionmaker(bind=engine)

#class and table formats.
Base = declarative_base()

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
        return "<Event(id='%s',title='%s',startTime='%s')>" % (self.id,self.title,self.startTime)

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
        return "<Performer(id='%s',name='%s')>" % (self.id,self.name)

class EventPerfomer(Base):
    __tablename__ = 'eventsPerformers'
    eventId = Column(String,ForeignKey('events.id'))
    performerId = Column(String,ForeignKey('performers.id'))
    __table_args__ = (PrimaryKeyConstraint('eventId', 'performerId'),{},)   
    
    def __repr__(self):
        return "<EventPerfomer(eventId='%s',performerId='%s')>" % (self.eventId,self.performerId)
    
class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, Sequence('comment_seq'), primary_key=True) 
    comment = Column(String)
    def __repr__(self):
        return "Comment id: %s comment: %s" % (self.id,self.comment)  
    
    
#deleting all the tables
Base.metadata.drop_all(engine)

#creates tables in the DB if don't exist
Base.metadata.create_all(engine)

#creating subSession to interact with DB
session = Session()

#===============================================================================
#parsing data and populating the DB 
#===============================================================================

xmldoc = minidom.parse('app_data.xml')

recent_combinations = []
relevant_performers = []
number_of_events = 0

events_ls = xmldoc.getElementsByTagName('event')
for event in events_ls:    
    #creating combinations of performerid to eventid & populating events table.
    include_event = False    
    perf_list = event.getElementsByTagName('performer')    
    if perf_list != []:
        for one_perf in perf_list:            
            perf_id_list = one_perf.getElementsByTagName('id')        
            condition = False
            for xyz in one_perf.getElementsByTagName('url'):
                condition = True
                break
            if not condition:
                #print(event.getElementsByTagName('id')[0].firstChild.data,perf_id_list[0].firstChild.data)
                recent_combinations.append((event.getElementsByTagName('id')[0].firstChild.data,perf_id_list[0].firstChild.data))
                if (perf_id_list[0].firstChild.data) not in relevant_performers:
                    relevant_performers.append(perf_id_list[0].firstChild.data)
                include_event = True
            
    #processing events with performers
    if include_event:   
        number_of_events += 1
        idnt1 = event.getElementsByTagName('id')[0].firstChild.data
        if (event.getElementsByTagName('url')[0].firstChild) != None:
            url1 = event.getElementsByTagName('url')[0].firstChild.data
        else:
            url1 = "None"
        if (event.getElementsByTagName('title')[0].firstChild) != None:
            title1 = event.getElementsByTagName('title')[0].firstChild.data
        else:
            title1 = "None"
        if (event.getElementsByTagName('description')[0].firstChild) != None:
            description1 = event.getElementsByTagName('description')[0].firstChild.data
        else:
            description1 = "None"
        if (event.getElementsByTagName('start_time')[0].firstChild) != None:
            start_time1 = event.getElementsByTagName('start_time')[0].firstChild.data
        else: start_time1 = "None"
        if (event.getElementsByTagName('stop_time')[0].firstChild) != None:
            stop_time1 = event.getElementsByTagName('stop_time')[0].firstChild.data
        else:
            stop_time1 = "None"    
        if (event.getElementsByTagName('price')[0].firstChild) != None:
            price1 = event.getElementsByTagName('price')[0].firstChild.data
        else:
            price1 = "None"
            
        each_event = Event(id=idnt1, url=url1, title=title1, description=description1,startTime=start_time1, stopTime=stop_time1,price=price1)        
        session.add(each_event)
        session.commit()

#populating performers table
number_of_performers = 0
performers_lst = xmldoc.getElementsByTagName('performer')
for performer in performers_lst:    
    condition = False
    for xyz in performer.getElementsByTagName('url'):
        condition = True
        break    
    if condition and (performer.getElementsByTagName('id')[0].firstChild.data in relevant_performers):
        number_of_performers += 1
        idnt2 = performer.getElementsByTagName('id')[0].firstChild.data        
        url2 = performer.getElementsByTagName('url')[0].firstChild.data  
        name2 = performer.getElementsByTagName('name')[0].firstChild.data        
        if (performer.getElementsByTagName('short_bio')[0].firstChild) != None:
            short_bio2 = performer.getElementsByTagName('short_bio')[0].firstChild.data
        else:
            short_bio2 = ""
        demand_member_count2 = performer.getElementsByTagName('demand_member_count')[0].firstChild.data    
        event_count2 = performer.getElementsByTagName('event_count')[0].firstChild.data    
        popularity2 = performer.getElementsByTagName('popularity')[0].firstChild.data        
        each_performer = Performer(id=idnt2,url=url2,name=name2,shortBio=short_bio2,demandMemberCount=demand_member_count2,eventCount=event_count2,popularity=popularity2)        
        session.add(each_performer)
        session.commit()

#populating events_performers table
for u,v in recent_combinations:  
    each_event_performer = EventPerfomer(eventId=u,performerId=v)
    print(each_event_performer)
    session.add(each_event_performer)
    session.commit()
    
y_time = time.time()
timetaken = int(y_time - x_time)/60

print("")
print("******* Statistics **********")
print("number of performers: ",number_of_performers)
print("number of combinations: ",len(recent_combinations))
print("number of rel performers: ",len(relevant_performers))
print("number of events: ",number_of_events)
print("Time taken in mins: ",timetaken)
