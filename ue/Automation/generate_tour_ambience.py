"""Generate a quiet original seamless air-noise loop; no third-party recordings."""
import json,wave,hashlib
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1];out=root/'SourceAudio';out.mkdir(exist_ok=True)
rate=44100;seconds=32;n=rate*seconds;rng=np.random.default_rng(48049);freq=np.fft.rfftfreq(n,1/rate)
weight=np.maximum(freq,1)**(-.55)*(1-np.exp(-(freq/100)**2))*np.exp(-(freq/4200)**2)
phase=rng.uniform(0,2*np.pi,len(freq));spectrum=weight*np.exp(1j*phase);spectrum[0]=0
signal=np.fft.irfft(spectrum,n);t=np.arange(n)/rate;envelope=.85+.10*np.sin(2*np.pi*t/seconds)+.05*np.sin(6*np.pi*t/seconds+.6);signal*=envelope;signal*=.04/np.sqrt(np.mean(signal**2));pcm=(np.clip(signal,-.9,.9)*32767).astype('<i2')
path=out/'Tour_Gentle_Air.wav'
with wave.open(str(path),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(pcm.tobytes())
(out/'SOURCE.json').write_text(json.dumps({'source':'Original deterministic synthesis by this project; not a recording of the school.','purpose':'Subtle optional air ambience; no music or speech','seconds':seconds,'sample_rate':rate,'rms_dbfs':20*np.log10(np.sqrt(np.mean(signal**2))),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2),encoding='utf8')
print(path)
