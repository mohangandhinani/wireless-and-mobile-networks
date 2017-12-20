#########################################################
# sender.py
# Reference : https://stackoverflow.com
#########################################################

import pygame
import sys
import comtypes.client

from comtypes import *
from ctypes   import POINTER
from ctypes.wintypes import DWORD, BOOL

CLSID_MMDeviceEnumerator = \
    GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')

IID_IAudioEndpointVolume = \
    GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')

#########################################################
# Microsoft Windows related Class definitions below
#########################################################
class IMMDeviceCollection(IUnknown):
    _iid_ = GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
    pass

class IAudioEndpointVolume(IUnknown):
    _iid_ = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
    _methods_ = [
        STDMETHOD(HRESULT, 'RegisterControlChangeNotify', []),
        STDMETHOD(HRESULT, 'UnregisterControlChangeNotify', []),
        STDMETHOD(HRESULT, 'GetChannelCount', []),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevel',
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
            (['in'], DWORD, 'nChannel'),
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
            (['in'], DWORD, 'nChannel'),
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
            (['in'], DWORD, 'nChannel'),
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
            (['in'], DWORD, 'nChannel'),
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'SetMute',
            (['in'], BOOL, 'bMute'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetMute',
            (['out','retval'], POINTER(BOOL), 'pbMute')
        ),
        COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
            (['out','retval'], POINTER(c_float), 'pnStep'),
            (['out','retval'], POINTER(c_float), 'pnStepCount'),
        ),
        COMMETHOD([], HRESULT, 'VolumeStepUp',
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'VolumeStepDown',
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'QueryHardwareSupport',
            (['out','retval'], POINTER(DWORD), 'pdwHardwareSupportMask')
        ),
        COMMETHOD([], HRESULT, 'GetVolumeRange',
            (['out','retval'], POINTER(c_float), 'pfMin'),
            (['out','retval'], POINTER(c_float), 'pfMax'),
            (['out','retval'], POINTER(c_float), 'pfIncr')
        ),
    ]

class IMMDevice(IUnknown):
    _iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'Activate',
            (['in'], POINTER(GUID), 'iid'),
            (['in'], DWORD, 'dwClsCtx'),
            (['in'], POINTER(DWORD), 'pActivationParans'),
            (['out','retval'], POINTER(POINTER(IAudioEndpointVolume)), 'ppInterface')
        ),
        STDMETHOD(HRESULT, 'OpenPropertyStore', []),
        STDMETHOD(HRESULT, 'GetId', []),
        STDMETHOD(HRESULT, 'GetState', [])
    ]
    pass

class IMMDeviceEnumerator(comtypes.IUnknown):
    _iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')

    _methods_ = [
        COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
            (['in'], DWORD, 'dataFlow'),
            (['in'], DWORD, 'dwStateMask'),
            (['out','retval'], POINTER(POINTER(IMMDeviceCollection)), 'ppDevices')
        ),
        COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
            (['in'], DWORD, 'dataFlow'),
            (['in'], DWORD, 'role'),
            (['out','retval'], POINTER(POINTER(IMMDevice)), 'ppDevices')
        )
    ]

enumerator = comtypes.CoCreateInstance( 
    CLSID_MMDeviceEnumerator,
    IMMDeviceEnumerator,
    comtypes.CLSCTX_INPROC_SERVER
)

endpoint = enumerator.GetDefaultAudioEndpoint( 0, 1 )
volume = endpoint.Activate( IID_IAudioEndpointVolume, comtypes.CLSCTX_INPROC_SERVER, None )

# Global constants
FREQ        = 44100 # same as audio CD
BITSIZE     = -16   # unsigned 16 bit
CHANNELS    = 2     # 1 == mono, 2 == stereo
BUFFER      = 1024  # audio buffer size in no. of samples
FRAMERATE   = 60    # how often to check if playback has finished

sounds = {
    'a': 'wa200.wav',
    'b': 'wb240.wav',
    'c': 'wc280.wav',
    'd': 'wd320.wav',
    'e': 'we360.wav',
    'f': 'wf400.wav',
    'g': 'wg440.wav',
    'h': 'wh480.wav',
    'i': 'wi520.wav',
    'j': 'wj560.wav',
    'k': 'wk600.wav',
    'l': 'wl640.wav',
    'm': 'wm680.wav',
    'n': 'wn720.wav',
    'o': 'wo760.wav',
    'p': 'wp800.wav',
    'q': 'wq840.wav',
    'r': 'wr880.wav',
    's': 'ws920.wav',
    't': 'wt960.wav',
    'u': 'wu1000.wav',
    'v': 'wv1040.wav',
    'w': 'ww1080.wav',
    'x': 'wx1120.wav',
    'y': 'wy1160.wav',
    'z': 'wz1200.wav',
    ' ': 'wspace1800.wav'
}

pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)

#########################################################
# Function to play the sound file
#########################################################
def playsound(soundfile):
    """
    Play sound through default mixer channel in blocking manner.
    This will load the whole sound into memory before playback
    """
    sound = pygame.mixer.Sound(soundfile)
    clock = pygame.time.Clock()
    volume.SetMasterVolumeLevel(-1, None)
    sound.play()
    while pygame.mixer.get_busy():
        clock.tick(FRAMERATE)

#########################################################
# main function begins here
#########################################################
def main(argv):
    while True:
        convert_string = raw_input("\n\nEnter Message : "),
        for i in convert_string[0]:
            playsound(pygame.mixer.Sound('SoundFiles/' + sounds[i]))


if __name__ == '__main__':
    main(sys.argv[1:])
