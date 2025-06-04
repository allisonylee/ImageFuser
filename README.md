# ImageFuser

Version 1.0 for Mac and Windows OS can be downloaded under "Releases."

Characterization of materials by electron microscopy (EM) is one of the essential methods to
understand their detailed structures from micron to nanoscale. However, raw EM images often
contain noise, distortions, and artifacts that obscure fine structural details, necessitating 
post-processing techniques to extract meaningful information. Here, we introduce ImageFuser, a
software application that improves the quality of EM images by performing noise reduction,
contrast enhancement, and artifact correction through image fusion, a process which integrates
features from a series of images into one singular image. This also makes further processing less
computationally expensive, as the same information is contained within a smaller dataset. When
fusing images, ImageFuser first aligns them using enhanced correlation coefficient
maximization, for the sample can shift in between frames, then fuses them using the discrete
wavelet transform. ImageFuser’s interface also allows users to resize images, crop images, and
extract frames from videos without any programming.

## Usage

### Example: Hydroxyapatite (HAP)

Original video captured through transmission electron microscopy (TEM): [Click here](https://www.dropbox.com/scl/fo/2hpp3uekg4ot36icgn0gw/ACLR7ox9yQ3NmNZv4ATOxE4/004-videoprocessing?dl=0&preview=20240716+HAADF-BF+1146+64000+x-151.mpg&rlkey=19fl0d3ub18bv2pykhmputds1&subfolder_nav_tracking=1)

Final result after fusing 249 frames: ![Fused HAP](https://github.com/allisonylee/ImageFuser/raw/refs/heads/main/examples/fusedHAP.tif)

Another example can be seen in the "Examples" folder with a tantalum film captured through TEM, in which 100 images were fused.
