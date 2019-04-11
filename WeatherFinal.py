"""

Weather Widget

Gets your ip address and uses it to work out an approximate location then gives you the
weather in that location all in a GUI window. Also option to search a city in a Country
and display the weather of the city you have entered. This code relies on geocoder for
location data and openweathermap for weather data. Error handling is in place for attempting
to use without internet connection, attempting to get weather more than once without clearing
or attempting to clear already destroyed canvases and entering an invalid city country combo
for the manual location entry method.

Joshua Utting

10/4/2019

This program relies on prior install of gecoder by [pip install geocoder]

"""

#Imports list
import geocoder
import requests
import json
from tkinter import *
import matplotlib.pyplot as plt
from PIL import Image,ImageTk
from io import BytesIO
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import http.client as httplib

canvasexist=0 #Define that no canvas exists yet

def have_internet(): #Define function to check if internet connection exists
    conn = httplib.HTTPConnection("www.google.com", timeout=1) #Define a connection to google servers and time out as 5 seconds
    try:
        conn.request("HEAD", "/") #Attempt to connect without returning data
        conn.close() #If connected close connection
        return True #have_internet returns true as connection was succesful
    except:
        conn.close() #Close connection after failed request
        return False #have_internet returns false as connection was unsuccesful

def internetpopupmsg(msg): #Define popup window function
    internettest = have_internet() #Check a second time to ensure no connection
    intpopup = Tk() #Define tkinter warning pop up window for no internet
    intpopup.wm_title("Error Warning") #Add a title to the window of error warning
    label = Label(intpopup, text=msg) #Show the warning message defined
    label.pack() #Pack the warning message to a window
    while(internettest==False): #While loop to continuously check the state of internet until it is detected to be on
        intpopup.update() #Used instead of mainloop as mainloop woud stop the program and not allow continuous checks, needed for window display
        internettest = have_internet() #Update the value of haveinternet by checking again
    intpopup.destroy() #When internet is detected close error warning
    return #Return to allow main program to run after internet detected

def canvaspopupmsg(msg): #Define popup window function
    popup = Tk() #Define tkinter pop up window for multiple clicks
    popup.wm_title("Error Warning") #Add a title to the window of error warning
    label = Label(popup, text=msg) #Show the warning message defined
    label.pack() #Pack the warning message to a window
    Okbutton = Button(popup, text="Ok", command = popup.destroy) #Add ok button which closes error message
    Okbutton.pack() #Pack ok button in pop up window
    popup.mainloop() #Keep this tkinter window open until destroyed by ok button
    
def coordspopupmsg(msg): #Define popup window function
    coordspopup = Tk() #Define tkinter pop up window for incorrect locations
    coordspopup.wm_title("Error Warning") #Add a title to the window of error warning
    label = Label(coordspopup, text=msg) #Show the warning message defined
    label.pack() #Pack the warning message to a window
    Okbutton = Button(coordspopup, text="Ok", command = coordspopup.destroy) #Add ok button which closes error message
    Okbutton.pack() #Pack ok button in pop up window
    coordspopup.mainloop() #Keep this tkinter window open until destroyed by ok button

#Define function to clear all existing canvases for redrawing
def clearcanvas(canvas,canvas2,canvas3,canvas4):
    global canvasexist #Dfeine canasexists as global
    canvas.get_tk_widget().destroy() #Destroy first canvas widget
    canvas2.get_tk_widget().destroy() #Destroy second canvas widget
    canvas3.get_tk_widget().destroy() #Destroy third canvas widget
    canvas4.destroy() #Destroy fourth canvas widget
    clearbutton.grid_remove() #Remove the clear button after it has been clicked as to not try and destroy undefined canvases
    canvasexist = 0 #Reset the canvas exists value to doesn't exist

#Define function for closing the program
def quitwindow():
    root.destroy() #Destro GUI window

#Define selecting dropdown option function
def change_dropdown(*args):
    global ans,city,country #Define globals for access
    ans=locvar.get() #Define answer of chosen dropdown option
    city=hidden_text.get() #Define chosen city as appropriate entry
    country=hidden_text2.get() #Define country as appropritae entry
    __main__() #Call Main plotting function

#Define function to hide extra options if wrong choice made from dropdowns
def hide(choice):
    if choice == "Enter City": #Condition to show entry fields if appropriate choice is made
        textfield.grid() #Show entry field for city
        textlabel.grid() #Show label for city entry field
        textfield2.grid() #Show entry field for country
        textlabel2.grid() #Show label for country entry field
    else: #If condition not met hide the entry fields and labels
        textfield.grid_remove() #Hide entry field for city
        textlabel.grid_remove() #Hide label for city entry field
        textfield2.grid_remove() #Hide entry field for country
        textlabel2.grid_remove() #Hide label for country entry field

def __main__(): #Define main plotting function
    global canvasexist #Define canvasexist value as global
    
    global clearbutton #Define the clear button as a global for use elsewhere
    api_key=str('08f1313bdc9cfc764e04711228fc95ce') #Define my API string for URL
    base_url = "http://api.openweathermap.org/data/2.5/weather?" #Define base URL for all cases
    
    if(ans=='Auto-Location'): #If code executed on auto-location call fetch IP location and weather
        g = geocoder.ip('me') #Take IP from device and run it through geocoder to get location
        lat = str(g.latlng[0]) #Define latitude from geocoder data
        long = str(g.latlng[1]) #Define longitude from geocoder data
        complete_url=base_url+"lat="+lat+"&lon="+long+"&appid="+api_key #Define full URL to look up weather for this case via openweathermap
        response = requests.get(complete_url) #Get the response from the website
        x=response.json() #Define x as the json data response
    else: #If code executed on manual city and country select use these values in IP
        complete_url=base_url+"q="+city+","+country+"&appid="+api_key #Define full URL to look up weather data from for this case via openweathermap
        response = requests.get(complete_url) #Get the response from the website
        x=response.json() #Define x as the json data response
     
    try:    
        y=x["main"] #Define y as the main section of the json data
        current_temp = y["temp"] #Define current temperature from the main section
        current_pressure = y["pressure"] #Define current pressure from the main section
        current_humidity = y["humidity"] #Define current humidity from the main section
        z = x["weather"] #Define weather a z from the weather section of the json data
        weather_description = z[0]["description"] #Define a description of the weather from z
        weather_code = z[0]["icon"] #Define an image code to match description of weather from z
    except:
        coordspopupmsg('Error: Location not found.\nPlease ensure your entry is valid.\nEnsure country format is ISO 3166-1 alpha-2.')
        return
    
    canvasexist = canvasexist+1 #Increase canvasexist to by 1
    if(canvasexist==1): #Run the data fetching and plotting if get weather has only been for the irst time or previous canvas cleared
            weather_description = weather_description.title() #Capitalise first letter of each word in weather_description
            
            current_temp=float(current_temp-271.15) #Convert temperature to Celsius from Kelvin and add 2 degrees based on empirical running and comparing to other sites (value - 273.15 +2)
            
            weathericon = "http://openweathermap.org/img/w/"+weather_code+".png" #Find image by its code on openweathermap
            imageresponse = requests.get(weathericon) #Get the image response from the site
            image=Image.open(BytesIO(imageresponse.content)) #Open the image for use in the program
            
            f=Figure(figsize=(3,3)) #Define first figure with appropriate size
            a=f.add_subplot(111) #Add subplot to figure
            a.imshow(image) #Plot the image on axes
            a.axis('off') #Switch off the plot axes for the image
            a.set_title(weather_description) #Plot title on weather condition image as the description
            
            canvas = FigureCanvasTkAgg(f, master=root) #Create canvas in GUI with figure on it
            canvas.get_tk_widget().pack(side="top", fill="both", expand=1) #Pack canvas widget in GUI and allow to expand to fit graphs
            canvas._tkcanvas.pack(side="top", fill="both", expand=1) #Pack canvas in GUI and allow to expand to fit graphs
            
            f2=Figure(figsize=(10,1)) #Define second figure with appropriate size
            a2=f2.add_subplot(111) #Add subplot to figure
            a2.set_title('Current Temperature %s°C' % str(int(current_temp))) #Set title on plot as current temperature rounded to the nearest degree
            x=np.arange(-50,current_temp,0.01) #Define the x values of the plot every 0.01 degrees up to current temperature value
            y=[1]*len(x) #Match the length of the y array to the x array for whatever length it becomes, the value doesn't matter as long as it's constant
        
            cmap = matplotlib.cm.get_cmap('inferno') #Get matplotlib colourmap for tmperature graph
            normalize = matplotlib.colors.Normalize(-50, vmax=50) #Normalise the colourmap between the minimum and maximum temperatures the graph will plot
            colors = [cmap(normalize(value)) for value in x] #Divide the colour values up for each value in x and assign each x value one
            a2.scatter(x, y, color=colors) #Plot a scatter graph of the colours (scatter chosen to allow colour mapping) but will simulate straight line because of y values
            a2.set_xlim(-50,50) #Plot the x limits for a default range to show clearer the graph of temperature
            a2.set_xlabel('Temperature (°C)') #Label the x axis to explain what it is showing
            a2.set_yticklabels([]) #Hide the y tick labels as they are arbitrary
            f2.tight_layout() #Stop the labels and graphs from overlapping
            
            canvas2 = FigureCanvasTkAgg(f2, master=root) #Create canvas in GUI with figure on it
            canvas2.get_tk_widget().pack(side="top", fill="both", expand=1) #Pack canvas widget in GUI and allow to expand to fit graphs
            canvas2._tkcanvas.pack(side="top", fill="both", expand=1) #Pack canvas in GUI and allow to expand to fit graphs
            
            f3=Figure(figsize=(10,1)) #Define third figure with appropriate size
            a3=f3.add_subplot(111) #Add subplot to figure
            humidityx = np.arange(0,current_humidity,1) #Define the x values of the plot every 1% up to current humidity value
            humidityy = [1]*len(humidityx) #Match the length of the y array to the x array for whatever length it becomes, the value doesn't matter as long as it's constant
            a3.plot(humidityx,humidityy,linewidth=15) #Plot line graph for x and y values with thick bar to make easily visible as a percentage full of its axes
            a3.set_xlim(0,100) #Set the x limits for the percentage
            a3.set_xlabel('Humidity (%)') #Label x axis to clearly explain what it is showing
            a3.set_yticklabels([]) #Hide the y tick labels as they are arbitrary
            a3.set_title('Current Humidity %s%%' % str(current_humidity)) #Plot title on graph stating current humidity
            f3.tight_layout() #Stop labels and graphs from overlapping
            
            canvas3 = FigureCanvasTkAgg(f3, master=root) #Create canvas in GUI with figure on it
            canvas3.get_tk_widget().pack(side="top", fill="both", expand=1) #Pack canvas widget in GUI and allow to expand to fit graphs
            canvas3._tkcanvas.pack(side="top", fill="both", expand=1) #Pack canvas in GUI and allow to expand to fit graphs
        
            canvas4 = Canvas(master=root) #Create normal blank canvas
            canvas4.pack(side='bottom',expand=1) #Pack the new canvas at the bottom of the GUI window
        
            if(ans=='Auto-Location'): #If auto-location was picked fill in string to show on canvas
                string1 = ('\nPressure at latitutde: %s and lonigutde: %s is %s millibar' %(lat,long,current_pressure)) #Define string showing pressure at automatic coordinates
                canvas4.create_text(200,10,text=string1) #Create text on the final canvas of the chosen string
            else: #If manual location was picked fill in string to show on canvas
                string2 = ('\nPressue in %s is %s millibar' % (city,current_pressure)) #Define string showing pressure at city entered
                canvas4.create_text(200,10,text=string2) #Create text on the final canvas of the chosen string
                
            canvas.show() #Show canvas 1
            canvas2.show() #Show canvas 2
            canvas3.show() #Show canvas 3   
                
            clearbutton=Button(dataframe,text='Clear',command=lambda: clearcanvas(canvas,canvas2,canvas3,canvas4)) #Show clear canvas button but only when a canvas has been plotted to avoid lack of definition
            clearbutton.grid(row=2,column=2) #Define location of clearn button
    
    else: #If canvas has not been cleared before replotting show popup
        canvaspopupmsg('Please clear current canvas before plotting again') #If attempting to plot a second time without clearnin
    return #Return from plotting function back to tkinter mainloop

internet = have_internet() #Test if connected to the internet
if(internet==True): 
    pass #If connection established carry on with main program
else:
    #Call ine no internet popup message function with following error message
    internetpopupmsg('This program requires internet connection.\nConnection not detected, please connect to continue.\nThis message will close automatically when internet connection is detected.')
    
root = Tk() #Define Tkinter interface by root

root.title('Weather Interface') #Set GUI title
dataframe = Frame(root) #Create frame for entry data
dataframe.pack(side=TOP) #Pack frame at top of GUI window

locvar=StringVar() #Define location variable as string
choices = {'Auto-Location','Enter City'} #Define drop down menu choices
locvar.set('Auto-Location') #Set default value to auto-location

hidden_text = StringVar() #Create string class for entry value
hidden_text.set('Manchester') #Set default entry value for field
hidden_text2 = StringVar() #Create string class for entry value
hidden_text2.set('GB') #Set default entry value for field

textfield = Entry(dataframe, textvariable = hidden_text) #Create text field linked to the hidden text field 
textlabel = Label(dataframe,text = 'Enter City') #Create label in dataframe for hidden text entry field              

textfield2 = Entry(dataframe, textvariable = hidden_text2) #Create text field linked to the second hidden text field 
textlabel2 = Label(dataframe,text = 'Enter Country') #Create label in dataframe for second hidden text entry field              

textfield.grid(row=1,column=1) #Align entry space in second column of second row of frame
textfield.grid_remove() #Hide the entry field from the grid by default
textlabel.grid(row=1,column=0) #Align label space for hidden label in first column of second row
textlabel.grid_remove() #Hide the text field label from the grid by default

textfield2.grid(row=2,column=1) #Align entry space in second column of third row
textfield2.grid_remove() #Hide the entry field from the grid by default
textlabel2.grid(row=2,column=0) #Align label space for hidden label in first column of third row
textlabel2.grid_remove() #Hide the entry field label from the grid by default

dropmenu = OptionMenu(dataframe,locvar,*choices,command=hide) #Define drop menu with choices set earlier linked to display the value of locvar and linked to the hide fields command
label = Label(dataframe,text='Choose Location Type').grid(row=0,column=0) #Define label for drop menu and pack it to the first row and first column
dropmenu.grid(row=0,column=1) #Pack drop menu to second column in the first row

button = Button(dataframe,text='Get Weather', command = change_dropdown) #Define get weather button to trigger start of plotting linked to the change_dropdown function
button.grid(row=0,column=2) #Pack the button to the third column of the first row

quitbutton = Button(dataframe,text='Quit', command = quitwindow) #Define quit button and link it to the quitwindow function
quitbutton.grid(row=1,column=2) #Pack the quit button the third column of the second row

root.mainloop() #Define end of tkinter loop