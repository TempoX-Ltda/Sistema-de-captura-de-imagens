from configparser import ConfigParser

Config = ConfigParser()

Config.read(r'classes\PreProcessorCameraConfig.ini')

print(Config.get('Render Jatoba Caemmun', 'recortY'))