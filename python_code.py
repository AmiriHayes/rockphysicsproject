# %% [markdown]
# # Permeability Simulation Using PoreSpy and OpenPNM
# This simulation is based on the original notebook [Berea Sandstone Simulation Using PoreSpy and OpenPNM](https://github.com/PMEAL/OpenPNM/blob/master/examples/simulations/Berea%20Sandstone%20-%20Effective%20Permeability.ipynb)

# %% [markdown]
# ### Start by importing the necessary packages

# %%
import numpy as np
import openpnm as op
import porespy as ps
import matplotlib.pyplot as plt
np.set_printoptions(precision=4)
np.random.seed(10)
%matplotlib inline

# %% [markdown]
# ### Load Sandstone Data

# %%
resolution = 2.25e-6
name = 'Bentheimer'

# %%
# Read input RAW file
raw_file = np.fromfile('Sandstones/'+name+'_2d25um_binary.raw', dtype=np.uint8)
im = (raw_file.reshape(1000,1000,1000))
im = im==0;

# %% [markdown]
# ### Confirm image and check image porosity
# 

# %%
#NBVAL_IGNORE_OUTPUT
fig, ax = plt.subplots(1, 3, figsize=(12,5))
ax[0].imshow(im[:, :, 100]);
ax[1].imshow(ps.visualization.show_3D(im[:250,:250,:250]));
ax[2].imshow(ps.visualization.sem(im[:250,:250,:250]));
ax[0].set_title("Slice No. 100 View");
ax[1].set_title("3D Sketch");
ax[2].set_title("SEM View");

# %%
print(ps.metrics.porosity(im))
print(im.shape)
print(im.dtype)

# %% [markdown]
# ### Extract pore network using SNOW algorithm in PoreSpy

# %% [markdown]
# The SNOW algorithm (an accronym for Sub-Network from an Oversegmented Watershed) was presented by [Gostick](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.96.023307). 

# %%
net = ps.networks.snow(im=im, voxel_size=resolution)

# %% [markdown]
# ### Import network in OpenPNM

# %% [markdown]
# The output from the SNOW algorithm above is a plain python dictionary containing all the extracted pore-scale data, but it is NOT yet an OpenPNM network. We need to create an empty network in OpenPNM, then populate it with the data from SNOW:

# %%
ws = op.Workspace()
proj = op.Project()
pn = op.network.GenericNetwork(name=name, project=proj)
pn.update(net)  # Fills 'pn' with data from 'net'

# %% [markdown]
# ## Optional: load already saved network

# %%
proj = op.io.OpenpnmIO.load_project('Bentheimer.pnm');
pn = proj.network;

# %% [markdown]
# Now we can print the network to see how the transferred worked:

# %%
print(pn)

# %% [markdown]
# ### Check network health

# %% [markdown]
# Remove isolated pores or cluster of pores from the network by checking it network health. Make sure ALL keys in network health functions have no value. 

# %%
h = pn.check_network_health()
op.topotools.trim(network=pn, pores=h['trim_pores'])
h = pn.check_network_health()
print(h)

# %% [markdown]
# ### Assign geometry

# %%
geo = op.geometry.GenericGeometry(network=pn, pores=pn.Ps, throats=pn.Ts)

# %% [markdown]
# ### Assign phase

# %% [markdown]
# In this example air is considered as fluid passing through porous channels. 

# %%
water = op.phases.Water(network=pn)

# %% [markdown]
# ### Assign physics

# %%
phys_water=op.physics.GenericPhysics(network=pn, phase=water, geometry=geo)
R = geo['throat.diameter']/2.0;
L = geo['throat.length'];
phys_water['throat.hydraulic_conductance'] = (np.pi*(R**4))/(8*water['pore.viscosity'].max()*L)

# %% [markdown]
# ### Calculate effective permeability

# %% [markdown]
# Caclulate effective permeablity using hagen poiseuille equation. Use cross section area and flow length manually from image dimension. 

# %%
A = (1000*1000) *resolution**2
L = 1000 * resolution
mu = water['pore.viscosity'].max()
Pressure = 10e3;
delta_P = Pressure - 0
#X
perm = op.algorithms.StokesFlow(network=pn, project=proj)
perm.setup(phase=water)
perm.set_value_BC(pores=pn.pores('top'), values=0)
perm.set_value_BC(pores=pn.pores('bottom'), values=Pressure)
perm.run()
Q = perm.rate(pores=pn.pores('bottom'), mode='group')
K = Q * L * mu / (A * delta_P)
print('X:', K/0.98e-12*1000, 'mD')

#y
perm = op.algorithms.StokesFlow(network=pn, project=proj)
perm.setup(phase=water)
perm.set_value_BC(pores=pn.pores('front'), values=0)
perm.set_value_BC(pores=pn.pores('back'), values=Pressure)
perm.run()
Q = perm.rate(pores=pn.pores('back'), mode='group')
K = Q * L * mu / (A * delta_P)
print('Y:', K/0.98e-12*1000, 'mD')

#z
perm = op.algorithms.StokesFlow(network=pn, project=proj)
perm.setup(phase=water)
perm.set_value_BC(pores=pn.pores('left'), values=0)
perm.set_value_BC(pores=pn.pores('right'), values=Pressure)
perm.run()
Q = perm.rate(pores=pn.pores('right'), mode='group')
K = Q * L * mu / (A * delta_P)
print('Z:', K/0.98e-12*1000, 'mD')

# %%



