# 🛡️ Next-Gen AI-Driven Intrusion Prevention System (IPS) Core

An Enterprise-Grade Network Security & Intrusion Prevention System (IPS) built using Python Flask, WebSockets, and Machine Learning. The platform features an advanced Cyberpunk-inspired SOC telemetry console, real-time geospatial threat mapping, and an active LSTM-driven predictive risk engine.

---

## 🌐 Live Interactive Dashboard Preview
👉 **[Click Here to Access the Live UI Sandbox](https://kaadi127.github.io/AI-IPS-Cyber-Core/)**

> 💡 **Note on Deployment Architectures:** The link above serves as an interactive frontend sandbox simulating live telemetry logic. Active network packet interception (Scapy) and native host operating system hardening (Windows Firewall `netsh` rule injections) run exclusively within secured internal network nodes for architecture protection.

---

## 🚀 Key Architectural Modules

### 1. 🧠 ML Anomaly Engine (Isolation Forest)
Continuous stream analytics engine utilizing an automated Isolation Forest pipeline to classify structural patterns of packet behaviors, distinguishing between standard traffic baselines and malicious ingress bursts.

### 2. 📈 LSTM Time-Series Risk Forecasting
A predictive Deep Learning layer running background mathematical loops to compute upcoming threat vectors and DDoS velocity probabilities over a rolling 2-hour window.

### 3. 🛡️ Native OS Hardening & Port-Scan Blocker
An active Host IPS (HIPS) module running persistent background telemetry checking routines. If internal node scanning or sequential port-flooding behavior is recognized, it immediately executes native shell adjustments to inject dropping rules into the **Windows Advanced Firewall**:
```bash
netsh advfirewall firewall add rule name="NIDS_BLOCK_ATTACKER_IP" dir=in action=block remoteip=ATTACKER_IP
