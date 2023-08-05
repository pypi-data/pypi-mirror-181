import sqlalchemy
from sqlalchemy.orm import sessionmaker

class Connection:
    def __init__(self, **kwargs) -> None:
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.database = kwargs.get('database')
        
        self.__engine = None
        self.session = None
        self.validate_and_connect()

    def validate_and_connect(self):
        if self.user is None or self.password is None or self.database is None:
            raise Exception('No valid database credentials specified')
        
        self.connect()

    def connect(self):
        try:
            if self.valid_parameters() is False:
                raise Exception('Invalid parameters')
            
            self.__engine = sqlalchemy.create_engine(
                f"mysql+pymysql://{self.user}:{self.password}@db/{self.database}"
            )

            self.session = sessionmaker(bind=self.__engine)
        except Exception as e:
            print(e)
    
    def valid_parameters(self) -> bool:
        if self.user is None or self.password is None or self.database is None:
            return False
        return True
 
    
    def set_user(self, user):
        self.user = user
    
    def get_user(self):
        return self.user

    def set_password(self, password):
        self.password = password
    
    def get_password(self):
        return self.password
    
    def get_engine(self):
        return self.__engine          
            

