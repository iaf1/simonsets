from parameters import parameters

class Settings:
    def __init__(self,params):
        for param in params:
            setattr(self,param,params[param])

cf = Settings(parameters)