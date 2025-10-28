# MBU Udskrivning 22 år – Opret Aftale

**Version:** 1.0.0

---

## 🔍 Overview

This project defines a Python-based Automation Server (ATS) process developed for Aarhus Kommune’s MBU automation platform.
The robot automatically identifies citizens who have just turned 22 years old in Solteq Tand and creates a booking reminder in the system.

It connects to the Solteq Tand database to find eligible citizens and uses GUI automation to open each patient’s record in the Solteq Tand application and create a booking with the correct aftaletype and aftalestatus.

---

## ⚙️ Main Responsibilities
- Identify citizens who turned 22 years old today
- Add them as workitems in the relevant ATS workqueue
- Open Solteq Tand via GUI automation
- Create a booking reminder with:
    - Aftaletype: Z - 22 år - Borger fyldt 22 år
    - Aftalestatus: 22 år - Afventer faglig vurdering
- Log in and out of Solteq Tand automatically
- Handle and report process or business errors

---

## ⚙️ How it works

1. The robot runs inside ATS and fetches citizens from the Solteq Tand database.
2. Each citizen is added to the queue as a workitem (with CPR as reference).
3. The robot opens Solteq Tand, searches for the patient, and creates the reminder booking.
4. Once all items are processed, the application is closed automatically.

---
