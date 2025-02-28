# GROUP 2 CODE | MATH 451
Members: Amiri, Ebru, Madison, Cailyn \
https://github.com/AmiriHayes/rockphysicsproject \
[Link to Research Notebook](https://docs.google.com/document/d/1Imp-BBaWYbqmGOgQ5amiGeykf2N4QkyHTzvVvJPT-b8/edit?usp=sharing)

## __Notebook Goals:__

1 - Download existing & create simulated 3D rock topology data  [✓] \
2 - Simplify dataset using PoreSPY SNOW2 (into a graph network) [✓] \
3 - Predict permeability (fluid flow) on datasets using OpenPNM [✓] \
4 - Use machine learning to map representation to permeability \
* https://chatgpt.com/share/67c10964-8b3c-8004-9dbb-f566bc51a04c \
     -  Method 1: Try Node2Vec and Regular Deep Neural Network \
     -  Method 2: Try GCN: Graph Convolutional Networks \
     -  Method 3: Try MPNN: Message-Passing Neural Network \

## __Resources:__
Our Explanation of the PoreSPY SNOW2 Reduction Method:
- https://docs.google.com/presentation/d/1SSHW31IZ6fWqkfT2cLFDcU22-vQ2aC4XyXFaqe7JiCk/edit?usp=sharing
- [SNOW2 Research Paper](https://docs.google.com/document/d/1Imp-BBaWYbqmGOgQ5amiGeykf2N4QkyHTzvVvJPT-b8/edit?usp=sharing)

## __Installation:__
To install, run "pip install -r requirements.txt" in terminal \
Note: "pip install git+https://github.com/PMEAL/porespy.git@dev" installs latest porespy! \

## __Code References:__
1. polydisperse_spheres: https://porespy.org/examples/generators/reference/polydisperse_spheres.html
2. open_pnm_to_im: https://porespy.org/modules/generated/generated/porespy.io.openpnm_to_im.html
3. predict fluid flow: https://openpnm.org/examples/applications/network_extraction.html

## __Dataset References:__
1. Berea Sandstone: https://www.digitalrocksportal.org/projects/317
2.
