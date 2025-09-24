# Quiz: Backup Modern –- Tag 1

## Frage 1: Was gehört zur 3-2-1-Backup-Regel?

- [x] Drei Kopien der Daten  
- [x] Zwei unterschiedliche Speichermedien  
- [x] Eine Kopie an einem externen Ort  
- [ ] Drei Backups pro Tag  

---

## Frage 2: Was ist ein typisches Ziel von Backup-Strategien?

- [x] Minimierung von Datenverlust (RPO)  
- [x] Minimierung von Ausfallzeiten (RTO)  
- [ ] Maximierung der Dateigröße  
- [ ] Vermeidung von Benutzerinteraktionen  

---

## Frage 3: Welche Aussagen treffen auf Snapshots zu?

- [x] Sie sind Momentaufnahmen des Dateisystems  
- [x] Sie lassen sich sehr schnell erzeugen  
- [ ] Sie sind immer automatisch verschlüsselt  
- [x] Sie dienen oft als Basis für inkrementelle Backups  

---

## Frage 4: Was kann VSS (Volume Shadow Copy Service) leisten?

- [x] Sichern geöffneter Dateien  
- [x] Erstellung konsistenter Schattenkopien  
- [ ] Verschlüsselung der Backups  
- [x] Integration in viele Backup-Tools  

---

## Frage 5: Welche Werkzeuge können unter Linux/WSL verwendet werden?

- [x] restic  
- [x] rsync  
- [ ] robocopy  
- [ ] wbadmin  

---

## Frage 6: Was sind typische Merkmale von `restic`?

- [x] CLI-basiert  
- [x] Verschlüsselung standardmäßig aktiviert  
- [x] Unterstützt viele Zielsysteme (lokal, SFTP, S3, WebDAV)  
- [ ] Unterstützt GUI-only-Konfiguration  

---

## Frage 7: Welche Tools sind auf einem Windows-11-System nativ vorhanden?

- [x] robocopy  
- [ ] rsync  
- [x] VSS (Volume Shadow Copy Service)  
- [ ] restic  

---

## Frage 8: Welche Varianten von Backups gibt es typischerweise?

- [x] Vollbackup  
- [x] Inkrementelles Backup  
- [x] Differenzielles Backup  
- [ ] Snapshot-only-Backup  

---

## Frage 9: Was spricht gegen WebDAV als Backup-Ziel?

- [x] Kein echtes Dateisystem  
- [x] Hohe Ausfallneigung bei großen Dateien  
- [ ] Automatischer VSS-Support  
- [x] Kein konsistenter Umgang mit Dateiattributen  

---

## Frage 10: Welche Backup-Ziele stehen im Beispiel-Szenario zur Verfügung?

- [x] D:\backups (USB-Platte)  
- [x] O:\backups (ownCloud via WebDAV)  
- [ ] Z:\Sicherung (iSCSI)  
- [ ] C:\Windows\System32  

---

## Frage 11: Wie können PowerShell und WSL auf restic zugreifen?

- [x] Über gesetzte Umgebungsvariablen  
- [x] Mit `restic init` zur Repos-Erzeugung  
- [x] Mit relativen oder absoluten Pfadangaben  
- [ ] Nur über Windows-Taskplanung  

---

## Frage 12: Was unterscheidet robocopy von rsync?

- [x] robocopy ist Windows-nativ, rsync nicht  
- [x] rsync unterstützt SSH, robocopy nicht  
- [ ] robocopy verschlüsselt automatisch  
- [x] rsync zeigt Bandbreiten-optimierte Übertragung  

---

## Frage 13: Was muss stimmen, damit „Vorherige Versionen“ im Windows-Explorer angezeigt werden?

- [x] VSS muss aktiv sein  
- [x] Das Volume muss Schattenkopien unterstützen  
- [ ] rsync muss installiert sein  
- [ ] Der Ordner muss freigegeben sein  

---

## Frage 14: Welche Befehle sichern `/mnt/c/Users/rjwsb/Projekte` korrekt?

- [x] `rsync -avh /mnt/c/... /mnt/d/...`  
- [x] `restic backup /mnt/c/...`  
- [ ] `robocopy /mnt/c/...`  
- [ ] `cp -R /mnt/c/...`  

---

## Frage 15: Welche Aussagen treffen auf `wbadmin` zu?

- [x] Unterstützt VSS  
- [x] Nur vollständig in Windows Pro/Enterprise verfügbar  
- [ ] Verfügbar unter WSL  
- [ ] CLI-Ersatz für robocopy  

---

# Quiz: Backup Modern –- S3-Backups, Container und virtuelle Maschinen

## Frage 1: Welche dieser Dienste sind S3-kompatibel?

- [x] Wasabi
- [x] IONOS S3
- [x] MinIO
- [ ] Azure Blob Storage

## Frage 2: Welches Tool unterstützt nativ Azure Blob Storage?

- [ ] robocopy
- [x] restic
- [ ] rsync
- [ ] duplicity

## Frage 3: Welche Vorteile hat MinIO im lokalen Einsatz?

- [x] Vollständig S3-kompatibel
- [x] Einfach via Docker aufsetzbar
- [x] GUI zur Verwaltung enthalten
- [ ] Nur in der Cloud nutzbar

## Frage 4: Wie authentifiziert sich restic beim S3-Zugriff?

- [x] Mit `AWS_ACCESS_KEY_ID` und `AWS_SECRET_ACCESS_KEY`
- [ ] Mit OAuth2-Token
- [ ] Per SSH-Key
- [ ] Mit der MAC-Adresse

## Frage 5: Was wird bei `restic backup /home/user/data` gesichert?

- [x] Die aktuellen Inhalte des angegebenen Pfads
- [x] Inkrementelle Änderung gegenüber letztem Snapshot
- [ ] Der komplette Systemzustand inklusive Kernel
- [ ] Nur die leeren Ordner

## Frage 6: Welche Aussagen zu `docker export` sind korrekt?

- [x] Exportiert das Dateisystem eines Containers
- [ ] Enthält automatisch alle Volumes
- [ ] Ermöglicht Snapshots während des Betriebs
- [ ] Ersetzt den Dockerfile vollständig

## Frage 7: Wo liegen standardmäßig Docker-Volumes unter Linux?

- [ ] /opt/docker
- [x] /var/lib/docker/volumes
- [ ] /mnt/docker/volumes
- [ ] /usr/local/docker-data

## Frage 8: Warum ist das Sichern von Datenbanken aus dem Containerinneren oft besser?

- [x] Weil ein konsistenter Dump erzeugt werden kann
- [ ] Weil das Volume so schneller gelöscht werden kann
- [x] Weil Dateisystem-Backups inkonsistent sein können
- [ ] Weil man dann kein root braucht

## Frage 9: Welche Tools können Containerdaten außerhalb des Containers sichern?

- [x] rsync
- [x] restic
- [ ] pg_dump
- [ ] mysqldump

## Frage 10: Welche Daten solltest du bei einem `docker-compose`-Projekt sichern?

- [x] docker-compose.yml
- [x] alle benutzten Volumes
- [ ] nur die Container-ID
- [x] .env-Dateien für Konfiguration

## Frage 11: Welches dieser Tools kann verschlüsselt in S3 schreiben?

- [ ] robocopy
- [ ] rsync
- [x] restic
- [x] duplicity

## Frage 12: Welche Speicherorte für Containerdaten gelten NICHT unter Windows?

- [x] /var/lib/docker
- [ ] D:\DockerVolumes
- [ ] %PROGRAMDATA%\docker
- [ ] In der Docker-VM im WSL-Backend

## Frage 13: Was passiert bei einem `restic init`?

- [x] Ein neues, verschlüsseltes Repository wird angelegt
- [ ] Die aktuelle VM wird geklont
- [ ] Das erste Backup beginnt automatisch
- [ ] Das Repository wird formatiert

## Frage 14: Welche der folgenden Speicherarten gelten als objektbasiert?

- [x] S3
- [ ] SMB
- [ ] NFS
- [x] Azure Blob Storage

## Frage 15: Was muss beim Einsatz von WebDAV mit `restic` beachtet werden?

- [x] WebDAV-Support ist nicht mehr direkt in restic enthalten
- [x] Die Nutzung erfolgt über `rclone:`-Backends
- [ ] Das Backend heißt `davfs:` statt `webdav:`
- [ ] WebDAV funktioniert nur unter Linux

---

# Quiz: Backup Modern –- Desaster-Recovery & Restore-Sicherheit

## Frage 1: Was bedeutet RTO?

- [x] Maximale Ausfallzeit, die akzeptabel ist
- [ ] Maximale Größe eines Backups
- [ ] Die Dauer des Backups
- [ ] Zeitraum zwischen zwei Snapshots

## Frage 2: Was beschreibt RPO?

- [x] Wie viele Daten maximal verloren gehen dürfen
- [ ] Wie viele Personen für Restore verantwortlich sind
- [ ] Ob Snapshots aktiviert sind
- [x] Die akzeptierte Zeitspanne seit dem letzten Backup

## Frage 3: Welche Formen des Restore sind gängig?

- [x] Vollständiger Restore
- [x] Selektiver Restore einzelner Dateien
- [x] Test-Restore zur Verifizierung
- [ ] Parallel-Restore ohne Reboot

## Frage 4: Was leistet `restic restore`?

- [x] Stellt ein ganzes Backup oder Teile davon wieder her
- [ ] Startet ein neues inkrementelles Backup
- [ ] Löscht alte Snapshots automatisch
- [x] Funktioniert mit verschiedenen Zielverzeichnissen

## Frage 5: Was macht `restic ls latest`?

- [x] Zeigt alle Dateien im letzten Snapshot
- [ ] Listet alle Backup-Speicherorte
- [ ] Zeigt die Volume-Liste für Container
- [ ] Startet den Mount-Modus

## Frage 6: Warum ist ein Test-Restore wichtig?

- [x] Um zu prüfen, ob die Backups tatsächlich verwendbar sind
- [x] Um Fehler frühzeitig zu entdecken
- [ ] Um Speicherplatz zu sparen
- [ ] Weil das gesetzlich vorgeschrieben ist

## Frage 7: Was leistet der Befehl `restic forget --prune`?

- [x] Entfernt alte Backups gemäß Regelwerk
- [ ] Prüft den Backup-Server
- [x] Räumt das Repository physisch auf
- [ ] Exportiert Snapshots als ZIP-Datei

## Frage 8: Welche Tools lassen sich zur Restore-Kontrolle nutzen?

- [x] diff
- [x] robocopy /L
- [ ] top
- [ ] journalctl

## Frage 9: Was sollte Bestandteil eines DR-Plans sein?

- [x] Verantwortliche Personen und deren Erreichbarkeit
- [x] Wiederherstellungsverzeichnis
- [ ] Die Release-Version von LibreOffice
- [x] Zugang zu Passwörtern oder Secrets

## Frage 10: Wie überprüft `restic check` ein Repository?

- [x] Prüft Struktur und Konsistenz
- [ ] Startet automatisch einen Restore
- [x] Meldet fehlende oder beschädigte Daten
- [ ] Prüft das Betriebssystem auf Fehler

## Frage 11: Welche Backup-Ziele eignen sich für Restore-Simulationen?

- [x] Temporäre Ordner wie `/tmp/testrestore`
- [x] Eigene Unterordner (z. B. `C:\Temp\restic-test`)
- [ ] Das Live-Systemverzeichnis `/etc`
- [ ] `/var/lib/docker` im laufenden Betrieb

## Frage 12: Was ist ein typischer Fehler beim Restore?

- [x] Fehlende Restore-Dokumentation
- [x] Vergessene Passwörter
- [ ] Backup auf zu großem Laufwerk
- [x] Restore im laufenden Betrieb ohne Stopp

## Frage 13: Welche Aussagen zu robocopy /L sind korrekt?

- [x] Listet, was kopiert würde – ohne Kopieren
- [x] Dient zur Vergleichsanalyse von Backup-Zielen
- [ ] Verschlüsselt Dateien automatisch
- [ ] Nutzt ZIP-Archivierung intern

## Frage 14: Was macht den Unterschied zwischen Replikation und Backup?

- [x] Replikation kann auch Fehler und Löschungen spiegeln
- [x] Backup speichert Zustände unabhängig
- [ ] Replikation ist immer sicherer
- [ ] Backup ist nur auf USB möglich

## Frage 15: Wie sieht ein erfolgreicher Restore-Test aus?

- [x] Die gewünschten Daten sind vollständig und intakt
- [x] Die Wiederherstellungszeit bleibt im RTO
- [ ] Das Backupmedium ist wieder leer
- [ ] Die Uptime des Servers wird verlängert

---

# Quiz: Backup Modern –- Anwendungssicherung und Backup

### Frage 1
Warum ist es sinnvoll, Anwendungsdaten separat zu exportieren, bevor sie gesichert werden?

- [x] Um konsistente und vollständige Sicherungen zu ermöglichen
- [ ] Damit man auf ein Backup-Tool verzichten kann
- [x] Weil viele Anwendungen eigene Speicherformate verwenden
- [ ] Damit die Dateien besser komprimiert werden

---

### Frage 2
Welches Tool eignet sich für die Sicherung von IMAP- und Exchange-Postfächern?

- [ ] restic
- [x] MailStore
- [ ] mongodump
- [ ] rsync

---

### Frage 3
Was wird mit dem Befehl `mongodump` erzeugt?

- [x] Ein Dump-Verzeichnis mit BSON-Dateien
- [ ] Ein inkrementelles Backup
- [ ] Ein Snapshot des Dateisystems
- [ ] Ein Backup im CSV-Format

---

### Frage 4
Was ist bei der Sicherung einer PostgreSQL-Datenbank mit `pg_dump` besonders zu beachten?

- [x] Konsistenz (z. B. durch Locking oder Dump aus replizierter DB)
- [ ] Nur im JSON-Format sichern
- [ ] Es ist nicht möglich, PostgreSQL automatisiert zu sichern
- [ ] Der Dump muss aus einem Docker-Volume erfolgen

---

### Frage 5
Wie funktioniert die Sicherung von Nextcloud über `rclone` und `restic`?

- [ ] Das Nextcloud-Webinterface bietet einen Backup-Knopf
- [x] Das Nextcloud-Verzeichnis wird per rclone gemountet und dann mit restic gesichert
- [ ] Nextcloud muss per FTP gespiegelt werden
- [ ] Es ist nicht möglich, Nextcloud ohne Root-Zugriff zu sichern

---

### Frage 6
Welches dieser Verfahren ist **keine empfohlene Methode** zur Sicherung von Chatverläufen?

- [ ] Export aus Teams per Microsoft Graph API
- [ ] Matrix-Export per API und JSON
- [x] Einfaches Kopieren des RAM-Inhalts
- [ ] API-Export aus Slack

---

### Frage 7
Was macht `plonecli zodbpack` in einer Zope/Plone-Umgebung?

- [x] Es „packt“ die Datenbank und legt eine `Data.fs.old` an
- [ ] Es erstellt ein Live-Backup mit Snapshots
- [ ] Es exportiert Benutzer in ein XML-Format
- [ ] Es führt ein Upgrade durch

---

### Frage 8
Was ist ein typisches Ziel einer Anwendungssicherung?

- [x] Eine automatisierbare Export- und Backup-Strategie
- [x] Die Trennung von Export und Dateisicherung
- [ ] Nur Snapshot-Sicherung mit Volume-Mount
- [ ] Tägliches händisches Kopieren durch den Admin

