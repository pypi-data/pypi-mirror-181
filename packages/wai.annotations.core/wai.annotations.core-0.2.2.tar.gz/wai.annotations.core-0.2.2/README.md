# wai-annotations-core
wai.annotations core module, containing core data structures and basic data loading and preprocessing techniques.

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/


## Commands

The following sections contain the help screens of the wai.annotations main commands.  

### batch-split

```
usage: wai-annotations batch-split [-d DIR [DIR ...]] [-g GLOB] [--grouping-groups GROUPS]
                                   [--grouping-regexp REGEXP] [-h] [-i FILENAME [FILENAME ...]] [-o DIR]
                                   [--output-ext EXT] [-O NAMING] [-s SEED] [-n [SPLIT NAME [SPLIT NAME ...]]]
                                   [-r RATIO [RATIO ...]] [-v] [STAGE [STAGE ...]]

When datasets contain multiple batches, it is recommended to get the same distribution of each batch when
generating train/test/validation datasets. The 'batch-split' command allows you to generate these splits for
each batch separately, outputting .list files that can be used as input for conversion plugins (using '-I'
instead of '-i'). Furthermore, it is possible to group files within a batch that should stay together,
e.g.,images that depict the same object(s) and can be distinguished via a prefix or suffix. The grouping is
achieved via regular expression groups.

optional arguments:
  -d DIR [DIR ...], --dir DIR [DIR ...]
                        the batch directories to look for files using the supplied glob expression (--glob)
                        (default: [])
  -g GLOB, --glob GLOB  the glob expression to apply when looking for files in the input directories (--dir),
                        e.g., '*.xml' (default: None)
  --grouping-groups GROUPS
                        the comma-separated list of regular expression group indices (0: all, 1: first group,
                        etc) that will make up the string for identifying files to treat as single unit, e.g.:
                        '1,3' (default: None)
  --grouping-regexp REGEXP
                        the regular expression with groups for combining files into groups that get treated as
                        a unit, e.g.: '([a-z]+)(-a|-b|-c)(-[a-z]+).csv' (default: None)
  -h, --help            prints this help message and exits (default: False)
  -i FILENAME [FILENAME ...], --input FILENAME [FILENAME ...]
                        each -i/--input defines a single batch that gets split separately, to be used with glob
                        syntax, e.g., '-i /some/where/*.xml' (default: [])
  -o DIR, --output-dir DIR
                        the directory to store the generated splits in as files (default: *)
  --output-ext EXT      the extension to use for the split files (incl dot) (default: .list)
  -O NAMING, --output-naming NAMING
                        how the generate the name for the created split files in the output directory:
                        enumerate|input_dir (default: input_dir)
  -s SEED, --seed SEED  the seed value to use for randomizing the input files (default: None)
  -n [SPLIT NAME [SPLIT NAME ...]], --split-names [SPLIT NAME [SPLIT NAME ...]]
                        the names to use for the batch splits (default: [])
  -r RATIO [RATIO ...], --split-ratios RATIO [RATIO ...]
                        the ratios to use for the batch splits (default: [])
  -v, --verbose         outputs debugging information (default: False)
```

### convert

```
usage: wai-annotations convert [-h] [--macro-file FILENAME] [-v] [STAGE [STAGE ...]]

Defines the stages in a conversion pipeline: Source [ISP [ISP ...]] Sink

optional arguments:
  -h, --help            prints this help message and exits (default: False)
  --macro-file FILENAME
                        the file to load macros from (default: )
  -v                    whether to be more verbose when generating the records (default: 0)
```

### domains

```
usage: wai-annotations domains [-d] [-f {cli,markdown}] [-h] [-o DOMAIN [DOMAIN ...]] [STAGE [STAGE ...]]

Outputs information on the (data) domains available within the virtual environment.

optional arguments:
  -d, --no-descriptions
                        whether to suppress the descriptions of the plugins (default: True)
  -f {cli,markdown}, --formatting {cli,markdown}
                        the formatting style to print the domains in (default: cli)
  -h, --help            prints this help message and exits (default: False)
  -o DOMAIN [DOMAIN ...], --only DOMAIN [DOMAIN ...]
                        restrict the set of domains to only those specified (default: [])
```

### plugins

```
usage: wai-annotations plugins [-d] [-D] [-f {cli,markdown}] [-g] [-h] [-o PLUGIN [PLUGIN ...]]
                               [-O TYPE [TYPE ...]] [-n] [STAGE [STAGE ...]]

Outputs command-line help information on one or more plugins, in plain text or markdown.

optional arguments:
  -d, --no-descriptions
                        whether to suppress the descriptions of the plugins (default: True)
  -D, --no-domains      whether to suppress the domains of the plugins (default: True)
  -f {cli,markdown}, --formatting {cli,markdown}
                        the formatting style to print the plugins in (default: cli)
  -g, --group-by-type   whether to group the plugins by their function (default: False)
  -h, --help            prints this help message and exits (default: False)
  -o PLUGIN [PLUGIN ...], --only PLUGIN [PLUGIN ...]
                        restrict the set of plugins to only those specified (default: [])
  -O TYPE [TYPE ...], --only-types TYPE [TYPE ...]
                        restricts the set of plugins to only the specified types (can be source, sink, or
                        processor) (default: [])
  -n, --no-options      whether to suppress the options to the plugin (default: True)
```


## Plugins

### CHECK-DUPLICATE-FILENAMES
Causes the conversion stream to halt when multiple dataset items have the same filename

#### Domain(s):
- **Image Object-Detection Domain**
- **Audio classification domain**
- **Speech Domain**
- **Image Classification Domain**
- **Spectrum Classification Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: check-duplicate-filenames
```

### CLEAN-TRANSCRIPT
ISP that cleans speech transcripts.

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: clean-transcript [-b] [-c CUSTOM] [-a] [-l] [-n] [-p] [-q] [--verbose]

optional arguments:
  -b, --brackets        removes brackets: ()[]{}〈〉 (default: False)
  -c CUSTOM, --custom CUSTOM
                        the custom characters to remove (default: )
  -a, --non-alpha-numeric
                        removes all characters that are not alpha-numeric (default: False)
  -l, --non-letters     removes all characters that are not letters (default: False)
  -n, --numeric         removes all numeric characters (default: False)
  -p, --punctuation     removes punctuation characters: :;,.!? (default: False)
  -q, --quotes          removes quotes: '"‘’“”‹›«» (default: False)
  --verbose             outputs information about processed transcripts (default: False)
```

### COERCE-BOX
Converts all annotation bounds into box regions

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: coerce-box
```

### COERCE-MASK
Converts all annotation bounds into polygon regions

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: coerce-mask
```

### CONVERT-IMAGE-FORMAT
Converts images from one format to another

#### Domain(s):
- **Image Object-Detection Domain**
- **Image Segmentation Domain**
- **Image Classification Domain**

#### Options:
```
usage: convert-image-format -f FORMAT

optional arguments:
  -f FORMAT, --format FORMAT
                        format to convert images to (default: None)
```

### DIMENSION-DISCARDER
Removes annotations which fall outside certain size constraints

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: dimension-discarder [--max-area MAX_AREA] [--max-height MAX_HEIGHT] [--max-width MAX_WIDTH]
                           [--min-area MIN_AREA] [--min-height MIN_HEIGHT] [--min-width MIN_WIDTH]
                           [--verbose]

optional arguments:
  --max-area MAX_AREA   the maximum area of annotations to convert (default: None)
  --max-height MAX_HEIGHT
                        the maximum height of annotations to convert (default: None)
  --max-width MAX_WIDTH
                        the maximum width of annotations to convert (default: None)
  --min-area MIN_AREA   the minimum area of annotations to convert (default: None)
  --min-height MIN_HEIGHT
                        the minimum height of annotations to convert (default: None)
  --min-width MIN_WIDTH
                        the minimum width of annotations to convert (default: None)
  --verbose             outputs information when discarding annotations (default: False)
```

### DISCARD-INVALID-IMAGES
Discards images that cannot be loaded (e.g., corrupt image file or annotations with no image)

#### Domain(s):
- **Image Object-Detection Domain**
- **Image Segmentation Domain**
- **Image Classification Domain**

#### Options:
```
usage: discard-invalid-images [-v]

optional arguments:
  -v, --verbose  whether to output debugging information (default: False)
```

### DISCARD-NEGATIVES
Discards negative examples (those without annotations) from the stream

#### Domain(s):
- **Image Object-Detection Domain**
- **Audio classification domain**
- **Speech Domain**
- **Image Classification Domain**
- **Spectrum Classification Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: discard-negatives
```

### FILTER-LABELS
Filters detected objects down to those with specified labels or, in case of image classification, removes the label if it doesn't match.

#### Domain(s):
- **Image Object-Detection Domain**
- **Image Classification Domain**

#### Options:
```
usage: filter-labels [-l LABELS [LABELS ...]] [--min-iou FLOAT] [-r regexp] [--region x,y,w,h]

optional arguments:
  -l LABELS [LABELS ...], --labels LABELS [LABELS ...]
                        labels to use (default: [])
  --min-iou FLOAT       the minimum IoU (intersect over union) that the object must have with the
                        region in order to be considered an overlap (object detection only)
                        (default: 0.01)
  -r regexp, --regexp regexp
                        regular expression for using only a subset of labels (default: None)
  --region x,y,w,h      region that the object must overlap with in order to be included (object
                        detection only). Between 0-1 the values are considered normalized, otherwise
                        absolute pixels. (default: None)
```

### FILTER-METADATA
Filters detected objects based on their meta-data.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: filter-metadata [-c COMPARISON] [-k KEY] [-t VALUE_TYPE]

optional arguments:
  -c COMPARISON, --comparison COMPARISON
                        the comparison to apply to the value: for bool/numeric/string '=OTHER' and
                        '!=OTHER' can be used, for numeric furthermore '<OTHER', '<=OTHER',
                        '>=OTHER', '>OTHER'. E.g.: '<3.0' for numeric types will discard any
                        annotations that have a value of 3.0 or larger (default: None)
  -k KEY, --key KEY     the key of the meta-data value to use for the filtering (default: None)
  -t VALUE_TYPE, --value-type VALUE_TYPE
                        the data type that the value represents, available options:
                        bool|numeric|string (default: None)
```

### FROM-AUDIO-FILES-AC
Dummy reader that turns audio files into a classification dataset.

#### Domain(s):
- **Audio classification domain**

#### Options:
```
usage: from-audio-files-ac [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME]
                           [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax) (default: [])
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax) (default: [])
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax) (default: [])
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax) (default: [])
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into (default: None)
  --seed SEED           the seed to use for randomisation (default: None)
```

### FROM-AUDIO-FILES-SP
Dummy reader that turns audio files into a speech dataset.

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: from-audio-files-sp [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME]
                           [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax) (default: [])
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax) (default: [])
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax) (default: [])
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax) (default: [])
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into (default: None)
  --seed SEED           the seed to use for randomisation (default: None)
```

### FROM-IMAGES-IC
Dummy reader that turns images into an image classification dataset.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: from-images-ic [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME]
                      [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax) (default: [])
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax) (default: [])
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax) (default: [])
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax) (default: [])
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into (default: None)
  --seed SEED           the seed to use for randomisation (default: None)
```

### FROM-IMAGES-IS
Dummy reader that turns images into an image segmentation dataset.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: from-images-is [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME]
                      [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax) (default: [])
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax) (default: [])
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax) (default: [])
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax) (default: [])
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into (default: None)
  --seed SEED           the seed to use for randomisation (default: None)
```

### FROM-IMAGES-OD
Dummy reader that turns images into an object detection dataset.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: from-images-od [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME]
                      [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax) (default: [])
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax) (default: [])
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax) (default: [])
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax) (default: [])
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into (default: None)
  --seed SEED           the seed to use for randomisation (default: None)
```

### FROM-SPECTRA-SC
Dummy reader that turns spectra into a spectrum classification dataset.

#### Domain(s):
- **Spectrum Classification Domain**

#### Options:
```
usage: from-spectra-sc [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME]
                       [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax) (default: [])
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax) (default: [])
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax) (default: [])
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax) (default: [])
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into (default: None)
  --seed SEED           the seed to use for randomisation (default: None)
```

### LABEL-PRESENT
Keeps or discards images depending on whether annotations with certain label(s) are present. Checks can be further tightened by defining regions in the image that annotations must overlap with (or not overlap at all).

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: label-present [--coordinate-separator CHAR] [--invert-regions] [-l LABELS [LABELS ...]]
                     [--min-iou FLOAT] [--pair-separator CHAR] [-r regexp]
                     [--region [x,y[;x,y[;...]] [x,y[;x,y[;...]] ...]]] [--verbose]

optional arguments:
  --coordinate-separator CHAR
                        the separator between coordinates (default: ;)
  --invert-regions      Inverts the matching sense from 'labels have to overlap at least one of the
                        region(s)' to 'labels cannot overlap any region' (default: False)
  -l LABELS [LABELS ...], --labels LABELS [LABELS ...]
                        explicit list of labels to check (default: [])
  --min-iou FLOAT       the minimum IoU (intersect over union) that the object must have with the
                        region(s) in order to be considered an overlap (object detection only)
                        (default: 0.01)
  --pair-separator CHAR
                        the separator between the x and y of a pair (default: ,)
  -r regexp, --regexp regexp
                        regular expression for using only a subset of labels (default: None)
  --region [x,y[;x,y[;...]] [x,y[;x,y[;...]] ...]]
                        semicolon-separated list of comma-separated x/y pairs defining the region
                        that the object must overlap with in order to be included. Values between
                        0-1 are considered normalized, otherwise absolute pixels. (default: None)
  --verbose             Outputs some debugging information (default: False)
```

### MAP-LABELS
Maps object-detection labels from one set to another

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: map-labels [-m old=new]

optional arguments:
  -m old=new, --mapping old=new
                        mapping for labels, for replacing one label string with another (eg when
                        fixing/collapsing labels) (default: [])
```

### OD-TO-IC
Converts image object-detection instances into image classification instances

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: od-to-ic [-m HANDLER]

optional arguments:
  -m HANDLER, --multiplicity HANDLER
                        how to handle instances with more than one located object (default: error)
```

### OD-TO-IS
Converts image object-detection instances into image segmentation instances

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: od-to-is [--label-error] --labels LABEL [LABEL ...]

optional arguments:
  --label-error         whether to raise errors when an unspecified label is encountered (default is
                        to ignore) (default: False)
  --labels LABEL [LABEL ...]
                        specifies the labels for each index (default: None)
```

### PASSTHROUGH
Dummy ISP which has no effect on the conversion stream

#### Domain(s):
- **Image Object-Detection Domain**
- **Audio classification domain**
- **Speech Domain**
- **Image Classification Domain**
- **Spectrum Classification Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: passthrough
```

### POLYGON-DISCARDER
Removes annotations with polygons which fall outside certain point limit constraints

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: polygon-discarder [--max-points MAX_POINTS] [--min-points MIN_POINTS] [--verbose]

optional arguments:
  --max-points MAX_POINTS
                        the maximum number of points in the polygon (default: None)
  --min-points MIN_POINTS
                        the minimum number of points in the polygon (default: None)
  --verbose             outputs information when discarding annotations (default: False)
```

### REMOVE-CLASSES
Removes classes from classification/image-segmentation instances

#### Domain(s):
- **Spectrum Classification Domain**
- **Image Segmentation Domain**
- **Audio classification domain**
- **Image Classification Domain**

#### Options:
```
usage: remove-classes -c CLASS [CLASS ...]

optional arguments:
  -c CLASS [CLASS ...], --classes CLASS [CLASS ...]
                        the classes to remove (default: None)
```

### RENAME
ISP that renames files.

#### Domain(s):
- **Image Object-Detection Domain**
- **Audio classification domain**
- **Speech Domain**
- **Image Classification Domain**
- **Spectrum Classification Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: rename [-f NAME_FORMAT] [--verbose]

optional arguments:
  -f NAME_FORMAT, --name-format NAME_FORMAT
                        the format for the new name. Available placeholders: - {name}: the name of
                        the file, without path or extension. - {ext}: the extension of the file
                        (incl dot). - {occurrences}: the number of times this name (excl extension)
                        has been encountered. - {count}: the number of files encountered so far. -
                        {[p]+dir}: the parent directory of the file: 'p': immediate parent, the more
                        the p's the higher up in the hierarchy. (default: {name}{ext})
  --verbose             outputs information about generated names (default: False)
```

### SAMPLE
ISP that selects a subset from the stream.

#### Domain(s):
- **Image Object-Detection Domain**
- **Audio classification domain**
- **Speech Domain**
- **Image Classification Domain**
- **Spectrum Classification Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: sample [-s SEED] [-T THRESHOLD]

optional arguments:
  -s SEED, --seed SEED  the seed value to use for the random number generator; randomly seeded if
                        not provided (default: None)
  -T THRESHOLD, --threshold THRESHOLD
                        the threshold to use for Random.rand(): if equal or above, sample gets
                        selected; range: 0-1; default: 0 (= always) (default: 0.0)
```

### STRIP-ANNOTATIONS
ISP which removes annotations from instances

#### Domain(s):
- **Image Object-Detection Domain**
- **Audio classification domain**
- **Speech Domain**
- **Image Classification Domain**
- **Spectrum Classification Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: strip-annotations
```

### TO-AUDIO-FILES-AC
Dummy writer that just outputs audio files from classification datasets.

#### Domain(s):
- **Audio classification domain**

#### Options:
```
usage: to-audio-files-ac [-o OUTPUT_DIR]

optional arguments:
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        the directory to write the audio files to (default: .)
```

### TO-AUDIO-FILES-SP
Dummy writer that just outputs audio files from speech datasets.

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: to-audio-files-sp [-o OUTPUT_DIR]

optional arguments:
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        the directory to write the audio files to (default: .)
```

### TO-IMAGES-IC
Dummy writer that just outputs images from image classification datasets.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: to-images-ic [-o OUTPUT_DIR]

optional arguments:
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        the directory to write the images to (default: .)
```

### TO-IMAGES-IS
Dummy writer that just outputs images from image segmentation datasets.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: to-images-is [-o OUTPUT_DIR]

optional arguments:
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        the directory to write the images to (default: .)
```

### TO-IMAGES-OD
Dummy writer that just outputs images from object detection datasets.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-images-od [-o OUTPUT_DIR]

optional arguments:
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        the directory to write the images to (default: .)
```

### TO-SPECTRA-SC
Dummy writer that just outputs spectra from spectrum classification datasets.

#### Domain(s):
- **Spectrum Classification Domain**

#### Options:
```
usage: to-spectra-sc [-o OUTPUT_DIR]

optional arguments:
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        the directory to write the spectra to (default: .)
```

### TO-VOID-AC
Consumes audio classification instances without writing them.

#### Domain(s):
- **Audio classification domain**

#### Options:
```
usage: to-void-ac
```

### TO-VOID-IC
Consumes image classification instances without writing them.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: to-void-ic
```

### TO-VOID-IS
Consumes image segmentation instances without writing them.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: to-void-is
```

### TO-VOID-OD
Consumes object detection instances without writing them.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-void-od
```

### TO-VOID-SC
Consumes spectrum classification instances without writing them.

#### Domain(s):
- **Spectrum Classification Domain**

#### Options:
```
usage: to-void-sc
```

### TO-VOID-SP
Consumes speech instances without writing them.

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: to-void-sp
```

### WRITE-LABELS
ISP which gathers labels and writes them to disk

#### Domain(s):
- **Image Object-Detection Domain**
- **Audio classification domain**
- **Image Classification Domain**
- **Spectrum Classification Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: write-labels [-f {csv,csv-headless,list,json,json-pretty}] -o FILENAME

optional arguments:
  -f {csv,csv-headless,list,json,json-pretty}, --format {csv,csv-headless,list,json,json-pretty}
  -o FILENAME, --output FILENAME
                        the file into which to write the labels (default: None)
```