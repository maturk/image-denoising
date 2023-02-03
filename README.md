A small collection of Image Based Denoising algorithms written in Python

## Algorithms:
- [x] Gaussian blur
- [ ] Bilateral filter

## Download
```
git clone git@github.com:maturk/image-denoising.git
cd image-denoising/
pip install -r requirements.txt    
```

### Gaussian Blur
Gaussian blur is one of the simplest denoising algorithms and it amounts to estimating
at each pixel position a local average of intensities and corresponds to low-pass filtering.

```
python ./gaussian-blur/gaussian-blur.py
```
### Bilateral Filter
The bilateral filter is technique to smooth images while preserving edges.
