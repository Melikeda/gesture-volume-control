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


# Mevcut ses seviyesini al
current_volume = volume.GetMasterVolumeLevelScalar()

print(current_volume)
print(round(current_volume, 2)) #virgülden sonra 2 basamak  gösterme
print(int(current_volume * 100), "%") #yüzde olarak yazdırma 