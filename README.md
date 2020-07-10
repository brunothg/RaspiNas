RaspiNas
========

A Raspberry Pi 4 8GB based NAS

Hierbei handelt es sich um einen Selbstbau NAS mit oben genanntem Raspberry Pi in einem Mini ITX Gehäuse für bis zu vier Festplatten und einer System SSD.  
Zusätzlich wird eine Leiterplatine zur Steuerung des ATX Netzteils, sowie der LEDs (Power und HDD) und der Lüfter gelötet.


## Stückliste

Diese Liste enthält die genutzten Komponenten. Kleinteile wie Kabel, Schrumpfschläuche etc. werden nicht aufgeführt:

* Raspberry Pi 4 8GB (4GB sollte ebenfalls ausreichen)
* Kühlkörper für den Respberry Pi
* SD Karte (zum Booten, 32GB reichen vollkommen)
* Fractal Design Node 304 Gehäuse
* KOLINK SFX-250 (wichtig sind 3A für die 5VSB Standby Leitung, sowie ein aktueller ATX Standard >= 2.4 auf Grund des geringen Verbrauchs)
* Netzteiladapterblende SFX auf ATX (da das Gehäuse für ATX Netzteile ausgelegt ist)
* USB Stick als SWAP (optional)
* USB 3.0 Hub für die Festplatten (4 fach ist hier passend)
* USB 2.0 Hub für Front Panel USB Anschlüsse (optional)
* Adapter für Front Panel USB auf USB A (optional)
* SSD + USB Adapter für das System (hier Crucial 120GB, bei den Adaptern auf kompatibilität achten - JMicron scheint aktuell nur mit quirks zu funktionieren)
* Festplatten + USB Adapter (z.B. 2x4TB WD40EFRX)
* 3D Drucker oder Sperrholz :) für Halterungen (z.B. ITX Halterung für den Raspberry Pi)
* Verlängerungen für HDM und Ethernet zum herausführen der Anschlüsse aus dem Gehäuse (am besten schraubbar)
* Die Komponenten für die Leiterplatine können dem Schaltplan entnommen werden


## License
This project is licensed under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html).
