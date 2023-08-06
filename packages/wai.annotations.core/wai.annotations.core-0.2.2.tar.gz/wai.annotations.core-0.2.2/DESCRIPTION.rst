wai.annotations core module, containing core data structures and basic data loading and preprocessing techniques.

The following sources are available:

* `from-audio-files-ac`: dummy reader that turns audio files into a classification dataset.
* `from-audio-files-sp`: dummy reader that turns audio files into a speech dataset.
* `from-images-ic`: dummy reader that turns images into an image classification dataset.
* `from-images-is`: dummy reader that turns images into an image segmentation dataset.
* `from-images-od`: dummy reader that turns images into an object detection dataset.


The following inline stream processors (ISPs) area available:

* `check-duplicate-filenames`: causes the conversion stream to halt when multiple dataset items have the same filename
* `clean-transcript`: ISP that cleans speech transcripts.
* `coerce-box`: converts all annotation bounds into box regions
* `coerce-mask`: converts all annotation bounds into polygon regions
* `convert-image-format`: converts images from one format to another
* `dimension-discarder`: removes annotations which fall outside certain size constraints
* `discard-invalid-images`: discards images that cannot be loaded (e.g., corrupt image file or annotations with no image)
* `discard-negatives`: discards negative examples (those without annotations) from the stream
* `filter-labels`: filters detected objects down to those with specified labels.
* `filter-metadata`: filters detected objects based on their meta-data.
* `label-present`: keeps or discards images depending on whether annotations with certain label(s) are present. Checks can be further tightened by defining regions in the image that annotations must overlap with (or not overlap at all).
* `map-labels`: maps object-detection labels from one set to another
* `passthrough`: dummy ISP which has no effect on the conversion stream
* `polygon-discarder`: removes annotations with polygons which fall outside certain point limit constraints
* `remove-classes`: removes classes from classification/image-segmentation instances
* `rename`: ISP that renames files.
* `sample`: ISP that selects a subset from the stream.
* `strip-annotations`: ISP which removes annotations from instances


The following cross-domain converters (XDCs) are available:
* `od-to-ic`: converts image object-detection instances into image classification instances
* `od-to-is`: converts image object-detection instances into image segmentation instances


The following sinks are available:

* `to-audio-files-ac`: dummy writer that just outputs audio files from classification datasets.
* `to-audio-fileS-sp`: dummy writer that just outputs audio files from speech datasets.
* `to-images-ic`: dummy writer that just outputs images from image classification datasets.
* `to-images-is`: dummy writer that just outputs images from image segmentation datasets.
* `to-images-od`: dummy writer that just outputs images from object detection datasets.
* `to-void-ac`: consumes audio classification instances without writing them.
* `to-void-ic`: consumes image classification instances without writing them.
* `to-void-is`: consumes image segmentation instances without writing them.
* `to-void-od`: consumes instances without writing them.
* `to-void-sp`: consumes instances without writing them.
