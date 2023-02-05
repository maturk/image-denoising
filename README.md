A small collection of Image Based Denoising algorithms written in Python. Small writeup and demo images can be seen here: [link to demo.](https://maturk.github.io/page/2023/02/03/image_denoising.html) All algorithms are hard coded. Requirements are only numpy and Pillow (see requirements.txt).

## Algorithms:
- [x] Gaussian blur
- [x] Bilateral filter
    - [ ] TODO: optimize bilateral 

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
