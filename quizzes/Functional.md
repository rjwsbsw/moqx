# Quiz: Funktionale Programmierung  -- in Python und JavaScript

## Frage 1: Welche Eigenschaft trifft auf funktionale Programmierung zu?
- [x] Vermeidung von Seiteneffekten
- [x] Nutzung reiner Funktionen
- [ ] Objektorientierte Vererbung
- [ ] Verwendung globaler Variablen

## Frage 2: Welche Funktion führt in Python eine Transformation durch?
- [x] map()
- [ ] filter()
- [ ] reduce()
- [ ] zip()

## Frage 3: Was ist das Ergebnis von list(map(lambda x: x*2, [1, 2, 3]))?
- [ ] [1, 2, 3]
- [x] [2, 4, 6]
- [ ] [1, 4, 9]
- [ ] [3, 2, 1]

## Frage 4: Was liefert filter(lambda x: x > 2, [1, 2, 3]) in Python?
- [ ] [1, 2]
- [x] [3]
- [ ] [2, 3]
- [ ] [1, 2, 3]

## Frage 5: Welche Bibliothek stellt reduce in Python bereit?
- [ ] itertools
- [x] functools
- [ ] lambda
- [ ] numpy

## Frage 6: Was beschreibt den Begriff „referenzielle Transparenz“?
- [x] Gleiche Eingabe → gleiche Ausgabe
- [ ] Code kann dynamisch verändert werden
- [ ] Variable ist global sichtbar
- [ ] Der Rückgabewert ist zufällig

## Frage 7: Was bewirkt yield in Python?
- [x] Erzeugt einen Generator
- [ ] Führt sofortige Rückgabe durch
- [ ] Bricht die Schleife ab
- [ ] Deklariert eine Klasse

## Frage 8: Was ist das Ergebnis von next(iter([10, 20, 30]))?
- [x] 10
- [ ] 20
- [ ] [10]
- [ ] TypeError

## Frage 9: Wie lautet die Syntax einer Python-Lambda-Funktion?
- [x] lambda x: x + 1
- [ ] function(x) { return x + 1 }
- [ ] x -> x + 1
- [ ] lambda(x) { x + 1 }

## Frage 10: Was ist ein Generator-Ausdruck?
- [x] (x*x for x in range(5))
- [ ] [x*x for x in range(5)]
- [ ] map(lambda x: x*x)
- [ ] filter(x % 2)

## Frage 11: Was ist der Hauptunterschied zwischen map() in Python und JavaScript?
- [ ] JS ist lazy, Python ist eager
- [x] Python ist lazy, JS ist eager
- [ ] Beide sind lazy
- [ ] Beide brauchen yield

## Frage 12: Was ist eine Arrow Function in JavaScript?
- [x] Kurzschreibweise für anonyme Funktionen
- [ ] Nur in Klassen erlaubt
- [ ] Führt automatische Rückgabe von undefined durch
- [ ] Hat ein eigenes this

## Frage 13: Was bewirkt .filter() in JavaScript?
- [x] Gibt alle Elemente zurück, die den Test bestehen
- [ ] Sortiert das Array
- [ ] Gibt die Indizes zurück
- [ ] Entfernt Duplikate

## Frage 14: Welcher Ausdruck ergibt [1, 4, 9]?
- [ ] [1, 2, 3].filter(x => x * x)
- [x] [1, 2, 3].map(x => x * x)
- [ ] [1, 2, 3].reduce(x => x * x)
- [ ] [1, 2, 3].map(x => x + x)

## Frage 15: Was gibt [1,2,3].reduce((a,b) => a + b, 0) zurück?
- [x] 6
- [ ] [1, 2, 3]
- [ ] [3, 2, 1]
- [ ] undefined

## Frage 16: Was ist ein Closure?
- [x] Eine Funktion, die auf den Scope ihrer Erstellung zugreift
- [ ] Eine Methode innerhalb einer Klasse
- [ ] Eine API-Funktion
- [ ] Ein Singleton

## Frage 17: Welche Aussagen zu this in Arrow Functions sind korrekt?
- [x] this wird aus dem umgebenden Kontext übernommen
- [ ] Arrow Functions haben ihr eigenes this
- [ ] this zeigt immer auf das globale Objekt
- [ ] this ist in Arrow Functions nicht erlaubt

## Frage 18: Welcher Ausdruck sortiert nach Alter? personen.sort((a, b) => a.alter - b.alter)

* [x] korrekt
* [ ] falsche Syntax
* [ ] sortiert nach Name
* [ ] gibt nur undefined zurück

## Frage 19: Welche Eigenschaft trifft auf map/filter/reduce in JS zu?

* [x] Erzeugen neue Arrays oder Werte
* [ ] Verändern das Original-Array
* [ ] Funktionieren nur im Browser
* [ ] Erfordern async/await

## Frage 20: Was ist () => 42?

* [x] Arrow Function ohne Parameter
* [ ] Generator-Funktion
* [ ] sofortiger Funktionsaufruf
* [ ] Callback in setTimeout()

## Frage 21: Wie kann man aus einer JS-Arrow Function mit mehreren Anweisungen einen Wert zurückgeben?

* [x] mit return im {}-Block
* [ ] automatisch ohne return
* [ ] mit yield
* [ ] mit break

## Frage 22: Welche Funktionen in Python sind lazy?

* [x] map()
* [x] filter()
* [x] Generator-Ausdrücke
* [ ] list()-Comprehension

## Frage 24: Was macht list(filter(lambda x: x > 10, range(20)))?

* [x] Liste aller Zahlen > 10 von 0–19
* [ ] Liste aller Zahlen < 10
* [ ] Fehler wegen filter
* [ ] Gibt einen Iterator zurück

## Frage 25: Welche der folgenden Ausdrücke sind in JavaScript gültige Arrow Functions?

* [x] x => x + 1
* [x] (x, y) => x * y
* [ ] function x => x + 1
* [ ] x -> x + 1

