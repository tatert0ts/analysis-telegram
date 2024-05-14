# Telegram Chat Analysis Tool

## Overview
This repository is dedicated to exploring the everyday use of Telegram. By analyzing exported Telegram conversations, I aimed to uncover valuable insights and summary statistics about communication patterns, frequently discussed topics, and other relevant metrics.

To achieve this, I leveraged the power of Plotly for data visualization and Streamlit for interactive web-based visualization. The analysis results are also hosted on Streamlit, providing a user-friendly interface for exploring the insights derived from the Telegram conversation data.

Visit the Streamlit Dashboard [here!](https://telegram-analysis.streamlit.app/)

![image](https://github.com/tatert0ts/analysis-telegram/assets/165807891/c757eaec-f2fe-4e4f-b58e-dcb889a53fe5)


## Files

1. **main.py**: This file acts as the primary script for executing the Streamlit application on localhost. It manages the user interface and interaction with the analysis results.

2. **calculations.py**: This file contains the code responsible for data cleaning and preprocessing. The processed data is utilized to generate visuals that are subsequently referenced in `main.py`.

3. **markdown.py**: This file contains markdown formatting and text snippets intended to be referenced and displayed within `main.py`.

## Getting Started

### 1. Clone the Repository
   ```
   git clone https://github.com/tatert0ts/analysis-telegram.git
   ```
### 2. Install Dependencies
   ```
   pip install -r requirements.txt
   ```
### 3. Run the Dashboard
   ```
   python main.py
   ```
## Contributors
- Tan Jia Yin
