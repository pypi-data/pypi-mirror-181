
__version__ = "1.0.1"
__author__ = "Osman Onur KUZUCU"
__company__ = "KZC Software Inc."

import time
from ksubscribe import Ksubscribe
from threading import Thread

class KtimerSingletonMeta(type):

    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class KTimer(metaclass=KtimerSingletonMeta):

    __scheduledEvent = {}
    kSubscribeObject = Ksubscribe()
    workOrStop = True 

    def __init__(self):
        # create a thread
        self.thread = Thread(target=self._publishEventBasedOnTimer)
        # run the thread
        self.thread.start()

    def _createScheduledEvent(self, subscriber,eventName:str, msTimePeriod:int):
        
        try:
            __startMs = time.time()*1000
            if(self.kSubscribeObject._createAnEvent(eventName)):
                if(self.kSubscribeObject._subscribeForAnEvent(subscriber,eventName)):
                    self.__scheduledEvent[eventName] = {"subscriber":[subscriber] , "timePeriod": msTimePeriod, "milisEventGenerated":__startMs} 
                    return True
                else:
                    print("Ztimer : cannot subscribe a scheduled event")
                    return False
            else:
                print("ZTimer : cannot create a scheduled event")
                return False
        except Exception as e:
            print("Ztimer_createScheduledEvent : ",e)
            return False

    def _subscribeScheduledEvent(self, subscriber,eventName:str):
        try:
            if(self.kSubscribeObject._subscribeForAnEvent(subscriber,eventName)):
                self.__scheduledEvent[eventName]["subscriber"].append(subscriber)
                return True
            else:
                print("ZTimer : cannot subscribe event")
                return False
        except Exception as e:
            print("Ztimer_subscribeScheduledEvent : ",e)
            return False

    def _removeScheduledEvent(self,eventName:str):
        try:
            if(self.kSubscribeObject._removeAnEvent(eventName)):
                self.__scheduledEvent.pop(eventName)
                return True
            else:
                print("Ztimer : cannot remove event from event list")
                return False
        except Exception as e:
            print("Ztimer_removeScheduledEvent : ",e)
            return False
    
    def _removeSubscriberFromScheduledEvent(self,subscriber,eventName:str):
        try:
            if(self.__scheduledEvent.get(eventName) != None):
                if(subscriber in self.__scheduledEvent.get(eventName).get("subscriber")):
                    self.__scheduledEvent.get(eventName).get("subscriber").remove(subscriber)
                    self.kSubscribeObject._removeSubscriberFromEvent(subscriber,eventName)
                    return True
                else:
                    print("Ztimer : There is no subscribtion with eventName-Subscriber")
                    return False
            else:
                print("Ztimer : There is no event with this name")
                return False
        except Exception as e:   
            print("Ztimer_removeSubscriberFromScheduledEvent : ",e)
            return False

    
    def _publishEventBasedOnTimer(self):
        while(self.workOrStop):
            try:
                currentMilis = time.time()*1000
                for element in list(self.__scheduledEvent.keys()):
                    if(self.__scheduledEvent != None and self.__scheduledEvent.get(element) != None and self.__scheduledEvent.get(element).get("milisEventGenerated") != None and self.__scheduledEvent.get(element).get("timePeriod") !=None):
                        if(currentMilis - self.__scheduledEvent.get(element).get("milisEventGenerated") >= self.__scheduledEvent.get(element).get("timePeriod")):
                            self.kSubscribeObject._publish(eventName= element)
                            self.__scheduledEvent.get(element)["milisEventGenerated"] = currentMilis  
                    else:
                        print(self.__scheduledEvent.get(element))
            except Exception as e:
                print("Ztimer_publishEventBasedOnTimer : ",e)

    def _stopThread(self):
        self.workOrStop = False     

    def __del__(self):
        self._stopThread() 

    