# Contributing to vattenfall_tijdprijs

Thank you for your interest in contributing to **vattenfall_tijdprijs** 🎉  
This project is open source, but with strong guarantees that improvements remain available to the community.

Please read this document carefully before contributing.

---

## 📜 License & Legal Framework

This project is licensed under the **GNU Affero General Public License v3 (AGPL-3.0)**.

By contributing to this project, you agree that:

- Your contribution will be licensed under **AGPL-3.0**
- Any derivative work or modification you deploy or distribute
  **must also be made publicly available under AGPL-3.0**
- This applies **including use over a network**, such as Home Assistant installations

➡️ In short: **improvements must remain open source**.

---

## 🔁 Sharing Modifications

You are **not legally required** to submit a Pull Request to this repository.

However:

- If you modify this project and deploy or distribute it,
  you **must publish the full source code** of your changes
- Publishing as a **public fork** is acceptable
- Submitting a **Pull Request to this repository is strongly encouraged**

> The intent of this project is collaboration, not fragmentation.

---

## ✅ What Contributions Are Welcome?

We welcome contributions including, but not limited to:

- Bug fixes
- Performance improvements
- New tariff models or providers
- Configuration or UX improvements
- Documentation improvements
- Tests and validation logic

All contributions should align with:
- Home Assistant best practices
- Clean, readable Python code
- Backwards compatibility where possible

---

## 🧪 Development Guidelines

Please ensure that:

- Code follows **PEP8**
- New features are configurable via `config_flow`
- Constants are placed in `const.py`
- Sensors have clear names and units
- Prices are treated as **inclusive of VAT**, unless explicitly stated otherwise
- No hardcoded supplier-specific assumptions outside configuration

---

## 🧾 Commit & PR Guidelines

If you submit a Pull Request:

- Use clear, descriptive commit messages
- One logical change per PR where possible
- Explain *why* the change is needed, not just *what* changed
- Reference related issues if applicable

The maintainer reserves the right to:
- Request changes
- Reject PRs that conflict with project goals
- Delay merging until alignment is clear

---

## 🚫 What Is Not Allowed

- Closed-source forks
- Proprietary extensions that depend on this code
- Removing or weakening the AGPL license
- Misrepresenting tariff calculations or legal status
- Claiming endorsement by Vattenfall or Home Assistant

---

## 🧠 Project Philosophy

This integration exists to:

- Provide transparent and correct energy pricing
- Empower Home Assistant users
- Prevent vendor lock-in or closed derivatives

If that philosophy does not align with your goals,  
this project may not be the right fit.

---

## 🙏 Thank You

By contributing, you help keep energy pricing transparent and fair.

Questions or ideas?  
Open an issue — discussion is always welcome.
