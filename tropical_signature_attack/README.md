# A Comprehensive Break of the Tropical Matrix-Based Signature Scheme

This repository contains the implementation and experimental evaluation of attacks on the signature scheme proposed in the recent preprint, Tropical Cryptography IV: Digital Signatures and Secret Sharing with Arbitrary Access Structure
## Repository Structure

src/ – implementation of tropical algebra and the signature scheme

experiments/ – scripts demonstrating the attacks

challenge/ – challenge generation scripts

## Running Experiments

Install dependencies:

pip install -r requirements.txt

Run the malleability attack:

python experiments/malleability_demo.py

Run timing experiments:

python experiments/timing_N_signatures.py

## Disclaimer

This code is provided for academic research purposes only.

## Author

Research implementation for cryptanalysis of tropical signature schemes.
## Reproducibility

All experiments in the paper can be reproduced by running the scripts in the `experiments` folder.

Example:

python experiments/malleability_demo.py
python experiments/timing_N_signatures.py
