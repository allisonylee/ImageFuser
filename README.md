# ImageFuser

Version 1.0 for Mac and Windows OS can be downloaded under "Releases."

# Abstract

Characterization of materials by electron microscopy (EM) is one of the essential methods to
understand their detailed structures from micron to nanoscale. However, raw EM images often
contain noise, distortions, and artifacts that obscure fine structural details, necessitating post-
processing techniques to extract meaningful information. Here, we introduce ImageFuser, a
software application that improves the quality of EM images by performing noise reduction,
contrast enhancement, and artifact correction through image fusion, a process which integrates
features from a series of images into one singular image. This also makes further processing less
computationally expensive, as the same information is contained within a smaller dataset. When
fusing images, ImageFuser first aligns them using enhanced correlation coefficient
maximization, for the sample can shift in between images, then fuses them using the discrete
wavelet transform. ImageFuser’s interface also allows users to resize images, crop images, and
extract frames from videos without any programming.
