# log-analyzer

## Overview
A tool for analyzing logs for anomaly detection

## Problem Statement
This project aims to solve the problem, when a service is producing a tones of logs, in which it is hard to identify when something is wrong by looking at all these logs. With this project, it helps to identify anomalies from the logs.

## Features
- Log Ingestor
- Anomaly Detector
- Report Generator

## Tech Stack
- Language: Python
- Framework: 
- Database:
- Other tools:

## Project Structure
```text
src/
logs/
config/
README.md

## Running Locally

```bash
poetry install
poetry run uvicorn app.main:app --reload