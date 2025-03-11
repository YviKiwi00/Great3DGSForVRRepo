# Great 3DGS for VR

## Abstract

## Overview

## Installation
Die Installation hier wird nur für Ubuntu-basierte Systeme beschrieben. Betriebssysteme wie Windows sind nicht getestet und die Funktionalität kann nicht garantiert werden.

Erst muss das Repo und seine Submodules geklont werden:
```shell
git clone --recurse-submodules https://github.com/YviKiwi00/Great3DGSForVRRepo.git
```

### 1. Abhängigkeiten
<details>
<summary><span style="font-weight: bold;">Hier klicken zum Aufklappen.</span></summary>

Folgende Abhängigkeiten werden vor der Installation dieses Repos benötigt:

- Conda
- Colmap
- ImageMagick 7 (optional)
- C++ Compiler für PyTorch
- CUDA Toolkit 11.8

Dabei ist wichtig, das der C++ Compiler und das CUDA SDK kompatibel sind. Im Folgenden wird die Installation beider Abhängigkeiten für dieses Repo beschrieben.

#### 1.1 C++ Compiler
Die Installation eines C++ Compilers kann einzeln oder neben anderen C++ Versionen durchgeführt werden. Laut der [CUDA-Dokumentation](https://docs.nvidia.com/cuda/archive/11.8.0/cuda-installation-guide-linux/index.html) von Nvidia ist GCC und G++ Version 11 kompatibel mit CUDA Toolkit 11.8. Sowohl g++ als auch gcc müssen beide die gleiche Version haben, um Fehler zu vermeiden.

- Installation der passenden gcc- und g++-Version
    ```shell
    sudo apt install build-essential
    sudo apt -y install gcc-11 g++-11
    ```
- Alternative Versionen zu Manager hinzufügen (höhere Priorität wird Standardmäßig ausgewählt)
    ```shell
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-[Version] [Priorität]
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-[Version] [Priorität]
    ```
- Checken, welche Versionen verfügbar sind + Auswahl der gerade benötigten Version
    ```shell
    sudo update-alternatives --config gcc
    sudo update-alternatives --config g++
    ```
- Checken der gerade aktiven Version
    ```shell
    gcc --version
    g++ --version
    ```
Für die Installation und Benutzung dieses Repos muss die kompatible Version von GCC und G++ auf dem System aktiv sein!

#### 1.2 CUDA Toolkit
Auch die Installation der passenden CUDA-Toolkit Version kann als Einzelversion auf dem System oder auch neben einer bestehenden CUDA-Version installiert werden.

- Prüfen der CUDA-Version
    ```shell
    nvidia-smi                                    # Höchste unterstützte CUDA-Version
    nvcc --version                                # Momentan genutzte CUDA-Version
    ls /usr/local/ | grep cuda                    # Alle auf dem Rechner installierten CUDA-Versionen
    ```
- Download der gewünschten CUDA-Version: [CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive)
  - Auf der Download-Seite der gewünschten Version sollte runfile (local) als Installer Type ausgewählt werden 
  - Aus den Instruktionen in diesem Schritt nur den Download durchführen, nicht die Installtion!
- Gedownloadete Runfile muss executable gemacht werden
    ```shell
    chmod +x <name of runfile .run>
    ```
- Installation des Toolkit (und auch nur des Toolkit, ohne Treiber-Installation!)
    ```shell
    sudo ./<name of runfile .run> --silent --toolkit
    ```
- CUDA-Version sollte jetzt mit obigen Befehl aufgelistet werden
  - Falls nvcc --version nicht funktionieren sollte, könnte es sein, dass CUDA nicht dem PATH hinzugefügt wurde
    ```shell 
    gedit .bashrc
    
    # Diese zwei Zeilen hinzufügen, CUDA-Version ggf. ändern
    export PATH="/usr/local/cuda-[version]/bin:$PATH"
    export LD_LIBRARY_PATH="/usr/local/cuda-[version]/lib64:$LD_LIBRARY_PATH"
    
    source .bashrc      # Oder neues Terminal
    ```
    
</details>

### 2. Installation des Conda-Environments und aller anderen Module
<details>
<summary><span style="font-weight: bold;">Hier klicken zum Aufklappen.</span></summary>

Die Installation aller Abhängigkeiten und Module für dieses Repo wurde in einem einzigen Installationsskript gebündelt. Wie oben beschrieben wird für die Installation CUDA 11.8 und GCC und G++ 11 benötigt.

Folgende Argumente werden für das Installationsskript akzeptiert:

| Parameter             |                                                                                                                                                                       Beschreibung |
|:----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| `--no_rasterizer`     | Installation des [Gaussian Splatting Rasterizers](https://github.com/YviKiwi00/diff-gaussian-rasterization) wird übersprungen. Nur empfohlen, wenn schon gepulled und installiert. |
| `--no_simple_knn`     |                                                                                   Installation des simple-knn Submodules wird übersprungen. Nur empfohlen, wenn schon installiert. |
| `--no_sam`            |                                 Installation des [SAM-Algorithmus](https://github.com/facebookresearch/segment-anything) wird übersprungen. Nur empfohlen, wenn schon installiert. |
| `--no_grounding_dino` |                             Installation des [GroundingDINO-Algorithmus](https://github.com/IDEA-Research/GroundingDINO) wird übersprungen. Nur empfohlen, wenn schon installiert. |
| `--no_nvdiffrast`     |                             Keine Installation von [Nvdiffrast](https://nvlabs.github.io/nvdiffrast/), einem optionalem Repo für Occlusion Culling und schnellere Mesh-Extraction. |

Im Root-Verzeichnis können folgende Befehle für die Installation des Environments und das Aktivieren des Environments genutzt werden.
```shell
python install.py
conda activate Great3DGSForVR
```
<details>
<summary><span style="font-weight: bold;">Troubleshooting</span></summary>

Sollte während eines Jobs ein Fehler auftreten, bei dem sich über fehlende Pakete beschwert wird, kann folgender Befehl ausgeführt werden:
```shell
conda env update --file environment.yml --prune
```

Dies installiert nochmal alle Abhängigkeiten der Environment-Variable. Falls auch das nicht hilft, muss ggf. manuell nach dem benötigten Paket geschaut werden und mit pip install <package> installiert werden.
**Beachte:** Dafür muss sich im richtigen Conda-Environment aufgehalten werden!
</details>
</details>

## Starten der Anwendung
Das Repo ist aufgebaut in einen Client und einen Server. Der Client bietet ein einfaches Frontend zum Hochladen von Bilddatensätzen und schickt Anfragen an den Server zum Durchführen der Berechnungen. Der Client kann nach Hochladen auch gestoppt werden und je nach Bedarf wieder gestartet. Dieser holt sich Informationen zum Stand der Berechnungen beim Server ab.
Der Server sollte auf einem Rechner mit sehr guter Grafikkarte laufen. Beide Services können aber auch lokal auf dem selbem Rechner gestartet und ausgeführt werden.

**Starten des Servers:**
```shell 
  cd server
  PYTHONPATH=. python server.py
```

**Umleiten des Ports über SSH-Verbindung (falls Server auf anderem Rechner läuft):**
```shell 
  ssh -L 5000:localhost:5000 <username>@<ssh-adress>
```

**Starten des Clients:**
```shell 
  cd client
  PYTHONPATH=. python client.py
```

Das Frontend kann dann über http://localhost:8000/static/html/index.html aufgerufen werden.

## Nutzung
Der Client besteht aus einem einfachen HTML-Frontend mit vier Seiten: Upload, Jobs, Job-Details und How-To.

**TODO: README bebildern**

### Upload
Die Upload-Seite hat zum Ziel, den Bilddatensatz, der verarbeitet werden soll, hochzuladen. Dafür gibt es eine einfache Eingabemaske, in der man im File-System seine Bilder auswählen kann.

**Achtung:** Es gibt momentan keinen Check, der prüft, ob die ausgewählten Dateien ein Bildformat sind.

**Hinweis:** Bei Nutzung des Servers über SSH kann der Upload durch aus ein bisschen dauern, ohne das direkt Feedback kommt. Bitte nur einmal auf den Upload-Button drücken und auf Antwort des Servers warten!
Sowohl über Erfolg als auch Misserfolg wird im Frontend berichtet!

Ist der Upload erfolgreich verlaufen, wird automatisch auf die Jobs-Seite verlinkt. Man kann allerdings auch über die Navigation manuell die Seiten wechseln.

### Jobs
Die Jobs-Seite gibt einen Überblick über die vom Server verarbeiteten Jobs, deren Projektname, ID und Status. Bei Klick auf einen der Jobs kommt man in dessen Detail-Ansicht und kann (je nach Status) mit diesem interagieren.

**Hinweis:** Die Job-Tabelle wird momentan nicht nach zuletzt gestartetem Job sortiert. In den allermeisten Fällen wird der Job ganz unten in der Liste sein.

### Job-Detail
Die Job-Detail-Seite ist wohl die interessanteste, da man hier die Server-Logs verfolgen kann und einzelne Prozesse bei Fehlschlag neustarten kann. Außerdem befindet sich hier das interaktive Punkt-Prompting für die Objektsegmentierung.

**Hinweis:** Wurde ein Punkt-Prompt gesetzt, so sollte auf Antwort des Servers gewartet werden. Bis auf einen Alert gibt es leider keinen Hinweis auf den Fortschritt, die Segmentation-Preview sollte allerdings recht schnell durchgeführt sein.

Ist der Prozess soweit, dass ein Punkt als Prompt zur Segmentierung gesetzt werden kann, sollte auf den Button "Load Segmentation Image" gedrückt werden. Dieses Image ist das erste aus den vorhanden Kameransichten gerenderte Bild der Gaussian-Splatting-Szene. Mit Klick auf das Bild kann ein Punkt gesetzt werden. Der Server generiert darauf hin drei Previews der generierten Maske. Dieser Prozess kann so oft wiederholt werden wie nötig. Ist der Nutzer mit der Masken-Preview zufrieden, kann über "Confirm Segmentation" mit der tatsächlichen Segmentierung der Gaussians gestartet werden.

Nach der Segmentierung läuft automatisch auch das weitere Training mit Frosting ab. Das Endergebnis kann dann über den erscheinenden Button "Download Result" heruntergeladen werden.

### How-To
How-To ist beinhaltet eine ähnliche Erklärung zum Frontend wie diese README.

**TODO: How-To befüllen**