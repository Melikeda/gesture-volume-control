from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import IAudioEndpointVolume

from ctypes import cast, POINTER


# Hoparlör cihazını al
devices = AudioUtilities.GetSpeakers()

print(devices)


# Endpoint volume al
interface = devices.EndpointVolume

print(interface)


# Volume objesine çevir
volume = cast(
    interface,
    POINTER(IAudioEndpointVolume)
)

print(volume)