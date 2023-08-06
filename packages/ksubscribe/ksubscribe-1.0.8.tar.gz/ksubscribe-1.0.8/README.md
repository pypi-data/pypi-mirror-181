# ksubscribe
Python-Event-Based-Programming-Methodology


Ksubscribe library for Python Coders

<br/><br/>
This is a library that help python coder to run event-based methodology.
<br/><br/>
You can subscribe an event from object to another object. Ksubscribe library is designed with _**Singleton design pattern**_. So, if you create more that one Ksubscribe object, the all object is actually **same object**.
<br/><br/>

## **!!!!**

<br/>

Firstly, subscriber can subscribe an any event that is created before.  After this operation, subscriber class **must have inform functions**. 

You can see the inform function in below. Subscribed classc can send only one parameter that can be list, dict etc.

```
    def inform(self,eventName,parameters=None)

```

You can publish the event from subscriber like this from **subscribed class** <br/>

```
    self.slaveEventObject = Ksubscribe()
    def eventTwoSecond(self):
        self.slaveEventObject._publish(eventName="everyTwoSecond")
```

The ksubscribe library has these function that is mentioned in below.

```
    def _subscribeForAnEvent(self,subscriber,eventName:str)
       If this function returns True, subsciption is built.
       If this function returns False, subscription is not built.


    def _createAnEvent(self, eventName:str)
       If this function returns True, event is created.
       If this function returns False, event is not created.


    def _publish(self,eventName:str,parameters=None)
        This function does not return any value.


    def _removeAnEvent(self,eventName:str)
        If this function returns True, event is removed from event list.
        If this function returns False, event is not removed from event list


    def _removeAllEvents(self)
        If this function returns True, all events are removed.
        If this function returns False, all events are not removed.
    

    def _removeSubscriberFromEvent(self,subscriber, eventName:str)
        If this function returns True, subscriber is removed from event's subscriber list.
        If this function returns False, subscriber is not removed from event's subscriber list.
```

<br/><br/>
You can check [example usage](https://github.com/bossman48/ksubscribe-example-usage#in-this-example-usage-of-ksubscribe-we-have-master-and-slave-class)

<br/><br/>
If you have any question, send mail to [me](kuzucu48@gmail.com)



