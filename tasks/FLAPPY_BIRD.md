# Aufgabe 1: Flappy Bird

![Flappy Bird.png](img/Flappy%20Bird.png)

### Grundidee (definitiv nicht KI generiert):

In diesem Klassiker steuerst du einen Vogel, der unaufhaltsam dem Boden entgegenfällt. Deine einzige Waffe ist ein gezielter Flügelschlag (Tastendruck), der den Vogel kurzzeitig nach oben schnellen lässt. Die Herausforderung liegt im präzisen Timing: Du musst durch schmale Lücken zwischen endlos herannahenden Röhren navigieren. Berührst du eine Röhre oder den Boden, ist das Spiel vorbei. In dieser Challenge lernst du, wie man physikalische Kräfte wie Gravitation und Impuls in Code übersetzt und wie eine zuverlässige Kollisionsabfrage zwischen beweglichen Objekten funktioniert.

### Voraussetzung:

In dem zugehörigen Repository findet ihr ein einfaches Setup, welches die Game-Loop implementiert und die Steuerung eines Dots auf einem schwarzen Hintergrund ermöglicht. 
Es liegt an euch, dieses Setup zu erweitern und die Mechaniken von Flappy Bird zu implementieren.

### Aufgaben:

1. *Implementiere die Gravitation.*

Der Vogel muss fallen und auf Tastendruck (Leertaste) seine vertikale Geschwindigkeit ändern.
Ganz im Sinne der Physik bietet es sich hierbei an, eine konstante Beschleunigung nach unten anzunehmen. Ein Flügelschlag kann anschließend eine konstante Geschwindigkeitsänderung erzeugen oder alternativ die Geschwindigkeit auf einen Wert setzen. Probiert herum und habt Spaß dabei. :)


2. *Achtung Kollision!*

Generiert in regelmäßigen Abständen Röhren-Paare, welche in unterschiedlicher Höhe spawnen und sich über den Hintergrund bewegen.
Um Frustration zu vermeiden, könnt ihr auch hier mit der Geschwindigkeit, der Größe der Lücken und den maximal zu überwindenden Abständen spielen.


3. *Erweitert das Spiel.*

Lasst eurer Kreativität freien Lauf. Baut Power-Ups ein, beschleunigt das Spiel mit der Zeit oder habt auf andere Weise Spaß. Wir sind sicher euch fällt etwas ein.

4. *Wie wäre es mit Autoplay?*

Einfach zu spielen ist ja langweilig. Wie wäre es, wenn ihr voraus berechnet wann der ideale Zeitpunkt zum springen ist und den Computer einen neuen Highscore erzielen lasst. Lasst euch gerne von KI beraten um die beste Umsetzung zu finden.
