# Aufgabe 2: Curve Fever

![Curve Fever.png](img/Curve%20Fever.png)

### Grundidee (definitiv nicht KI generiert):

Curve Fever ist ein rasanter Multiplayer-Wettkampf, bei dem du eine sich ständig verlängernde Linie steuerst. Du kannst dich nicht stoppen, sondern nur nach links oder rechts lenken. Das Ziel ist es, als letzter Spieler zu überleben, ohne die Spielfeldbegrenzung, deine eigene Spur oder die deiner Gegner zu rammen. Der Clou: In unregelmäßigen Abständen entstehen kleine Lücken in deiner Linie, die anderen Spielern als Fluchtweg dienen können. Technisch liegt der Fokus hier auf der Vektorgeometrie (Winkelberechnung) und dem effizienten Management von Spur-Datenpunkten auf dem Spielfeld.

### Voraussetzung:

In dem zugehörigen Repository findet ihr ein einfaches Setup, welches die Game-Loop implementiert und die Steuerung eines Dots auf einem schwarzen Hintergrund ermöglicht.
Es liegt an euch, dieses Setup zu erweitern und die Mechaniken von Curve Fever zu implementieren.

### Aufgaben:

1. *Implementiere eine konstante Vorwärtsbewegung.* 

Der Spieler steuert nur die Richtung (Winkel) mit den Pfeiltasten.
In Curve Fever bewegt man sich (zunächst einmal) mit konstanter Geschwindigkeit. Die einzige Rettung vor der sicheren Kollision mit der Wand ist es, Kurven zu ziehen. Hierfür müsst ihr mit Winkeln arbeiten. Um euren inneren Mathematiker stolz zu machen, bieten sich hier Sinus und Cosinus an, aber hier ist eurer Kreativität keine Grenze gesetzt.

2. *Generiert eine Linie hinter eurem Spieler.*

Um später auch berechnen zu können, wer gewonnen hat, muss erst einmal klar sein, wo eine Kollision möglich wird. Hierfür zeichnet hinter eurem Spieler eine kontinuierliche Linie. Hierbei ist es am einfachsten auf die aktuelle Position des Spielers vor jeder Bewegung einen Punkt zu setzen bzw. auf die letzte Position des Spielers.

3. *Ermittelt eine Kollision.*

Um später einen Gewinner zu ermitteln, muss berechnet werden, ob eine Kollision vorliegt. Hierfür vergleicht ihr die Position des Spielers mit dem Rand des Spielfelds oder mit den bereits betretenen Punkte auf dem Spielfeld.

4. *Erweitert das Spiel für Multiplayer.*

Fügt einen zweiten Spieler hinzu, der sich mit anderen Tasten steuern lässt. Verwendet hierbei dieselben Mechanismen wie zuvor, aber (um Chaos zu vermeiden) eine andere Farbe. Hier könnt ihr auch gerne einen kleinen Gewinner Bildschirm einführen.

5. *Lasst eurer Kreativität freien Lauf.*

Das wäre ja zu einfach, wenn alles so simpel wäre. Fügt Lücken in der Spur der Spieler ein um ein Entkommen zu ermöglichen, erweitert das Spielfeld zufällig um Power-Ups oder Eventbereiche, die Geschwindigkeit oder Größe der Spieler anpassen.

