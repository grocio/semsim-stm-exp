#!/bin/sh
# Removing rows that contain " or '
sed -e "/'/d" -e '/"/d' ../Norms/strength.SWOW-EN.R123.csv > ../CSVNorms/cleansedStrength.csv
