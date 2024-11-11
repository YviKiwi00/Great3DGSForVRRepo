# Great 3DGS for VR

## Abstract

## Overview

## Installation
Die Installation hier wird nur für Ubuntu-basierte Systeme beschrieben. Betriebssysteme wie Windows sind nicht getestet und die Funktionalität kann nicht garantiert werden.

Erst muss das Repo und seine Submodules geklont werden:
```shell
git clone https://github.com/YviKiwi00/Great3DGSForVRRepo.git --recursive
```

### 1. Abhängigkeiten
Folgende Abhängigkeiten werden vor der Installation dieses Repos benötigt:

- Conda
- Colmap
- ImageMagick 7 (optional)
- C++ Compiler für PyTorch
- CUDA Toolkit 11.8

Dabei ist wichtig, das der C++ Compiler und das CUDA SDK kompatibel sind. Im Folgenden wird die Installation beider Abhängigkeiten für dieses Repo beschrieben.

<details>
<summary><span style="font-weight: bold;">Hier klicken für Installationsanleitung.</span></summary>

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
Die Installation aller Abhängigkeiten und Module für dieses Repo wurde in einem einzigen Installationsskript gebündelt. Wie oben beschrieben wird für die Installation CUDA 11.8 und GCC und G++ 11 benötigt.

Folgende Argumente werden für das Installationsskript akzeptiert:

| Parameter                    |                                                                                                                                                                               Beschreibung |
|:-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| `--no_nvdiffrast`            |                                     Keine Installation von [Nvdiffrast](https://nvlabs.github.io/nvdiffrast/), einem optionalem Repo für Occlusion Culling und schnellere Mesh-Extraction. |
| `--no_deva`                  | Keine Installation von [DEVA](https://github.com/hkchengrex/Tracking-Anything-with-DEVA), einem optionalem Repo für die Vorbereitung von Masken und Segmentierung auf eigenen Datensätzen. |
| `--no_lama`                  |                                                                      Keine Installation von [LaMa](https://github.com/advimman/lama), einem optionalem Repo für das Inpainting von Szenen. |

Im Root-Verzeichnis können folgende Befehle für die Installation des Environments und das Aktivieren des Environments genutzt werden.
```shell
python install.py
conda activate Great3DGSForVR
```

## Training

### 1. Structure from Motion
Als Basis jedes Trainings wird die Punktwolke und die Kameraparameter einer jeden Szene extrahiert. Es wird COLMAP als Structure-from-Motion (SfM) Pipeline benutzt.
Am besten wird ein Ordner `data` angelegt, in dem alle Datensätze enthalten sind, auf dem das weitere Training durchgeführt wird.
```shell
data
|---<dataset>
    |---input
        |---<image 0>
        |---<image 1>
        |---...
```

Auf diesen in `data` enthaltenen Datensätzen kann folgendes Skript für die Structure-from-Motion Konvertierung ausgeführt werden:
```shell
python convert.py -s <dataset> [--resize]
```

Das optionale Argument `--resize` kann, vorausgesetzt ImageMagick 7 ist als Abhängigkeit installiert, genutzt werden, um vier verschiedene Skalierungsstufen der Bilder zu generieren. Dies kann nützlich sein, falls der Grafikkartenspeicher nicht sehr groß ist und z.B. das Generieren von Segmentierungsmasken auf kleiner skalierten Bildern erfolgen muss.
Es werden folgende Ordner erstellt:

| Ordner     |                                                                                                                                     Beschreibung |
|:-----------|-------------------------------------------------------------------------------------------------------------------------------------------------:|
| `images`   |                                               Wird standardmäßig generiert und enthält die Input-Bilder aus dem Ordner `input` in Originalgröße. |
| `images_2` |  Wird mit gesetztem `--resize` Argument generiert und enthält die Input-Bilder aus dem Ordner `input` auf die Hälfte der Originalgröße skaliert. |
| `images_4` | Wird mit gesetztem `--resize` Argument generiert und enthält die Input-Bilder aus dem Ordner `input` auf ein Viertel der Originalgröße skaliert. |
| `images_8` |  Wird mit gesetztem `--resize` Argument generiert und enthält die Input-Bilder aus dem Ordner `input` auf ein Achtel der Originalgröße skaliert. |