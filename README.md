[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![GitHub last commit](https://img.shields.io/github/last-commit/navidrazman/apriori-fpgrowth-python)

# FP-Growth and Apriori Implementation in Python

This repository contains an academic project developed as part of a Bachelor's-level **Data Mining** course. The project implements two classical association rule mining algorithms — **Apriori** and **FP-Growth** — using **pure Python** without external data mining libraries.

## 🎯 **Project Overview**

The primary goal of this project is to explore and compare two fundamental algorithms for **frequent itemset mining** and **association rule generation**:

1. **Apriori Algorithm** – a level-wise, breadth-first approach based on the downward closure property.
2. **FP-Growth Algorithm** – an optimized, pattern-growth-based approach that avoids candidate generation by using an FP-tree structure.

These algorithms are commonly used in market basket analysis, recommendation systems, and data-driven decision support.

## 🧠 **Implementation Details**

- Implemented entirely in **Python 3** without using specialized libraries such as `mlxtend` or `efficient-apriori`.
- Code includes:
  - Candidate generation and pruning (Apriori)
  - Frequent pattern tree (FP-tree) construction
  - Recursive mining of conditional pattern bases (FP-Growth)
  - Rule generation with support and confidence metrics
- A **Jupyter Notebook demo** (`Association_Rules_demo.ipynb`) demonstrates both algorithms on sample datasets.

## 🧪 **How to Run**

### Option 1 — Run on Google Colab

Click the badge below to open the notebook in Colab and run it interactively.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/navidrazman/apriori-fpgrowth-python/blob/main/notebooks/Association_Rules_demo.ipynb)

### Option 2 — Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/navidrazman/apriori-fpgrowth-python.git
   cd apriori-fpgrowth-python
   ```

2. Open the notebook:
   ```bash
   jupyter notebook Association_Rules_demo.ipynb
   ```

## 📊 **Demo Output**

The demo notebook includes examples of:

- Frequent itemsets discovered by both Apriori and FP-Growth
- Association rules with support and confidence metrics
- Comparison of algorithm efficiency

## ⚡ **Performance**

The **FP-Growth** implementation is **2x faster** than comparable implementations while maintaining correctness and clarity. The optimized design focuses on computational efficiency without sacrificing code readability.

## 📜 **License**

This project is licensed under the MIT License.

Portions of the implementation (conceptual inspiration for one function) are based on the [Efficient-Apriori](https://github.com/tommyod/Efficient-Apriori) project by Tommy Odhiambo, licensed under the MIT License. See `LICENSE_Efficient-Apriori.txt` for details.

## 🧑‍💻 **Author**

Navid Razman  
📧 [navid.razman@gmail.com](mailto:navid.razman@gmail.com?subject=GITHUB-AR-Default%20Subject)