Use this script to turn your Akta results file (.csv) into a nicely formatted pdf (to open in illustrator) and jpg.

Useage: python plotakta.py [options] filename. Here are the options you can use:
-c Overlay the Conductance trace
-b Overlay the %B trace
-l Overlay the Log (e.g. injection, elution, etc.)
-f Overlay the fractions from the Akta fractionator
-t Overlay and label the fractions from the Cetac fractionator
-o Only plot where fractions were collected (add -e if you only want elution fractions)
-e Only plot fractions that are marked as part of an elution
-m Draw a vertical line at the maximum UV
-h Show help message

An example: python plotakta.py -foe mypurification.csv. 
