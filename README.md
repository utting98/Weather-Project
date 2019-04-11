# Weather-Project
Python project to create a widget that can get automatic location and choose manual city entry then display the weather conditions for that location.

This project requires an install of geocoder by:
pip install geocoder

Program is GUI based so should be self explanatory.

To use:
Choose either auto-location or enter city from drop down box
After your selection choose get weather
After verifying entry is valid weather conditions, image to describe weather, temperature graph, humidity graph and pressure will be plotted in tkinter canvas to display
If you want to choose another location and run again select the clear button and follow line 7 & 8 again
When done press quit to close program

Known bugs that have been fixed in last edit:
  Prevented crashes with no internet (this program requires internet connection) with warning message if no internet detected,            message closes automatically when internet is detected
  Prevented crashes with nonsense entry to city or country by interrupting after attempted data acquisition with warning to user that entry was invalid
  Prevented crashes with clicking get weather multiple times by interrupting plotting process with warning that you need to clear the canvas before plotting again
  Prevented crashes with pressing clear multiple times removing clear button after initial click until more data is plotted
