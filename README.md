# superposition
Visualisierung der Superposition von E-Feldern


## Wie's geht
Den Code der Datei [superposition.py](superposition.py) mit einer Python-Umgebung, in der matplotlib installiert ist, ausführen.

## Was dahinter steckt
Visualisiert wird mithilfe der matplotlib-Bibliothek das E-Feld, das durch die Überlagerung von verschiedenen Einzelfeldern entsteht. <br>
Über die Listen `sources` und `samplePoints` können Anzahl und Koordinaten der Radialquellen und Probepunkte geändert werden.

## Wie der Code funktioniert
Zunächst wird die Grafik initialisiert und es werden Einstellungen zu Titel und Achsenbeschriftung vorgenommen.
``` python
fig, ax = plt.subplots()
plt.xlim(limits[0][0], limits[0][1])
plt.ylim(limits[1][0], limits[1][1])
ax.set_xlabel("x-Achse in m")
ax.set_ylabel("y-Achse in m")
ax.set_title("Darstellung des E-Felds an bestimmten Probepunkten")
ax.tick_params(which="minor", length=3)
ax.xaxis.set_minor_locator(tk.MultipleLocator(0.1))
ax.yaxis.set_minor_locator(tk.MultipleLocator(0.1))
```

---

Dann wird jede Radialquelle der Liste auf ihre Ladung hin untersucht und in entsprechender Farbe gezeichnet.
``` python
for source in sources:
		if source.charge > 0:
			ax.plot(source.x, source.y, "ro")
			ax.annotate(source.getText(), (source.x+0.1, source.y-0.1), fontsize=10)
		else:
			ax.plot(source.x, source.y, "bo")
			ax.annotate(source.getText(), (source.x+0.15, source.y-0.1), fontsize=10)
```

---

Für jeden Probepunkt wird nun der Abstand und Winkel zu jeder Quelle berechnet und gespeichert. In `resultingVector` wird zudem die Summe aller Vektoren zwischengelagert.
``` python
for samplePoint in samplePoints:
	resultingVector = [0, 0]
	draw = True
	
	# Alle Vektoren für einen Punkt berechnen
	vectors=[]
	for source in sources:
		r = samplePoint.calculateE(source) * proportionalityFactor
		
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
```

---

Abschließend werden die berechneten Vektoren noch für jeden Probepunkt gezeichnet.
``` python
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
```
