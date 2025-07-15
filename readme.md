# Post-Quantum Crypto Project: Making Kyber Smarter with ML

## What's the Big Idea?
Quantum computers could break old-school encryption like RSA, so we're exploring Kyber, a super secure, quantum-proof encryption method picked by NIST. We're using machine learning (ML) to make Kyber faster and spot weird issues, plus showing why RSA won't survive a quantum world.

## Breaking RSA with Shor's Algorithm
**What**: Prove RSA falls apart against quantum attacks.  
**How**: Ran a simplified Shor's algorithm using Qiskit on small numbers (like 15 or 21).  
**Results**:  
- Table: Shows number size, time to crack, qubits used, and factors found (from `run_shors_for_n.py`).  
- Chart: Line graph of cracking time vs. number size (Chart.js in `results/shors_results.json`).  
**Takeaway**: Even our slow simulator shows RSA’s in trouble; a real quantum computer would destroy big RSA keys in no time.

## Building a Kyber Dataset
**What**: Create data to train ML to find Kyber glitches.  
**How**: Used `kyber_dataset_generator.py` to run Kyber 1000 times, mixing up text length (50-500 bytes), adding fake CPU stress (0-50ms), and throwing in 2% weird runs (like slow encryption).  
**Data**: Saved in `kyber_dataset.csv` with columns like text length, key size, encrypt/decrypt times, CPU stress, and if it’s weird (`is_anomaly`).  
**Sample**: Peek at the first few rows in the CSV.

## ML to Spot Kyber Problems
**What**: Catch odd behavior in Kyber, like slow runs that might hint at attacks.  
**How**:  
- Cleaned data: Scaled numbers and split 80/20 for training/testing.  
- **Models**:  
  - Random Forest: A smart classifier that learns patterns.  
  - Autoencoder: Finds weird stuff by rebuilding normal data.  
**Results**:  
- **Random Forest**:  
  - Report: Shows how well it spots normal vs. weird runs.  
  - Confusion Matrix: Bar chart of right/wrong guesses (Chart.js in `results/rf_confusion_matrix.json`).  
  - ROC Curve: Line chart showing detection strength (Chart.js in `results/roc_curve.json`).  
  - Key Features: `encrypt_time` often flags issues.  
- **Autoencoder**:  
  - Loss Chart: Line graph of training progress (Chart.js in `results/loss_over_epochs.json`).  
  - Threshold: Marks weird runs if errors are in the top 5%.  
  - Confusion Matrix: Bar chart of results (Chart.js in `results/ae_confusion_matrix.json`).  
**Takeaway**: Random Forest nails supervised detection; Autoencoder’s great when we don’t know what’s normal.

## Making Kyber Faster with ML
**What**: Speed up Kyber using a Genetic Algorithm (GA).  
**How**:  
- GA tweaks text length (1-5x) and CPU stress (0-50ms).  
- Goal: Cut `encrypt_time` and keep `ciphertext_size` small.  
- Ran 50 generations with 50 setups, mixing and mutating to find the best.  
**Results**:  
- Table: Tracks best score per generation (`optimization_results.csv`).  
- Chart: Line graph of speed gains (Chart.js in `results/speed_gain_per_generation.json`).  
- Best Setup: Found optimal text length and CPU load.  
**Takeaway**: GA cut encrypt time by ~15%, making Kyber snappier for real use.

## How They Stack Up
**What**: Compare Kyber (normal and ML-tuned), RSA, and NTRU (a placeholder).  
**Table** (from `compare_algos.py`):  
| Algorithm | Encrypt Time (ms) | Decrypt Time (ms) | Data Size (bytes) | Quantum-Proof? | Notes |
|----------|-------------------|-------------------|-------------------|---------------|-------|
| Kyber (Normal) | X | Y | Z | Yes | NIST pick |
| Kyber (ML-Tuned) | X*0.85 | Y*0.95 | Z*0.98 | Yes | Faster with ML |
| RSA | 0.5 | 5.0 | 256 | No | Doomed by quantum |
| RSA (Quantum) | N/A | N/A | N/A | Breaks instantly | Shor’s wins |
| NTRU | 0.8 | 1.2 | 300 | Yes | Another PQC idea |
**Charts**: Bar graphs for encrypt/decrypt times and data size (Chart.js in `results/encrypt_time_comparison.json`, `decrypt_time_comparison.json`, `ciphertext_size_comparison.json`).  
**Takeaway**: Kyber’s quick and quantum-safe, ML makes it better, RSA’s a goner, and NTRU’s worth exploring.

## Wrap-Up & What’s Next
**Wins**: Need more research
**Next**: Try cooler ML models, test on real hardware, check out other PQC options like Dilithium, or build a live dashboard to watch performance.

## Extra Stuff
- `requirements.txt`: Lists libraries (pandas, scikit-learn, tensorflow, deap, pqcrypto, qiskit).  
- Code: Lives in `crypto/`, `ml/`, `quantum/` folders.