## PROJECT ##

* ID: **T**humbnail!**M**AKER
* Contact: git@schepsen.eu

## DESCRIPTION ##

**T**humbnail!**M**AKER creates customisable thumbnails and adds some tech details in the picture's header

## DEPENDENCIES ##

Attention: Don't forget to install these additional apps

* ffmpeg
* imagemagick

```
pip install -r requirements.txt
```

## USAGE ##

usage: tnmake -i path [-o path] [-w px] [-c annotation] [--grid layout] [-e {bmp,jpg,png}] [-q x] [-f path] [-s px]

Thumbnail!MAKER creates thumbnails with some additional information

options:
  -h, --help

  * show this help message and exit

  -i path, --input path

  * set video filepath

  -o path, --output path

  * force a custom output filepath

  -w px, --width px

  * set width of the output image

  --comment annotation

  * append a thumbnail annotation

  --grid layout

  * set layout of the output thumbnail

  -e {bmp,jpg,png}, --extension {bmp,jpg,png}

  * choose the output extension (default: "jpg")

  -q x, --quality x

  * set quality, affects lossy image formats only

  -f path, --font path

  * select an available font or pass a path to a desired fontfile

  -s px, --size px

  * set desired fontsize (default: 13px)

  -v, --verbose

  * enable verbose mode

  -V, --version

  * show program's version number and exit


### EXAMPLES ###

```
tnmake -i "Blade Runner (1982) Original.mkv" -w 750 -c "This is useful for adding small annotations (such as text labels)"
```

## CHANGELOG ##

### Thumbnail!MAKER 0.2.0, updated @ 2022-11-03 ###

* pack the project into a `pip` package ([visit](https://pypi.org/project/tnmake/))

### Thumbnail!MAKER 0.1.1, updated @ 2020-01-14 ###

* add support for `embedded` subtitles

### Thumbnail!MAKER 0.1.0, updated @ 2020-01-13 ###

* initial release
