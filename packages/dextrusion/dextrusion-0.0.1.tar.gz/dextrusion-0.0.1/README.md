# ![DeXtrusion](./images/DeX.png?raw=true "DeXtrusion") DeXtrusion

DeXtrusion is  a machine learning based python pipeline to detect cell extrusions in epithelial tissues movies. It can also detect cell divisions and SOPs, and can easily be trained to detect other dynamic events. 

This repository contains the code source of the python DeXtrusion library, the trained neural networks (ready to use) with Jupyter notebooks to run, train or retrain DeXtrusion networks, and Fiji macros for visualization/analysis of the results.

* [Presentation](#presentation)
* [Installation](#installation)
* [Usage](#usage)
* [Data](#data)
* [DeXtrusion networks](#dexnets-dextrusion-neural-networks)
* [Fiji macros](#fiji-macros)
* [References](#references)

## Presentation
DeXtrusion takes as input a movie of an epithelium and outputs the **spatio-temporal location of cell extrusion events** or othe event as cell divisions. 
The movie is discretized into small overlapping rolling windows which are individually [classified for event detection](#event-classification) by a trained [neural network](#deXNets-deXtrusion-neural-networks). Results are then put together in event [probability map](#event-probability-map) for the whole movie or as [spatio-temporal points](#event-spot-localization) indicating each event. 

<p align="center">
![Example extrusion detection](./images/SequenceExtrusion.png?raw=true "Extrusion detection example") 
Example of the detection of an extrusion event (probability map, red).
</p>


### Event classification
The movie is discretized into small windows that span all the movie in a rolling windows fashion with overlap between the different windows. 
Each window is classified by a trained neural network as containing or not a cellular event as cell extrusion. The different classes available in the main DeXtrusion network are:
- No event
- Cell extrusion/cell death
- Cell division
- SOPs

It is easy to add or remove a cellular event to this list, but necessitates to train new neural networks for this. Jupyter notebook is available in this repository to do it.

### Event probability map
Each window is associated an event probability which allow to generate an events probability map on the whole movie. This probability maps can be refined to precise spatio-temporal spots for each event.
The results can be visualized by overlaying the initial movie and all the probability maps saved by DeXtrusion in Fiji with the saved by DeXtrusion with the [`deXtrusion_overlayProbabilityMaps.ijm`](https://gitlab.pasteur.fr/gletort/dextrusion/-/blob/main/ijmacros/deXtrusion_overlayProbabilityMaps.ijm) macro.

<p align="center">
![Example probability maps](./images/SequenceProbamaps.png?raw=true "Probability map example") 
</p>

Example of probability maps (green: division, red: extrusion, blue: SOP

### Event spot localization
An event is visible in the probability map as a volume of connected pixels of high probability. To convert the probability map to a list of event, we place the event localization at the center of each of these high probability volumes.
Moreover, to reduce false positive detections, the volumes can be thresholded to keep only big enough volume of high enough probability values. 
The list of spots obtained in this way are saved in ROIS `.zip` file that can be open in Fiji through the `ROIManager` tool. The macro [`deXtrusion_showROIs.ijm`](#https://gitlab.pasteur.fr/gletort/dextrusion/-/blob/main/ijmacros/deXtrusion_showROIs.ijm) allows to directly visualize with Fiji the results saved by DeXtrusion. 


## Installation
DeXtrusion is distributed as a python module, compatible with `python3.8`. 
You can install it in a virtual environment to be sure to have the required versions.
**DeXtrusion** can be installed either manually through the setup file or with pip:

* To install manually **DeXtrusion**, clone this github repository, and inside this repository type: `python setup.py install`. 
If you want to install it in a virtual environment, you should have activated it before.
It will install all the necessary dependencies.

* DeXtrusion can be directly installed via pip. In your python virtual environment, enter: `pip install dextrusion` to install it.
You should also download the trained neural network [DeXNet](#dexnets-dextrusion-neural-networks) that you want to use from this repository.

### Detailled installation on Linux Ubuntu
Here's a step by step command lines to run in a Terminal to install DeXtrusion on Linux from scratch. It is creating a new virtual environment on which DeXtrusion will be installed (not necessary but recommended). Tested with `python 3.8`.
 
```sh
python3 -m venv dextrusenv               ## create a virtual environment with python 3 called dextrusenv (you can choose the name)
source dextrusenv/bin/activate           ## activate the virtual environment: now python commands will be runned in that environment
git clone https://gitlab.pasteur.fr/gletort/dextrusion.git    ## download all the source code of DeXtrusion
cd dextrusion                            ## go inside DeXtrusion directory
python setup.py install                  ## install DeXtrusion, download all the necessary dependencies, can take time
cd DeXNets/notum_ExtSOPDiv               ## go inside the desired neural networks directory (here the network trained with 4 events)
unzip notumExtSOPDiv0.zip                ## uncompress it. It is now ready to be used
unzip notumExtSOPDiv1.zip
cd ../..                                 ## go back to main DeXtrusion directory
python -m dextrusion 	                  ## run DeXtrusion. Next time to run it again with the same networks, you only have to do this line
```

## Usage

DeXtrusion can be used directly within python. 
To run an already trained network and detect cell events, run `python3 -m dextrusion` in your virtual environment. It will open a graphical interface to perform the detection.

We also propose [Jupyter notebooks](https://gitlab.pasteur.fr/gletort/dextrusion/-/tree/main/jupyter_notebooks) in this repository, to use dextrusion options. 
You can find a notebook to perform the detection, train a new neural network, retrain a network or evaluate the performance of the network compared to a manual detection.


## Data
Data used for the training of our neural networks (raw movies with manual anotation of events) are freely available here:  XXXXXX. 


## DeXNets: deXtrusion neural networks
DeXtrusion was trained on E-cadherin tagged drosophilia notum but can be easily adapted to other markers/biological conditions. Retraining of DeXtrusion network may be necessary when images are quite different.

In the `deXNets` folder of this repository, we proposed several trained networks:
- `notum_Ext`: trained on drosophilia notum movies with only extrusion events
- `notum_ExtSOP`: trained on drosophilia notum movies with extrusion and SOP events
- `notum_ExtSOPDiv`: trained on drosophilia notum movies with extrusion, division and SOP events

Download them and unzip to be ready to use in DeXtrusion.

### Train/retrain a new DeXNet
If you want to train/retrain a neural network, to add a new event to detect or to improve its performance on new datasets, Jupyter notebooks are proposed in this repository: [Jupyter notebooks](https://gitlab.pasteur.fr/gletort/dextrusion/-/tree/main/jupyter_notebooks). You can just follow step by step the notebook.

If you want to change the architecture of DeXNet, you will have to change it in the `src/dextrusion/Network.py` file. The architecture is defined in the `action_model` function.


## Fiji macros
Fiji macros to prepare data for DeXtrusion neural network training or to handle DeXtrusion results are available in the [`Fiji macros`](#https://gitlab.pasteur.fr/gletort/dextrusion/-/blob/main/ijmacros/README.md) folder of this repository.


## References


## License
DeXtrusion is distributed open-source under the BSD-3 license, see the license file in this repository.

When you use DeXtrusion source code, neural networks or data for your projects, please cite our paper. 

