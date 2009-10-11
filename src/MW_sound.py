import pygame

class soundMan:
    class __impl:
        def __init__(self):
            soundList = dict()
            pass
        def loadSound(self,filename):
            """loads sound filename and puts it on the flywheel
            
            filename: string"""
            soundList[filename] = pygame.mixer.Sound(filename)
            
        def play(self, filename):
            if not soundList[filename]:
                loadSound(filename)
            soundList[filename].play()
        
    __instance = None
    def __init__(self):
        """ create instance """
        #check if instance exists and create it
        if soundMan.__instance is None:
            soundMan.__instance = soundMan.__impl()
            
        
        #store instance reference as the only member in the handle???
        self.__dict__['_soundMan_instance'] = soundMan.__instance
    
    def __getattr__(self, attr):
        """delegate access to implementation"""
        return getattr(self.__instance, attr)
    
    def __setattr__(self, attr, value):
        """delegate access to implementation"""
        return setattr(self.__instance, attr, value) 
        