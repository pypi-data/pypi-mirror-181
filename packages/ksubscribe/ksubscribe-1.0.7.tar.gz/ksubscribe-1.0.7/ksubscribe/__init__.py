"""
Ksubscribe

An event-based programming methodology for Python coders!
"""

__version__ = "1.0.7"
__author__ = 'Osman Onur KUZUCU'
__credits__ = 'KZC Software Inc.'

#TODO: place a link that is contains example
__usageDescription__ = "Subscriber class must have _inform or _informWithParameters functions. You can see the examples in examples "


class KsubscribeSingletonMeta(type):
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


class Ksubscribe(metaclass=KsubscribeSingletonMeta):
    def __init__(self):
        self.__eventList={}  

    
    def _subscribeForAnEvent(self,subscriber,eventName:str):
        try:
            if(self.__eventList.get(eventName) != None):
                self.__eventList[eventName].append(subscriber)
            else:
                self._createAnEvent(eventName)
                self._subscribeForAnEvent(subscriber,eventName)
                print("Ksubsribe : There is not an event. Because the event is not exist in event collections. KSubscribe has created an event to subscribe.")
            return True

        except Exception as e:
            print("Ksubsribe : ",e)
            return False

    def _createAnEvent(self, eventName:str):
        try:
            if(self.__eventList.get(eventName) == None):
                self.__eventList[eventName] = []
                return True

            else:
                print("Ksubsribe : Cannot create an event. Because the event is exist in event list")
                return False

        except Exception as e:
            print("Ksubsribe : ",e)
            return False



    def _publish(self,eventName:str,parameters=None):
        try:
            if(self.__eventList.get(eventName) != None):
                for x in self.__eventList[eventName]:
                    x.inform(eventName,parameters)
            else:
                print("Ksubsribe : Cannot publish an event. Because the event is not exist in event list")
        except Exception as e:
            print("Ksubsribe : ",e)

    def _removeAnEvent(self,eventName:str):
        try:
            if(self.__eventList.get(eventName) != None):
                self.__eventList.pop(eventName)
                return True

            else:
                print("Ksubsribe : Cannot remove an event. Because the event is not exist in event list")
                return False

        except Exception as e:
            print("Ksubsribe : ",e)
            return False

    def _removeAllEvents(self):
        try:
            if(len(self.__eventList)>0):
                self.__eventList.clear()
                return True
            else:
                print("Ksubsribe : Cannot remove all events. Because there is not events in event list")
                return False

        except Exception as e:
            print("Ksubsribe : ",e)
            return False

    def _removeSubscriberFromEvent(self,subscriber, eventName:str):
        try:
            if(self.__eventList.get(eventName) != None):
                if(subscriber in self.__eventList.get(eventName)):
                    self.__eventList.get(eventName).remove(subscriber)
                    return True
                else:
                    print("Ksubsribe : The subscriber does not in event subscriber list")
                    return False
            else:
                print("Ksubsribe : Cannot remove subscriber. Because the event is not exist in event collections")
                return False

        except Exception as e:
            print("Ksubsribe : ",e)
            return False
    
