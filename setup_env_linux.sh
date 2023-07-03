CONDA_BASE=$(conda info --base) 
conda create --name seedz python==3.10
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate seedz
pip install -r requirements.txt