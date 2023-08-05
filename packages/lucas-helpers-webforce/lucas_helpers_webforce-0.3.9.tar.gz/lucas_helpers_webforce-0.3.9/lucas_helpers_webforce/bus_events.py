from abc import abstractmethod
import json
import traceback

class BusEvents():
    def handle_event(self, data):
        try:
            data = json.loads(data)
            event_method = data.get('event')
            self.method_exists(event_method)
            
            method = getattr(self, event_method)
            method(data.get('payload'))
        except Exception as e:
            print(traceback.format_exc())
    
    def method_exists(self, event_method):
        if event_method is None: 
            raise Exception('Event type is not set')
        
        if not hasattr(self, event_method):
            raise Exception('No event method defined in class')
    
    @abstractmethod
    def new_queue(self, data):
        print("Event method new_queue has not been implemented")
        pass

    @abstractmethod
    def join_to_new_queue(self, data):
        print("Event method join_to_new_queue has not been implemented")
        pass

    @abstractmethod
    def add_worker_to_queue(self, data):
        print("Event method add_worker_to_queue has not been implemented")
        pass