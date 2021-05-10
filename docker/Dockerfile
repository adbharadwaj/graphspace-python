FROM ubuntu:20.04

# create conda environment in advance and activate on run

# install tools
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

# install miniconda and configure bashrc
ENV PATH /opt/conda/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean --all && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    conda init bash

WORKDIR /home/graphspace-python

# create graphspace-python conda environment
COPY docker/minimal_env.yml ./docker/
# requests module no longer part of conda - see https://github.com/vitchyr/rlkit/issues/107
# for info about the CONDA_RESTORE_FREE_CHANNEL option.
RUN CONDA_RESTORE_FREE_CHANNEL=1 conda env create -f docker/minimal_env.yml && \
    echo "conda activate graphspace-python" >> ~/.bashrc

# install graphspace-python
COPY graphspace_python/ ./graphspace_python

# add an ENV entry so graphspace_python can be accessed anywhere:
# https://stackoverflow.com/questions/49631146/how-do-you-add-a-path-to-pythonpath-in-a-dockerfile/49631407
ENV PYTHONPATH "${PYTHONPATH}:/home/graphspace-python"
