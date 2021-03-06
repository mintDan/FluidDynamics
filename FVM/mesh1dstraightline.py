"""

solving convection

ut + ... = 0

evt bruge hældningskeofficnet a1 = -1/a2

Kan også ændre det til classes i stedet for dict måske


to do:
should probably spliut up setting velocity and height to two functions

Dan Krog
"""
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
import Fluxes





def MakeCell(Cell,a,b,xrange,indstart,dx):
	#y = ax + b
	#dx = 1
	
	L = np.sqrt(dx**2+a**2*dx**2)
	
	angle = np.arctan(a)
	r = np.sqrt(2)*L/2
	print("Angle")
	print(angle)
	indstart = 0
	for i in range(indstart,indstart+len(xrange)):
		j = i
		
		xc = xrange[i-indstart]
		yc = a*xrange[i-indstart]+b
		
		#Jeg laver sikkert ikke disse rotations ordentligt, perhaps...
		#måske skal jeg full on bruge roationsmatrix
		
		#skal faktisk rotate vectors, kan man sige, men de beholder deres end point... maybe
		#Men, de bliver også lidt længere, pga y=ax+b
		#
		
		#Vi skal også plotte normal vectors
		
		
		#Man kan loop meget bedre over en dict end jeg gør nu
		
		#Lad os se hvad vi har lige nu
		#ved 45*, for (0,0)
		#så skal x0 = 0, right?
		#og x3 = 0
		#Og x1,x2 = r, right?
		
		#De her cos,sin calculations behøver jeg jo kun lave en enkelt gang for hver slope, tager meget cpu time
		x0 = xc + r*np.cos(5*np.pi/4+angle)
		x1 = xc + r*np.cos(7*np.pi/4+angle)
		x2 = xc + r*np.cos(1*np.pi/4+angle)
		x3 = xc + r*np.cos(3*np.pi/4+angle)
		
		y0 = yc + r*np.sin(5*np.pi/4+angle)
		y1 = yc + r*np.sin(7*np.pi/4+angle)
		y2 = yc + r*np.sin(1*np.pi/4+angle)
		y3 = yc + r*np.sin(3*np.pi/4+angle)
		
		
		Cell["{}".format(i)] = {
			"Node":[xc,yc],
			"Corners":[[x0,y0],[x1,y1],[x2,y2],[x3,y3]],
			"V":L*L}
			
		#plt.plot([x0,x1,x2,x3,x0],[y0,y1,y2,y3,y0],color="black")
		#plt.scatter(xc,yc,color="black")



def MakeSidesAndNormalVectors(Cell):
	"""
	Måske sæt normalvector ind under side1, så har vi "Side1" = {"Side","Normalvector","Velocity","Height"}
	"""
	
	for index in Cell:
		Side1=[
		[Cell[index]["Corners"][0][0],Cell[index]["Corners"][1][0]], #x
		[Cell[index]["Corners"][0][1],Cell[index]["Corners"][1][1]], #y
		0,	#velocity
		0,	#height
		0, 	#Flux density
		]

		Cell[index]["Side1"] = Side1
		
		Cell[index]["Normalvector1"] = [Cell[index]["Corners"][1][1]-Cell[index]["Corners"][0][1], #dy
										-(Cell[index]["Corners"][1][0]-Cell[index]["Corners"][0][0])]
		
		
		
		Side2=[
		[Cell[index]["Corners"][1][0],Cell[index]["Corners"][2][0]], #x
		[Cell[index]["Corners"][1][1],Cell[index]["Corners"][2][1]],  #y
		0,	#velocity
		0,	#height
		0, 	#Flux density
		]
		
		Cell[index]["Side2"] = Side2
		
		
		Cell[index]["Normalvector2"] = [Cell[index]["Corners"][2][1]-Cell[index]["Corners"][1][1],
										-(Cell[index]["Corners"][2][0]-Cell[index]["Corners"][1][0])]
		
		Side3=[
		[Cell[index]["Corners"][2][0],Cell[index]["Corners"][3][0]], #x
		[Cell[index]["Corners"][2][1],Cell[index]["Corners"][3][1]], #y
		0,	#velocity
		0,	#height
		0, 	#Flux density
		]

		Cell[index]["Side3"] = Side3
		
		
		Cell[index]["Normalvector3"] = [
								Cell[index]["Corners"][3][1]-Cell[index]["Corners"][2][1], #dy
								-(Cell[index]["Corners"][3][0]-Cell[index]["Corners"][2][0]) #-dx
								]
		
		Side4=[
		[Cell[index]["Corners"][3][0],Cell[index]["Corners"][0][0]], #x
		[Cell[index]["Corners"][3][1],Cell[index]["Corners"][0][1]], #y
		0,	#velocity
		0,	#height
		0, 	#Flux density
		]

		Cell[index]["Side4"] = Side4
		
		Cell[index]["Normalvector4"] = [
								Cell[index]["Corners"][0][1]-Cell[index]["Corners"][3][1], #dy
								-(Cell[index]["Corners"][0][0]-Cell[index]["Corners"][3][0]) #-dx
								]

def PlotCell(Cell):
	for index in Cell:
		plt.plot([
		Cell[index]["Corners"][0][0],
		Cell[index]["Corners"][1][0],
		Cell[index]["Corners"][2][0],
		Cell[index]["Corners"][3][0],
		Cell[index]["Corners"][0][0]],
		[
		Cell[index]["Corners"][0][1],
		Cell[index]["Corners"][1][1],
		Cell[index]["Corners"][2][1],
		Cell[index]["Corners"][3][1],
		Cell[index]["Corners"][0][1]],
		color="black")
		plt.scatter(Cell[index]["Node"][0],Cell[index]["Node"][1],color="black")
									
	
def PlotNormalVectors(Cell):
	for index in Cell:
		#JEg skal btw lige displace dem, jo...
		#Lige nu bliver de plottet fra (0,0) de skal displaces mere generally til side edges
		#De skal displaces til average af corners, tror jeg
		x1 = 0.5*(Cell[index]["Corners"][0][0]+Cell[index]["Corners"][1][0])
		y1 = 0.5*(Cell[index]["Corners"][0][1]+Cell[index]["Corners"][1][1])
		
		
		plt.plot([x1,x1+Cell[index]["Normalvector1"][0]],
		[y1,y1+Cell[index]["Normalvector1"][1]],color="black")
		
		
		
		x1 = 0.5*(Cell[index]["Corners"][1][0]+Cell[index]["Corners"][2][0])
		y1 = 0.5*(Cell[index]["Corners"][1][1]+Cell[index]["Corners"][2][1])
		
		
		plt.plot([x1,x1+Cell[index]["Normalvector2"][0]],
		[y1,y1+Cell[index]["Normalvector2"][1]],color="black")
		
		
			
		x1 = 0.5*(Cell[index]["Corners"][2][0]+Cell[index]["Corners"][3][0])
		y1 = 0.5*(Cell[index]["Corners"][2][1]+Cell[index]["Corners"][3][1])
		
		
		plt.plot([x1,x1+Cell[index]["Normalvector3"][0]],
		[y1,y1+Cell[index]["Normalvector3"][1]],color="black")
		
			
		x1 = 0.5*(Cell[index]["Corners"][3][0]+Cell[index]["Corners"][0][0])
		y1 = 0.5*(Cell[index]["Corners"][3][1]+Cell[index]["Corners"][0][1])
		
		
		plt.plot([x1,x1+Cell[index]["Normalvector4"][0]],
		[y1,y1+Cell[index]["Normalvector4"][1]],color="black")
		
		#plt.plot(Cell["{}".format(i)]["Normalvector2"][0],Cell["{}".format(i)]["Normalvector2"][1],color="black")
		#plt.plot(Cell["{}".format(i)]["Normalvector3"][0],Cell["{}".format(i)]["Normalvector3"][1],color="black")
		#plt.plot(Cell["{}".format(i)]["Normalvector4"][0],Cell["{}".format(i)]["Normalvector4"][1],color="black")

def PlotHeights(Cell):
	"""
	Let's take node x coordinate and height and put them into arrays
	"""
	Nx = len(Cell)
	xcoords = np.zeros(Nx)
	ycoords = np.zeros(Nx)
	id = 0
	for i in Cell:
		#plt.scatter(Cell[i]["Node"][0],Cell[i]["U"],color="black")
		xcoords[id] = Cell[i]["Node"][0]
		ycoords[id] = Cell[i]["U"]
		id += 1
	plt.plot(xcoords,ycoords,color="black")
	
def MatchVolumes(Cell1,Cell2):
	"""
	matches 2 different lines, glues their edges together and makes a quadrilateral volume
	"""
	#print(Cell1["4"]["Corners"])
	#print(Cell2["0"]["Corners"])
	
	#print(Cell1["4"]["Corners"][1])
	#print(Cell1["4"]["Corners"][2])
	
	#print(Cell2["0"]["Corners"][3])
	#print(Cell2["0"]["Corners"][0])
	
	#plt.plot([Cell1["4"]["Corners"][1][0],Cell2["0"]["Corners"][0][0]],
	#		[Cell1["4"]["Corners"][1][1],Cell2["0"]["Corners"][0][1]],
	#		color="black")
			
	#plt.plot([Cell1["4"]["Corners"][2][0],Cell2["0"]["Corners"][3][0]],
	#		[Cell1["4"]["Corners"][2][1],Cell2["0"]["Corners"][3][1]],
	#		color="black")
			
			
			

	Cell1length = len(Cell1)
	print(Cell1length)
	#Creating glue/intersection cell
	Cell1["{}".format(Cell1length)] = {"Node":[5,5]}
	Cell1["{}".format(Cell1length)]["Corners"] = [
	Cell1["4"]["Corners"][1],
	Cell2["0"]["Corners"][0],
	Cell2["0"]["Corners"][3],
	Cell1["4"]["Corners"][2]
	]
	
	#Let's calc V
	#https://en.wikipedia.org/wiki/Quadrilateral
	#We need diagonals
	
	#Diag1 -> x2 - x0
	#Diag2 -> x3 - x1
	D1 = [Cell1["{}".format(Cell1length)]["Corners"][2][0]-Cell1["{}".format(Cell1length)]["Corners"][0][0],
	Cell1["{}".format(Cell1length)]["Corners"][2][1]-Cell1["{}".format(Cell1length)]["Corners"][0][1]]
	
	D2 = [Cell1["{}".format(Cell1length)]["Corners"][3][0]-Cell1["{}".format(Cell1length)]["Corners"][1][0],
	Cell1["{}".format(Cell1length)]["Corners"][3][1]-Cell1["{}".format(Cell1length)]["Corners"][1][1]]
	
	V = 0.5*(D1[0]*D2[1]-D2[0]*D1[1])
	#print("volume")
	#print(V)
	Cell1["{}".format(Cell1length)]["V"] = V

def SetNodeHeight(Cell,U,v,Nx,dx):
	"""
	Only for the node. later we will extrapolate to edges of the control volume sides/edges
	
	Btw, this is atm setting INITIAL height only. So this is pretty much initial condition...
	
	"""
	j = 0
	for i in Cell:
		#j += 3
		#if "i" == "0":
			#periodic?
		#	pass
		#if "i" == "{}".format(Nx):
			#periodic?
		#	pass
		
		#Cell[i]["U"] = U+np.cos(j*2)
		Cell[i]["U"] = U + np.cos(10*j*dx/(2*np.pi)-20/(2*np.pi))
		Cell[i]["Unew"] = 0
		j += 1

				
def SetFluxDensity(Cell):
	"""
	The 4th index of "Side" refers to the flux density, 3 is height, 2 is velocity, so 2*3 -> height*velocity
	
	We want to do it upstream,right?
	Actually, it's the height initialization that has to be upstream
	
	Flux density is called after setting height 
	"""
	print("Setting FluxDensity")
	for i in Cell:
		#Cell[index]["Side1"][4] = Cell[index]["Side1"][3]*Cell[index]["Side1"][2]
		Cell[i]["Side2"][4] = Cell[i]["Side2"][3]*Cell[i]["Side2"][2]
		#Cell[index]["Side3"][4] = Cell[index]["Side3"][3]*Cell[index]["Side3"][2]
		Cell[i]["Side4"][4] = Cell[i]["Side4"][3]*Cell[i]["Side4"][2]
		
		#print(Cell[i]["Side2"][4])
		#Okay... side4 height er 0...
		print("Height of side4 {}".format(Cell[i]["Side4"][3]))
		


def UpdateU(Cell,dt):
	"""
	Continuity equation
	for 1d in straight line, we use only side2 and side4
	
	Unew = U - fac*(FluxDensity2*Vector2 + FluxDensity4*Vector4)
	
	[4] er flux density
	"""
	for i in Cell:
		fac = dt/Cell[i]["V"]
		
		Cell[i]["Unew"] = Cell[i]["U"]-fac*(
		Cell[i]["Side2"][4]*Cell[i]["Normalvector2"][0]+
		Cell[i]["Side4"][4]*Cell[i]["Normalvector4"][0]
		)
		
		
		#print("Side2 -> {}".format(Cell[i]["Side2"][4]*Cell[i]["Normalvector2"][0]))

		#print("Side4 -> {}".format(Cell[i]["Side4"][4]*Cell[i]["Normalvector4"][0]))

	
	for i in Cell:
		Cell[i]["U"] = Cell[i]["Unew"]

def Updatev(Cell,dt):
	"""
	Momentum equation
	Right now we just set v constant
	"""
	
def UpdateTimeStep(Cell,dt):
	
	for i in Cell:
		Cell[i]
		if dttest < dt:
			dt = dttest
			#er dette hurtigere måske ? dt = min(dttest,dt)
			#i stedet for if statement? dunno
			#måske overhead med at call min function
	return
	
if __name__ == "__main__":
	
	x0 = 0
	x1 = 4
	y0 = 0
	y1 = 10
	x = np.linspace(x0,x1,11)
	y = np.linspace(y0,y1,11)
	
	Cell = {}
	Nx = 20
	x1range = np.linspace(0,4,Nx)
	dx = x1range[1]-x1range[0]
	#dx = (x1-x0)/(Nx+1) #Tror faktisk det skal være Nx-1?
	a = 0
	b = 0
	#Bør faktisk include x-range.... fordi det er line segments...
	
	MakeCell(Cell,a,b,x1range,0,dx)
	MakeSidesAndNormalVectors(Cell)
	
	print("Lenght of Cell is {}".format(len(Cell)))
	
	U = 3
	v = 1
	dt = dx/v
	SetNodeHeight(Cell,U,v,Nx,dx) #Initial height
	#Initial
	#SetSideHeightAndVelocity(Cell,U,v,Nx)
	Fluxes.SetSideHeightAndVelocityBothSides(Cell,U,v,Nx)
	SetFluxDensity(Cell)
	
	
	runtime = 3
	for nt in range(runtime):
		UpdateU(Cell,dt)
		#SetSideHeightAndVelocity(Cell,U,v,Nx)
		#SetSideHeightAndVelocityLinear(Cell,U,v,Nx)
		#SetSideHeightAndVelocityQuadratic(Cell,U,v,Nx)
		Fluxes.SetSideHeightAndVelocityBothSides(Cell,U,v,Nx)
		SetFluxDensity(Cell)
		
		
	
	
	#=========================
	#Plotting
	#PlotNormalVectors(Cell)
	PlotCell(Cell)
	PlotHeights(Cell)
	plt.xlabel("x")
	plt.ylabel("y")
	plt.title("pseudo-1d grid nt = {}".format(runtime-1))
	plt.show()
	
	#for index in Cell:
	#	print(Cell[index])
	
