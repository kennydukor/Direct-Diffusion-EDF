# Diffusion EDF
Blah Blah
# Installation

**Step 1.** Clone Github repository.
```shell
git clone --recursive https://github.com/tomato1mule/diffusion_edf
```

**Step 2.** Setup Conda/Mamba environment. We recommend using Mamba for faster installation.
```shell
# if you don't have mamba yet, install it first (not needed when using mambaforge):
conda install mamba -c conda-forge

# now create a new environment
mamba create -n diff_edf python=3.8
conda activate diff_edf
```

**Step 3.** Install Diffusion EDF.
```shell
mamba install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 -c pytorch
mamba install -c fvcore -c iopath -c conda-forge fvcore==0.1.5.post20221221 iopath==0.1.9
mamba install pytorch3d==0.7.2 -c pytorch3d
mamba install pyg==2.1.0 -c pyg
pip install -e .
```