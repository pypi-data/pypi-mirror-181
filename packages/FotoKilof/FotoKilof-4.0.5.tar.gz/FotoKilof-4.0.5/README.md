# FotoKilof - GUI for ImageMagick

GUI for the most used (by me) ImageMagick functionality for processing pictures. 

## Screenshots

### Linux

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof.png)

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof2.png)

### Mac OSX

![Screenshot MacOS](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_macos.png)

### Windows

![Screenshot Windows](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_windows11.png)

## Graphics conversion

 - scaling/resize,
 - crop,
 - text annotation, inside or outside of picture (mems generator),
 - border around picture,
 - rotation,
 - mirroring (verticl or horizontal)
 - black-white or sepia,
 - contrast increase/decrease or normalize or histogram stretching,
 - color auto-level or equalize,
 - adding logo image o picture,
 - file formats: JPG, PNG, TIFF, SVG
 - format conversion into JPG, PNG, TIFF.

## Functionality:

 - processing JPG, PNG, SVG and TIFF images,
 - processing picture in the fly, originals are safe,
 - processing single file or whole directory,
 - take screenshot (Linux) or get picture from clipboard (Windows and MacOS) and use it as source picture,
 - after processing results is copied into clipboard (Windows),
 - display selected tools,
 - tools selection,
 - preview orignal and result,
 - predefined rotation: 90, 180 and 270 degree or custom,
 - crop selection via click on preview or coordinates,
 - crop coordinates:
   - two corners (upper left and lower right),
   - upper left corner and width plus height,
   - gravity, width plus height plus offset,
 - text: color, font and size selection, background
 - text position:
   - outside: top/bottom, left/center/right
   - inside: by gravity or by position
 - customized sepia,
 - equalize by channel,
 - contrast between -3 and +3,
 - customized contrast stretching,
 - histograms of original and result pictures,
 - fast file navigation: First, Prev, Next, Last,
 - own command editor,
 - own command can be composed from executed commands,
 - is possible to use other ImageMagick commands, eg. *-gaussian-blur* etc.,
 - logging conversion,
 - GraphickMagick is supported partialy.

## User manual

- PDF: [English](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/doc/en/fotokilof.pdf), [Polish](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/doc/pl/fotokilof.pdf).
- MD: [English](doc/en/fotokilof.md), [Polish](doc/pl/fotokilof.md).

## Available translations

Available: English, Polish, German, Bulgarian and Indonesian.

## Install and run

### Requirements

- Windows, Linux, MacOS X, BSD,
- FullHD screen for comfort work,
- [ImageMagick](https://imagemagick.org/), remember to add path into `%PATH%` environment variable, enable install libraries!
- [Python](https://www.python.org/), remember to add path into `%PATH%` environment variable.

### Install

Install as PyPi package by PIP:
```bash
python3 -m pip install wand fotokilof
```

for Windows:
```bash
python -m pip install pywin32 wand fotokilof
```

### Upgrade

```bash
python3 -m pip install --upgrade fotokilof
```

### Run

```bash
fotokilof
```

## Thanks

 - Friends - some ideas and testing,
 - Max von Forell - German translation,
 - Bozhidar Kirev - Bulgarian translation,
 - Alexander Ignatov - Bulgarian translation,
 - Afif Hendrawan - Indonesian translation,
 - Sebastian Hiebl - python packaging,
 - Matt Sephton - ideas for packing gui,
 - emsspree - update german translation, jpeg,
 - Olm - testing on Windows,
 - Carbene Hu - idea to fix issue
 - Mert Cobanov - Turkish translation

---

![Python powered](python-powered.png)
