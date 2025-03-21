# 🎮 Great 3DGS for VR

Eine Anwendung zur einfachen Verarbeitung von Bilddatensätzen und Aufbereitung dieser via 3D-Gaussian-Splatting zur einfachen Weiterverwendung in interaktiven 3D-Anwendungen.

---

## 📌 Inhaltsverzeichnis
- [📝 Abstract](#-abstract)
- [📦 Installation](#-installation)
  - [1. Abhängigkeiten](#1-abhängigkeiten)
    - [1.1 C++ Compiler (GCC/G++)](#11-c-compiler-gccg)
    - [1.2 CUDA Toolkit](#12-cuda-toolkit)
  - [2. Conda-Environment & Module](#2-conda-environment--module)
  - [3. Troubleshooting](#3-troubleshooting)
- [🚀 Anwendung starten](#-anwendung-starten)
  - [Server lokal](#server---lokal)
  - [Server via SSH](#server---über-ssh)
  - [Client starten](#client)
- [🧪 Nutzung](#-nutzung)
  - [Upload](#upload)
  - [Jobs](#jobs)
  - [Job-Details](#job-detail)
  - [How-To](#how-to)

---

## 📝 Abstract

*(TODO - Abstract hinzufügen)*

---

## 📦 Installation

> Die Installation wurde nur auf **Ubuntu-basierten Systemen** getestet. Eine Nutzung unter Windows wird nicht empfohlen.

### 📥 Repository klonen
```bash
git clone --recurse-submodules https://github.com/YviKiwi00/Great3DGSForVRRepo.git
```

---

### 1. Abhängigkeiten  
<details>
<summary><strong>▶️ Hier klicken zum Aufklappen</strong></summary>

#### Vorab benötigt:
- Conda
- Colmap
- ImageMagick 7 *(optional)*
- C++ Compiler für PyTorch
- CUDA Toolkit 11.8

Dabei müssen C++ Compiler und CUDA **kompatibel** zueinander sein. Das Projekt wurde mit CUDA Toolkit v11.8 und GCC / G++ v11 getestet. 

---

#### 1.1 C++ Compiler (GCC/G++)
Empfohlen: GCC/G++ 11
```bash
sudo apt install build-essential
sudo apt -y install gcc-[Version] g++-[Version]
```

#### Version verwalten (eine höhere Priorität wird automatisch genutzt)
```bash
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-[Version] [Priorität]
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-[Version] [Priorität]
sudo update-alternatives --config gcc
sudo update-alternatives --config g++
```

#### Version prüfen
```bash
gcc --version
g++ --version
```

---

#### 1.2 CUDA Toolkit

#### Version prüfen
```bash
nvidia-smi                    # Unterstützte Version
nvcc --version                # Aktive Version
ls /usr/local/ | grep cuda    # Alle auf dem Rechner installierten CUDA-Versionen
```

#### Installation
1. CUDA 11.8 als `.run`-Datei downloaden: [CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive)
2. Ausführbar machen:
   ```bash
   chmod +x <name of runfile .run>
   ```
3. Nur Toolkit installieren (ohne Treiberinstallation):
   ```bash
   sudo ./<name of runfile .run> --silent --toolkit
   ```

4. PATH konfigurieren:
   ```bash
   gedit ~/.bashrc
   
   # Folgendes einfügen:
   export PATH="/usr/local/cuda-11.8/bin:$PATH"
   export LD_LIBRARY_PATH="/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH"
   
   # Datei speichern und im Terminal neu laden
   source ~/.bashrc 
   ```

</details>

---

### 2. Conda-Environment & Module  
<details>
<summary><strong>▶️ Hier klicken zum Aufklappen</strong></summary>

Alles wird über ein Skript erledigt – vorausgesetzt, CUDA v11.8 und GCC/G++ v11 sind korrekt installiert.

```bash
python install.py
conda activate Great3DGSForVR
```

Optionale Parameter:

| Parameter             |                                                                                                            Beschreibung |
|:----------------------|------------------------------------------------------------------------------------------------------------------------:|
| `--no_rasterizer`     | Überspringt Installation des [Gaussian Splatting Rasterizers](https://github.com/YviKiwi00/diff-gaussian-rasterization) |
| `--no_simple_knn`     |                                                                      Überspringt Installation von simple-knn Submodule. |
| `--no_sam`            |      Überspringt Installation von [SAM](https://github.com/facebookresearch/segment-anything) (Segment Anything Model). |
| `--no_grounding_dino` |                           Überspringt Installation von [GroundingDINO](https://github.com/IDEA-Research/GroundingDINO). |
| `--no_nvdiffrast`     |                                        Überspringt Installation von [Nvdiffrast](https://nvlabs.github.io/nvdiffrast/). |

Diese Parameter sind ausschließlich sinnvoll, wenn nur einzelne Module neuinstalliert werden sollen.

</details>

---

### 3. Troubleshooting  
<details>
<summary><strong>▶️ Hier klicken zum Aufklappen</strong></summary>

#### Fehlende Pakete
```bash
conda env update --file environment.yml --prune
```
Wenn nötig:
```bash
pip install <fehlendes-package>
```

#### Fehlende Submodules
```bash
git pull --recurse-submodules
```

</details>

---

## 🚀 Anwendung starten

### Server - Lokal
```bash
cd server
PYTHONPATH=. python server.py
```

### Server - Über SSH
SSH-Verbindung mit Port-Tunnel aufbauen:
```bash
ssh -L 5000:localhost:5000 <user>@<ssh-server>
```

Optional mit `tmux` im Hintergrund:
```bash
tmux new -s great3dgsforvr_server
conda activate Great3DGSForVR
PYTHONPATH=. python server.py
```
- **Ausklinken:** `CTRL+B`, dann `D`
- **Wieder verbinden:**  
  ```bash
  tmux attach -t great3dgsforvr_server
  ```

### Client
```bash
cd client
PYTHONPATH=. python client.py
```

👉 Das Frontend öffnen: [http://localhost:8000/static/html/index.html](http://localhost:8000/static/html/index.html)

---

## 🧪 Nutzung

Das Frontend besteht aus vier Seiten: **Upload**, **Jobs**, **Job-Detail** und **How-To**.

### Upload
- Bildauswahl, Vergabe des Projektnamens und Upload
- Nur einmal auf „Upload“ klicken (unter SSH kann der Upload etwas dauern!)
- Erfolgreicher Upload wird mit eindeutiger Job-ID aus dem Backend bestätigt

⚠️ Aktuell keine Dateityp-Überprüfung – bitte nur gängige Bildformate hochladen!

---

### Jobs
- Übersicht aller gestarteten Jobs: ID, Projektname, Status
- Klick auf einen Job → zur Detailansicht

⚠️ Keine Sortierung nach Datum – neueste Jobs meist ganz unten.

---

### Job-Detail
- Status und Logs des Jobs einsehen
- Prozesse neu starten bei Fehlern
- **Interaktive Punktsegmentierung:**
  - „Load Segmentation Image“ drücken
  - Punkt setzen → 3 Vorschau-Masken
  - Zufrieden? → „Confirm Segmentation“ starten

Ab hier startet automatisch das weitere Training inkl. Frosting.  
Ergebnis kann anschließend heruntergeladen werden.  
Für die **interaktive Punktsegmentierung** bitte Geduld, Feedback kann über SSH etwas dauern!

---

### How-To

> ❗️ Noch nicht ausgefüllt – TODO!