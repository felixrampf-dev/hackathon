# Aufgabe 3: Subway Surfer

![Subway Surfer.png](img/Subway%20Surfer.png)

### Grundidee (definitiv nicht KI generiert):

Bei diesem Endless-Runner rast du auf drei fest vorgegebenen Bahnen (Lanes) durch eine gefährliche Umgebung. Hindernisse blockieren dir den Weg und zwingen dich zu blitzschnellen Reaktionen: Per Tastendruck wechselst du zwischen der linken, mittleren und rechten Spur, um Kollisionen zu vermeiden. Während das Spiel läuft, erhöht sich das Tempo stetig, was deine Reaktionszeit auf die Probe stellt. Dieses Projekt lehrt dich den Umgang mit diskreten Zuständen (Spur-Logik), die prozedurale Generierung von Hindernissen und das Design eines flüssigen Spielgefühls durch Animationen.

### Voraussetzung:

In dem zugehörigen Repository findet ihr ein einfaches Setup, welches die Game-Loop implementiert und die Steuerung eines Dots auf einem schwarzen Hintergrund ermöglicht.
Es liegt an euch, dieses Setup zu erweitern und die Mechaniken von Subway Surfer zu implementieren.

### Aufgaben:

1. *Implementiere die Bewegung des Runners.*

In Subway Surfer bewegt der Runner sich auf drei vorgegebenen Wegen. Hierbei erfolgt die Bewegung nicht instantan, sondern er oder sie slidet von einer Spur in die nächste. Implementiert diese Bewegung des Runners. (Tipp: Um es mit der Ansicht möglichst einfach zu machen, ergibt es hier Sinn, dass der Runner auf der Stelle rennt und sich die Hindernisse auf ihn oder sie zu bewegen)

2. *Generiert dynamisch Hindernisse.*

Auf maximal zwei der drei Wege sollen regelmäßig Hindernisse entstehen, denen ausgewichen werden muss. Hierbei solltet ihr im Idealfall Abstände einbauen, sodass ein Wechseln der Spuren immer möglich bleibt. Die Hindernisse sollen sich mit wachsender Dauer des Spiels immer schneller auf den Runner zu bewegen.

3. *Gibt dem Runner einen Grund für das Risiko.*

Legt auf dem Spielfeld vor Hindernissen Münzen ab, die eingesammelt werden können. Hierbei sollte Risiko entsprechend entlohnt werden.

4. *Lasst eurer Kreativität freien Lauf.*

Das wäre ja zu einfach, wenn alles so simpel wäre. Fügt Sprünge ein, bietet Power-Ups an oder baut Easter Eggs ein. Wir sind gespannt, was euch so einfällt.


