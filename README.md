---
title: CapiPort
emoji: 🤗
sdk: streamlit
sdk_version: 1.32.0
app_file: main.py
pinned: false
license: mit
---

# Portfolio Management for Indian Equity Markets
[![Build Status](https://github.com/bhanuprasanna527/CapiPort/actions/workflows/HF_sync_space.yml/badge.svg)](https://github.com/bhanuprasanna527/CapiPort/actions)


## Overview

Welcome to our project on portfolio management for Indian equity markets! This project aims to help individuals efficiently allocate their money between different equities, optimizing returns while managing risk.

## Features

- **Dynamic Allocation:** Our technique dynamically allocates funds among various equities based on a robust methodology.
- **Risk Management:** The project incorporates risk management strategies to enhance overall portfolio stability.
- **User-Friendly Interface:** Access the tool through our user-friendly web interface [here](https://capiport.streamlit.app/).

## Getting Started

Follow these steps to get started with the project:

1. Clone the repository:

   ```bash
   git clone https://github.com/bhanuprasanna527/CapiPort/

2. Install dependencies:
   ```bash
    pip install -r requirements.txt

3. Run the project:
   ```bash
    python main.py

## Technique used (Version 1) 
###  Mean-Variance Portfolio Optimization
Overview

Mean-Variance Portfolio Optimization is a widely used method in finance for constructing an investment portfolio that maximizes expected return for a given level of risk, or equivalently minimizes risk for a given level of expected return. This approach was pioneered by Harry Markowitz and forms the foundation of Modern Portfolio Theory (MPT).
Methodology
1. Basic Concepts

    Expected Return: The anticipated gain or loss from an investment, based on historical data or other factors.
    Risk (Variance): A measure of the dispersion of returns. In portfolio optimization, we seek to minimize the variance of the portfolio returns.

2. Optimization Algorithm
   
   Our implementation utilizes the following steps:
   Input Data: Historical returns for each asset in the portfolio.
   Objective Function: Construct an objective function that combines the expected return and variance.
   Optimization Algorithm: We employ a mean-variance optimization algorithm that iteratively adjusts the weights to find the optimal combination.
   Convergence Criteria: The algorithm iterates over a specified number of iterations (e.g., 5000) or until convergence is achieved.

3. Implementation

   In our project, we have implemented the Mean-Variance Portfolio Optimization method with 5000 iterations. The process involves:
   Input: Historical return data for each equity in the Indian market.
   Objective: Maximize expected return while minimizing portfolio variance.
   Optimization: Utilize an iterative approach, adjusting weights to find the optimal allocation.
   Output: The final set of weights that represent the optimal portfolio allocation.

#### Contributing
We welcome contributions! If you have any ideas for improvements, open an issue or submit a pull request.
License

This project is licensed under the MIT License.

## Links
1. **![Streamlit Deployment](https://capiport.streamlit.app/)**
2. **![HuggingFace Spaces](https://huggingface.co/spaces/sankhyikii/CapiPort)**
