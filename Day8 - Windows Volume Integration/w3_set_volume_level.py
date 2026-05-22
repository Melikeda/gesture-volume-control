from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import IAudioEndpointVolume

from ctypes import cast, POINTER


# Hoparlör cihazını al
devices = AudioUtilities.GetSpeakers()


# Endpoint volume al
interface = devices.EndpointVolume


# Volume objesine çevir
volume = cast(
    interface,
    POINTER(IAudioEndpointVolume)
)


# Ses seviyesini değiştir
volume.SetMasterVolumeLevelScalar(
    0.5,
    None
)

print("Volume changed to 50%")