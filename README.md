# Plot Akta

Use this script to turn your Akta results file (.csv) into a nicely formatted pdf (to open in illustrator) and png. It will plot the UV trace, but additional data can be overlaid (see below).

Usage:

```
plotakta.py [options] filename.csv
```

## Getting Started

* Make sure you have Python 3 installed and have the **numpy** and **matplotlib** packages.

* Export your Akta results file as a .csv file. Avoid spaces in the filename.

## Options

* ```-c``` Overlay the Conductance trace

* ```-b``` Overlay the %B trace

* ```-l``` Overlay the Log (e.g. injection, elution, etc.)

* ```-f``` Overlay the fractions from the Akta fractionator

* ```-t``` Overlay and label the fractions from the Cetac fractionator

* ```-o``` Only plot where fractions were collected (add *-e* if you only want elution fractions)

* ```-e``` Only plot fractions that are marked as part of an elution

* ```-m``` Draw a vertical line at the maximum UV

* ```-h``` Show help message

Options can be combined together without putting a new dash every time (e.g. ***-cbf***)

## Examples

UV trace only, fractions labeled, zoomed into the elution fractions (for elution details):

```
python plotakta.py -foe mypurification_results.csv
```

![Example plot -foe](./Examples/Option-foe.png "Example plot -foe")

UV trace, %B trace, and log overlaid (for purification overviews):

```
python plotakta.py -bl mypurification_results.csv
```

UV trace, conductance trace, and fractions labeled:

```
python plotakta.py -cf mypurification_results.csv
```

## Updates

* 2020-02-24 - Version 1.1 - Bug fixes.

* 2020-02-23 - Version 1.0

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
