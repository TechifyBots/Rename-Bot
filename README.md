<div align="center">

<img src="https://bannerrender.vercel.app/api?type=waving&height=300&color=gradient&text=𝗥𝗲𝗻𝗮𝗺𝗲%20𝗕𝗼𝘁&fontAlignY=35&fontSize=80&desc=𝗚𝗶𝘃𝗶𝗻𝗴%20𝗬𝗼𝘂𝗿%20𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺%20𝗙𝗶𝗹𝗲𝘀%20𝗮%20𝗠𝗮𝗸𝗲𝗼𝘃𝗲𝗿&descAlignY=60"/>

<p align="center">

A **powerful, open-source, and feature-rich** Telegram bot designed to **rename, customize, and transform files effortlessly** with support for **custom thumbnails, metadata, captions, and video conversion**.

⚡ Fast • 📝 Flexible • 🖼️ Customizable

</p>


[![Last Commit](https://img.shields.io/github/last-commit/TechifyBots/Rename-Bot?style=for-the-badge)](https://github.com/TechifyBots/Rename-Bot/commits)
<br>
[![CI](https://github.com/bisug/Rename-Bot/actions/workflows/ci.yml/badge.svg)](https://github.com/bisug/Rename-Bot/actions/workflows/ci.yml)
[![CodeQL](https://github.com/bisug/Rename-Bot/actions/workflows/codeql.yml/badge.svg)](https://github.com/bisug/Rename-Bot/actions/workflows/codeql.yml)
<br>
[![GitHub Stars](https://img.shields.io/github/stars/TechifyBots/Rename-Bot?style=for-the-badge)](https://github.com/TechifyBots)
[![GitHub Forks](https://img.shields.io/github/forks/TechifyBots/Rename-Bot?style=for-the-badge)](https://github.com/TechifyBots/Rename-Bot/fork)
<br>
[![Repo Size](https://img.shields.io/github/languages/code-size/TechifyBots/Rename-Bot?style=for-the-badge&color=8B5CF6)](https://github.com/TechifyBots/Rename-Bot)

</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/TechifyBots/TechifyBots/main/assets/divider.svg" width="600" alt="divider"/>
</p>

## 📑 Table of Contents

- 🌸 **[Overview](#-overview)**
- ✨ **[Features](#-features)**
- 🎥 **[Quick Start](#-quick-start)**
- ⚙️ **[Configuration](#-configuration)**
- 🤖 **[Commands](#-commands)**
- 🚀 **[Deployment](#-deployment)**
- 🤝 **[Contributing](#-contributing)**
- 📄 **[License](#-license)**
- 💬 **[Updates & Support](#-updates--support)**
- 🙌 **[Credits](#-credits)**
- 👨‍💻 **[Connect With Me](#-connect-with-me)**

---

## 🌸 Overview

**Rename Bot** is a powerful Telegram file management bot that goes **far beyond simple renaming**. It combines **4GB file support, premium plans, thumbnails, metadata, captions, and file conversion** into one convenient Telegram-based workflow.

> 💡 *Take full control of your files with powerful customization tools.*

### 🤔 Why Choose This Project?

- ⚡ **Fast & Powerful** — Process and rename files quickly with support for large files.
- 🎨 **Highly Flexible** — Customize your files with powerful options tailored to your needs.
- 💎 **Premium Ready** — Built-in plans and premium features for enhanced capabilities.
- 🚀 **Easy to Deploy** — Ready for self-hosting across multiple popular platforms.

### 🔄 How It Works

1. 📤 **Send Your File** — Upload the file you want to rename or process.
2. ⚙️ **Choose Your Options** — Configure your filename and preferred customization settings.
3. 🔄 **Let the Bot Process** — The bot applies your selected settings automatically.
4. 📥 **Get the Result** — Receive your customized file back through Telegram.

---

## ✨ Features

- ⚡ **Fast File Renaming** — Rename files quickly with an efficient Telegram-based workflow.
- 📦 **4GB File Support** — Process large files with upgraded 4GB support.
- 💎 **Premium Plans** — Offer upgraded limits and premium capabilities for users.
- 🖼️ **Thumbnail Customization** — Set permanent custom thumbnails for your files.
- 📝 **File Customization** — Personalize filenames, captions, prefixes, suffixes, and metadata.
- 🔄 **File Conversion** — Convert supported files between video and document formats.
- ♾️ **Unlimited Renaming** — Rename multiple files without a fixed renaming limit.
- 📢 **Broadcast System** — Send announcements and updates to all registered users.
- 🔐 **Force Subscribe** — Require users to join configured channels before using the bot.
- 🛡️ **User Management** — Ban, unban, and manage users directly from the bot.
- 🔧 **Maintenance Mode** — Temporarily pause bot services whenever maintenance is required.
- 🚀 **Multi-Platform Deployment** — Deploy easily on Koyeb, Heroku, Railway, and Render.

---

## 🎥 Quick Start

New to this project?

Watch this short video to understand **what the bot is**, **why it's useful**, **how it works**, explore its **key features**, and learn the **required configuration** before deployment.

📺 **Watch on YouTube: *[Project Overview](https://youtu.be/9q77WrKnm9k)***

---


## 📝 Configuration

| Variable | Description |
|:---------|:------------|
| `API_ID` | Telegram API ID |
| `API_HASH` | Telegram API Hash |
| `BOT_TOKEN` | Telegram Bot Token |
| `DB_URL` | MongoDB URI |
| `DB_NAME` | MongoDB database name *(default: `Rename_Bot`)* |
| `ADMIN` | Telegram User ID |
| `PIC` | Start image URL |
| `BIN_CHANNEL` | Bin Channel |
| `IS_FSUB` | Enable / Disable Force Subscribe |
| `FSUB_EXPIRE` | Force Subscribe Expire Time |
| `AUTH_CHANNELS` | Force Subscribe Channels |
| `AUTH_REQ_CHANNELS` | Request FSUB Channels (membership verified live) |
| `LOG_CHANNEL` | Log Channel |
| `STRING_SESSION` | Session string required for 4GB file processing |
| `PORT` | Web server port *(default: `8080`)* |

### 📝 Notes

> 💎 **4GB Support** — `STRING_SESSION` is **optional**. Add a **Kurigram v2 String Session** (Pyrogram-compatible) to enable 4GB file processing.

> ⚠️ **Without `STRING_SESSION`**, the bot will continue to work with its standard file-size limit.

### 📚 Setup Guides

- 🔑 **Telegram API ID & API Hash** — [Watch Tutorial](https://youtu.be/y5FwAobQ-Kc)
- 🤖 **Bot Token** — [Watch Tutorial](https://youtu.be/rUEKDOSPFho)
- 🍃 **MongoDB Database** — [Watch Tutorial](https://youtu.be/j8LIuM7vv18)

---

## 🤖 Commands

<details>
<summary><b>👤 User Commands</b></summary>

```
start - Check Bot Alive.
setprefix - Set Your Prefix
seeprefix - See Your Prefix
delprefix - Delete Your Prefix
viewthumb - To View Current Thumbnail.
delthumb - To Delete Current Thumbnail.
setcaption - To Set A Custom Caption.
seecaption - To See Your Custom Caption.
delcaption - To Delete Custom Caption.
setsuffix - Set Your Suffix
seesuffix - See Your Suffix
delsuffix - Delete Your Suffix
plans - to check all available plans.
myplan - to check your active plan.
metadata - To set custom metadata.
```

</details>

<details>
<summary><b>🔒 Owner Commands</b></summary>

```
ban - ban a user.
unban - unban a user.
banned - list all banned users.
status - get bot statistics.
broadcast - Send message to users.
logs - get recent bot logs.
addpremium - add a user to premium
removepremium - remove a user from premium
restart - restart the bot.
maintenance - Toggle maintenance mode.
delreq - Clear pending force-subscribe join requests.
```
</details>


<p align="center">
  <img src="https://raw.githubusercontent.com/TechifyBots/TechifyBots/main/assets/divider.svg" width="600" alt="divider"/>
</p>

## 🚀 Deployment

Need help deploying this project? We've got you covered.

> [!TIP]
> 📺 **Complete Deployment Playlist** — Follow the step-by-step video tutorials to get started.
>
> **▶ [Watch on YouTube](https://www.youtube.com/playlist?list=PLQrMSile4s5UnIEvWyKM1MKFuNg8Wfh2S)**

### Prerequisites

- Python **3.14.7** (see `.python-version`; Docker uses `python:3.14-slim`)
- [ffmpeg](https://ffmpeg.org/download.html) on `PATH` (metadata + thumbnails; `ffprobe` too)
- MongoDB database (URI for `DB_URL`)
- Telegram `API_ID` / `API_HASH` / `BOT_TOKEN`, plus `ADMIN` user ID

### Run locally

```bash
pip install -r requirements.txt
export API_ID=… API_HASH=… BOT_TOKEN=… ADMIN=… DB_URL=mongodb://localhost:27017 LOG_CHANNEL=…
python bot.py
```

### Deploy targets (all wired in this repo)

| Platform | File | Notes |
|:---------|:-----|:------|
| Docker (any host) | `Dockerfile` | `ffmpeg` + Ookla speedtest baked in; `CMD ["python", "bot.py"]` (`bot.py` entrypoint) |
| Heroku | `app.json`, `Procfile`, `heroku.yml` | One-click via `app.json`; all 14 env vars declared |
| Render | `render.yaml` | Free web service, `autoDeploy: false`; all 14 env vars declared |
| Koyeb / Railway | `Dockerfile` | Deploy from repo, use the Docker builder, set env vars below |

### Required environment variables

All 14 are declared in `app.json` and `render.yaml` (CI's `validate` job fails the PR if they drift from `config.py`):

`API_ID` · `API_HASH` · `BOT_TOKEN` · `DB_URL` · `DB_NAME` · `ADMIN` · `PIC` · `BIN_CHANNEL` · `LOG_CHANNEL` · `STRING_SESSION` · `IS_FSUB` · `AUTH_CHANNELS` · `AUTH_REQ_CHANNELS` · `FSUB_EXPIRE` · (`PORT` is injected by the host, default `8080`)

> 💎 **4GB Support** — `STRING_SESSION` is **optional**. Add a **Kurigram v2 String Session** (Pyrogram-compatible) to enable 4GB file processing. Without it the bot keeps its standard 2GB limit.

### CI — what runs before deploy

Every push/PR runs [`.github/workflows/ci.yml`](.github/workflows/ci.yml) (badge ↑ top):

| Job | What it catches |
|:----|:----------------|
| `build` | Syntax errors (`compileall`), bug-class lint (`ruff F,E9`), plugin wiring (38 handlers + web routes smoke test) |
| `audit` | Known CVEs in `requirements.txt` (`pip-audit`, advisory) |
| `validate` | `config.py` ↔ `app.json` ↔ `render.yaml` env drift · unparseable manifests · Docker base ≠ `.python-version` · stale `welcome.html` placeholders · hardcoded secrets / committed session files |
| CodeQL | Python security analysis (weekly + per-push, [config](.github/workflows/codeql.yml)) |


---

## 🤝 Contributing

*Contributions are always appreciated! ❤️*

| 🐞 **Report Bugs** | 💡 **Suggest Features** | 🚀 **Submit PRs** |
|:------------------:|:-----------------------:|:-----------------:|
| Found an issue? | Have an idea? | Ready to contribute? |
| **[Open Issue](https://github.com/TechifyBots/Rename-Bot/issues)** | **[Open Discussion](https://github.com/TechifyBots/Rename-Bot/issues)** | **[Fork & Submit](https://github.com/TechifyBots/Rename-Bot/fork)** |

> [!IMPORTANT]
> *Before opening an issue, please ensure you're using the **[latest version](https://github.com/TechifyBots/Rename-Bot)** and have followed the **[deployment guide](https://www.youtube.com/playlist?list=PLQrMSile4s5UnIEvWyKM1MKFuNg8Wfh2S)**.*

---

## 📄 License

<p align="center">
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge&logo=apache&logoColor=white" alt="License" />
  </a>
</p>

> [!WARNING]
> *This project is intended **strictly for educational purposes only**. The author is **not responsible** for any misuse or abuse. Please comply with all applicable laws and the terms of any third-party services. If you modify or redistribute this project, please provide proper credit to the original repository.*

See the **[LICENSE](./LICENSE)** file for complete details.

---

## 🫂 Updates & Support

<div align="center">

<a href="https://telegram.me/TechifyBots"><img src="https://tgcards.vercel.app/?username=TechifyBots&theme=light&verified=true" alt="Channel"></a>
<br>
<a href="https://telegram.me/TechifySupport"><img src="https://tgcards.vercel.app/?username=TechifySupport&theme=light" alt="Group"></a>

</div>

---

## 🙌 Credits

This repository is based on the original work of:

- **Original Developer:** [DigitalBotz](https://github.com/DigitalBotz)

> [!NOTE]
> This repository is maintained by **TechifyBots**, with improvements to the project presentation and user experience.

<p align="center">
  <img src="https://raw.githubusercontent.com/TechifyBots/TechifyBots/main/assets/divider.svg" width="600" alt="divider"/>
</p>

## 👤 Connect With Me

<p align="center">
  <b style="font-size: 5.5em;">Rahul Dhankhar</b>
  <br/>
  <sub><i>Open Source Maintainer • TechifyBots</i></sub>
<br/><br/>
<a href="https://github.com/TechifyBots"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"></a>
<a href="https://telegram.me/ImRahulDhankhar"><img src="https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white"></a>
<a href="https://instagram.com/ImRahulDhankhar"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>
<a href="https://youtube.com/@TechifyBots"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"></a>
<br>
<a href="https://techifybots.github.io/PayWeb">
  <img src="https://img.shields.io/badge/💖-Support_Development-ff4d6d?style=for-the-badge">
</a>
</p>