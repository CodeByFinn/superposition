import math
import matplotlib.pyplot as plt
import matplotlib.ticker as tk

class Source():
	def __init__(self, x, y, charge):
		self.x = x
		self.y = y
		self.charge = charge
	
	# Gibt den Text der Ladung zurück
	def getText(self):
		if self.charge > 0:
			return "+"+str(self.charge)+"C"
		else:
			return str(source.charge)+"C"		
		
class SamplePoint():
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	# Berechnet die Distanz zwischen sich selbst und einem angegebenen Punkt 
	def getDistance(self, toX, toY):
		return math.sqrt((toX-self.x)**2 + (toY-self.y)**2)
		
	# Berechnet den Winkel zu einem angegebenen Punkt in Polarkoordinaten
	def getAngle(self, toX, toY):
		if (toX-self.x) == 0:
			if (toY-self.y) > 0:
				return math.pi*3/2 
			else:
				return math.pi/2
				
		offset = 0
		if (toX-self.x) > 0:
			offset = math.pi
			
		return math.atan((toY-self.y) / (toX-self.x)) + offset
		
	# Wert von E berechnen
	def calculateE(self, source):
		distance = self.getDistance(source.x, source.y)
		
		# Liegt der Punkt zu nah an der Quelle, wird für E 0 zurückgegeben
		if distance < safeDistance:
			return 0
	
		constants = 1/(4*math.pi*e0)
		e = constants * (source.charge / distance**2)
		return e

# Gibt die kartesischen Koordinaten zu gegebenen Polarkoordinaten an
def getCartesian(r, angle):
	return [r*math.cos(angle), r*math.sin(angle)]





# ------------------------------

e0 = 8.85*(10**-12)

# Mathematische Parameter

# Proportionalistätsfaktor
proportionalityFactor = 10**-11
# Distanz um Radialquellen, unter der kein Punkt gezeichnet wird
safeDistance = 1.5
# Grenzen der Darstellung
limits = [[-10, 10], [-8, 8]]

# Liste der Radialquellen (x, y, Ladung)
sources = [
	Source(-3, -2, 100), 
	Source(3, -0.5, -100), 
	Source(-1, 3, 50)
]

# Liste der Probepunkte (x, y)
samplePoints = [
	SamplePoint(-6, 2),
	SamplePoint(-2, 0),
	SamplePoint(5, 3),
	SamplePoint(-2, -6),
	SamplePoint(1, -4),
	SamplePoint(0, 0)
]

# Erstellt ein Raster an Vektoren

#samplePoints = []
#for x in range(limits[0][0], limits[0][1]+1):
#	for y in range(limits[1][0], limits[1][1]+1):
#		samplePoints.append(SamplePoint(x, y))


# Stylistische Parameter

vectorColor = (0.9, 0.9, 0.9)
resultingVectorColor = (144/255, 43/255, 227/255)
width = 0.002
		
# ------------------------------



# Allgemeine Einstellungen für die Darstellung
fig, ax = plt.subplots()
plt.xlim(limits[0][0], limits[0][1])
plt.ylim(limits[1][0], limits[1][1])
ax.set_xlabel("x-Achse in m")
ax.set_ylabel("y-Achse in m")
ax.set_title("Darstellung des E-Felds an bestimmten Probepunkten")
ax.tick_params(which="minor", length=3)
ax.xaxis.set_minor_locator(tk.MultipleLocator(0.1))
ax.yaxis.set_minor_locator(tk.MultipleLocator(0.1))

# Zeichnet die Radialquellen mit passender Farbe ein
for source in sources:
		if source.charge > 0:
			ax.plot(source.x, source.y, "ro")
			ax.annotate(source.getText(), (source.x+0.1, source.y-0.1), fontsize=10)
		else:
			ax.plot(source.x, source.y, "bo")
			ax.annotate(source.getText(), (source.x+0.15, source.y-0.1), fontsize=10)

# Vektoren der Probepunkte zeichnen
for samplePoint in samplePoints:
	resultingVector = [0, 0]
	draw = True
	
	# Alle Vektoren für einen Punkt berechnen
	vectors=[]
	for source in sources:
		r = samplePoint.calculateE(source) * proportionalityFactor
		if r == 0:
			draw = not(draw)
			break
		
		angle = samplePoint.getAngle(source.x, source.y)
		targetCoordinates = getCartesian(r, angle)
		resultingVector[0] += targetCoordinates[0]
		resultingVector[1] += targetCoordinates[1]
		
		vectors.append([
			samplePoint.x,
			samplePoint.y,
			targetCoordinates[0],
			targetCoordinates[1]
		])
	
	#Liegt der zu zeichnende Punkt zu nah an einer Quelle, wird er nicht gezeichnet
	if not(draw):
		continue
	
	# Einzelne Vektoren und resultierenden Vektor zeichnen
	for vector in vectors:
		ax.quiver(
			vector[0],
			vector[1],
			vector[2],
			vector[3],
			angles="xy", scale_units="xy", scale=1,
			width=width,
			color=vectorColor
		)
	
	ax.quiver(
		samplePoint.x,
		samplePoint.y,
		resultingVector[0],
		resultingVector[1],
		angles="xy", scale=1, scale_units="xy",
		width=width,
		color=resultingVectorColor
	)

# Grafik zeigen
plt.show()
