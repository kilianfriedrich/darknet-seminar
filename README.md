Identification and Analysis of Leaked Data on the Dark Web
==========================================================

Starten
-------

Installiere die benötigten Dependencies mit: `pip install -r requirements.txt`

Um die Daten mit Hilfe des Jupyter-Notebooks zu analysieren, kann es dann über `jupyter lab` gestartet werden
und sollte sich dann im Browser öffnen.
Über den grünen doppelten Startbutton in der oberen Leiste können alle Zellen ausgeführt werden,
dann sollten schon alle Graphen und Ausgaben, die wir bereits gebaut hatten, angezeigt werden.
Alternativ können noch eigene Zellen hinzugefügt werden.

Wir haben die Daten einmalig selber gescraped und getestet, welche Leak Sites online sind.
Die Daten sind allerdings vermutlich schnell veraltet, wenn man neuere Daten will,
kann man mit `python aggregator.py` neu scrapen und arbeitet dann mit den neuen Daten.
Das sollte man über Nacht machen, da es sehr lange dauert,
da pro nicht erreichbarer Leak Site ein 60-Sekunden-Timeout abgewartet wird.

Die Post-Daten werden bei jedem Durchlauf über die APIs abgerufen und müssen NICHT durch den Befehl aktualisiert werden.
Das geht mit etwa 10 Sekunden sehr zügig.

Betreuer
--------

- Marius Brockhoff
- Sebastian Schinzel


Beschreibung
------------

The increasing threat of cyber attacks and the associated trade in leaked data on the dark web represents a serious challenge for society.
In recent years, there has been an increase in attacks in the form of ransomware attacks on healthcare facilities and thus also patient data available on the dark web.
In order to investigate the attackers' approach and techniques, it is necessary to identify and analyze the leaked data.
The aim of this project is to present a tool that searches the dark web for various parameters and provides data for further analysis.
There are several tools available on GitHub that could be used for this purpose (see sources).
Your task is to identify suitable tools and to explain and compare their functionality.

Quellen
-------

- https://github.com/DedSecInside/TorBot
- https://github.com/apurvsinghgautam/dark-web-osint-tools