import os
__home = os.environ['HOME']
config = {
    'home': __home,
    'axiom_path': os.path.join(__home, 'reaxiom'),
    'axiom_cache': os.path.join(__home, 'reaxiom', 'cache'),
    'huggingface_cache': os.path.join(__home, 'reaxiom', 'huggingface_cache'),
    'bypy_cache': os.path.join(__home, 'reaxiom', 'bypy_cache')
}
