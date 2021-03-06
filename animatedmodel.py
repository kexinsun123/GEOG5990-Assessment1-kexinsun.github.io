#Import modes.
import random
import operator
import matplotlib
import matplotlib.pyplot
import matplotlib.animation 
import tkinter
import requests
import bs4
import agentframework
import csv

matplotlib.use('TkAgg')

#Get the y and x data from the site.
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
print(td_ys)
print(td_xs)

#Make sure the numbers of agents and iterations.
num_of_agents = 10
num_of_iterations = 100
agents = []

#Give the appropriate figuresize and axes.
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])
#ax.set_autoscale_on(False)

#Read in environment data.
environment=[]
f = open('in.txt', newline='')
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
for row in reader:
    reader=csv.reader(f,delimiter=' ')
    rowlist=[]
    for value in row:
        rowlist.append(int(value))
    environment.append(rowlist)
    print(value)
f.close() 

#Adjust the agent initialisation loop.
for i in range(num_of_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    agents.append(agentframework.Agent(x, y, environment, agents, 20))

carry_on = True	
	
def update(frame_number):
    
    fig.clear()   
    global carry_on
 
#Make agents interact with environment.   
    print("Move Eat and Share")
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours()
        print("Done agent", str(i), "out of", str(num_of_agents))
#    if random.random() < 0.1:
#        carry_on = False
#        print("stopping condition")    
    print("Plot")
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
    matplotlib.pyplot.imshow(environment)
    
#Adjust the animation.	
def gen_function(b = [0]):
    a = 0
    global carry_on 
    while (a < num_of_iterations) & (carry_on) :
        yield a			
        a = a + 1

#Display the model as an animation.
def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()

# Build the main window.
root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

#Set the GUI waiting for events.
tkinter.mainloop()
