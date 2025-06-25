from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeController:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
    def get_volume(self):    
        return self.volume.GetMasterVolumeLevelScalar()
    def volume_up(self):
        self.volume.SetMasterVolumeLevelScalar(min(self.get_volume() + 0.15, 1.0), None)

    def volume_down(self):
        self.volume.SetMasterVolumeLevelScalar(max(self.get_volume() - 0.15, 0.0), None)        

    def volume_up_a_bit(self):
        self.volume.SetMasterVolumeLevelScalar(min(self.get_volume() + 0.05, 1.0), None)
    def volume_down_a_bit(self):
        self.volume.SetMasterVolumeLevelScalar(max(self.get_volume() - 0.05, 0.0), None)
        
    def volume_to(self, to:float):
        """
        This sets the volume to a specific level, But Provide the said/10 value where said is the level set by the user
        0 < said < 100.
        """
        if 0 <= to <= 1:
            self.volume.SetMasterVolumeLevelScalar(to, None)
        else:
            raise ValueError("Volume level must be between 0.0 and 1.0")
    
    def mute(self):
        self.volume.SetMute(1, None)
    def unmute(self):
        self.volume.SetMute(0, None)
    


