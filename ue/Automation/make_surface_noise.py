"""Deterministic seamless multi-scale material detail, authored for this project."""
import numpy as np
from PIL import Image
from pathlib import Path
n=1024;rng=np.random.default_rng(43044)
freq=np.fft.fftfreq(n);radius=np.sqrt(freq[:,None]**2+freq[None,:]**2)
channels=[]
for cutoff in (.012,.065,.25):
    spectrum=np.fft.fft2(rng.normal(size=(n,n)))
    layer=np.fft.ifft2(spectrum*np.exp(-(radius/cutoff)**2)).real
    layer=np.clip(.5+layer/(layer.std()*5),0,1);channels.append(layer)
rgba=np.stack(channels+[np.ones((n,n))],axis=-1)
path=Path(__file__).resolve().parents[1]/'SourceTextures/T_SurfaceDetail.png'
path.parent.mkdir(exist_ok=True);Image.fromarray((rgba*255).astype('uint8')).save(path)
print(path)
