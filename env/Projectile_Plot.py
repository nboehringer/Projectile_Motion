from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import numpy
from math import *

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

def makeform(root, fields, inputs):
   entries = {}
   count = 0
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0, inputs[count])
      row.pack(side=BOTTOM, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
      count += 1
   return entries


class Window(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)               
		self.master = master
		self.run = 0
		self.init_window()

	def init_window(self):
		self.pack(fill=BOTH, expand=1)
		
		# Initializing the data table
		columns = ('Max Distance (m)', 'Max Height (m)', 'Time (sec)')
		DT = Treeview(self)
		DT['columns'] = columns
		DT.heading("#0", text='Run Number', anchor='w')
		DT.column("#0", anchor="w", width=100)
		for column in columns:
			DT.heading(column, text=column)
			DT.column(column, anchor='center', width=100)
			DT.pack(side=BOTTOM,anchor='s')

		# Setting up inputs in a dict and 
		fields = ('Drag Coefficient','Mass (kg)', 'Diameter (m)', 'Velocity (m/s)', 'Angle (degrees)', 'Height (m)')
		inputs = ["0.3","2",".25","100","45","0"]
		self.ent = makeform(self, fields, inputs)

		# Label and drop down menu
		lab = Label(self,text='Planet Gravity')
		planets = StringVar()
		planets.set('Earth')
		self.ent['Gravity'] = planets # adds selection varible to dict
		drop = OptionMenu(self,planets,'Earth','Moon','Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto')
		
		# Air Risistance checkbox
		self.ent['Air'] = IntVar()
		C1 = Checkbutton(self, text='Air Resistance', variable=self.ent['Air'])
		   
		clearButton = Button(self, text="Graph on New",command=(lambda: self.graph_array(DT, 1)))
		clearButton.pack(side=TOP, anchor='n')

		graphButton = Button(self, text="Graph on Current",command=(lambda: self.graph_array(DT)))
		graphButton.pack(side=TOP, anchor='n')

		graphButton = Button(self, text="Show Error Box Test",command=(lambda: self.Error_nonint('Velocity (m/s)')))
		graphButton.pack(side=TOP, anchor='n')

		lab.pack(side=LEFT,anchor='s')
		drop.pack(side=LEFT,anchor='s')
		C1.pack(side=LEFT,anchor='s',padx=20)


	def graph_array(self, DT, clear=0):
		self.run += 1

		# Setting varible for calculations from inputs
		vi = self.nonint('Velocity (m/s)')#float(self.ent['Velocity (m/s)'].get())
		ai = float(self.ent['Angle (degrees)'].get())
		hi = float(self.ent['Height (m)'].get())
		mass = float(self.ent['Mass (kg)'].get())
		di = float(self.ent['Diameter (m)'].get())
		Cd = float(self.ent['Drag Coefficient'].get())

		# Selection of gravity based off planet
		gravity = {'Earth':9.81,'Moon':1.623,'Sun':274.88,'Mercury':3.728,'Venus':8.868,'Mars':3.689,'Jupiter':24.82,
					'Saturn':10.497,'Uranus':8.731,'Neptune':11.18,'Pluto':0.657}
		g = gravity[self.ent['Gravity'].get()]

		if clear == 1:
			plt.clf()

		if self.ent['Air'].get() == 0:
			pAir = 0
		else:
			Air = {'Earth':1.225,'Moon':0,'Sun':0,'Mercury':0,'Venus':0,'Mars':0,'Jupiter':0,
					'Saturn':0,'Uranus':0,'Neptune':0,'Pluto':0}
			pAir = Air[self.ent['Gravity'].get()]   # kg/m^3 Density of Air at sea level at 15C
		
		A = pi*(di/2)**2 # cross section area of ball
		K = (1/2)*pAir*Cd*A/mass # Total resultant force of drag
		Th = ai * pi / 180

		# Calculations
		# Initial position, velocity, and acceleration
		v_x, v_y, a_x, a_y, x, y = [], [], [], [], [0], [hi]
		delta_t = 0.01
		t = 0

		while y[-1] >= 0:
			t += delta_t
			v_x = vi*cos(Th)*exp(-K*t)
			if pAir is not 0:
				v_y = ((K*vi*sin(Th)+g)*exp(-K*t)-g)/K
			else:
				v_y = vi*sin(Th)*exp(-K*t)
			x.append(abs(v_x * t))
			y.append((-.5*g*(t**2)) + (v_y*t) + hi)
		y[len(y)-1] = 0

		DT.insert('', 'end', text=str(self.run), values=(str(int(max(x))), str(int(max(y))), str(int(t))))

		plt.plot(x, y)
		plt.xlabel('Distance (m)')
		plt.ylabel('Height (m)')
		plt.axis('Normal')
		plt.title('Projectile Motion')
		plt.text(0, max(y), ' Run: %d' % self.run , verticalalignment='top', horizontalalignment='left')
		plt.show()


	def nonint(self, input):
		try:
			return float(self.ent[input].get())
		except:
			messagebox.showwarning("Non Int Value","Expected Input Type: Number")

root = Tk()
app = Window(root)
root.mainloop()