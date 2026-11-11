**English** · [Español](USER_MANUAL.es.md)

# Teleco SLM — User Manual

**Version 1.0.0 · June 2026**

Local LLM inference for telecommunications engineering. Runs Qwen 3 1.7B Fine-tuned with llama.cpp on CPU, fully offline.

Arturo Fierro Pardo — Universidad CEU San Pablo

---

## Contents

1. [Introduction](#1-introduction)
2. [System requirements](#2-system-requirements)
3. [Installation](#3-installation)
4. [First launch and setup](#4-first-launch-and-setup)
5. [Using the application](#5-using-the-application)
6. [Settings](#6-settings)
7. [Inference metrics](#7-inference-metrics)
8. [Data management](#8-data-management)
9. [Troubleshooting](#9-troubleshooting)
10. [Technical information](#10-technical-information)

---

## 1. Introduction

Teleco SLM is a generative AI application built for students and professionals in telecommunications engineering. It lets you ask questions about telecommunications-specific content and get answers from a specialised language model that runs entirely on your own device.

The embedded model is **Qwen 3 1.7B Fine-tuned**, a Small Language Model (Mini-SLM) tuned with LoRA over a corpus of 24,680 question–answer pairs drawn from the Telecommunications Engineering syllabus at Universidad CEU San Pablo. The model ships in GGUF format (Q4_K_M quantisation, ~1.1 GB) and runs through llama.cpp, which allows efficient CPU inference with no dedicated GPU and no internet connection.

The application is available for Android and Windows, with an inference architecture adapted to each platform.

**Key features**

- 100% offline inference: your data never leaves the device.
- A model specialised in telecommunications, with support for mathematical formulas.
- LaTeX expression rendering inside the answers.
- Conversation history stored locally (SQLite).
- Performance metrics panel (tokens/s, latency, memory).
- Direct model download from Hugging Face, or loading a local file.
- Optional connection to a remote `llama-server` on the local network.

---

## 2. System requirements

### 2.1 Android

| Component | Requirement |
|-----------|-------------|
| Operating system | Android 8.0 (API 26) or later |
| Architecture | ARM64 (aarch64) |
| Minimum RAM | 4 GB (6 GB or more recommended) |
| Storage | ~1.5 GB free (model + application) |
| GPU | Not required (CPU inference with NEON) |
| Internet connection | Only for the initial model download |

### 2.2 Windows

| Component | Requirement |
|-----------|-------------|
| Operating system | Windows 10/11 (64-bit) |
| Minimum RAM | 4 GB (8 GB recommended) |
| Storage | ~1.5 GB free (model + application) |
| Dependency | `llama-server.exe`, included in the installation |
| Internet connection | Only for the initial model download |

---

## 3. Installation

### 3.1 Android

The application is distributed as an APK file. To install it:

1. Download `TelecoSLM.apk` onto the Android device.
2. Open the downloads folder with a file manager.
3. Tap the APK file. The first time, the system will ask you to allow installation from unknown sources under **Settings > Security**.
4. Confirm the installation and wait for it to finish.
5. Open the app from the app drawer.

The application is also available on the Google Play Store.

### 3.2 Windows

On Windows, the application is distributed as a portable folder or an installer:

1. Download the TelecoSLM distribution folder for Windows.
2. Extract the contents to `C:\Program Files\TelecoSLM\` or your preferred location.
3. Run `TelecoSLM.exe` to start the application.
4. The inference server `llama-server.exe` starts automatically in the background when the model loads.

---

## 4. First launch and setup

The first time you open the application you need the language model in place before you can run any inference. The **Settings** screen is where you configure the model source.

### 4.1 Downloading the model

The **Local Model** section of the settings shows the information for the preconfigured model: Qwen 3 1.7B Fine-tuned in Q4_K_M format (~1.1 GB). There are two ways to obtain it:

- **Download model** — automatically downloads the GGUF file from the Hugging Face repository. Requires an internet connection. Progress is shown on screen.
- **Select GGUF file** — loads a GGUF file already stored on the device. Useful if the model was downloaded earlier or transferred over USB.

![Settings screen — Local Model and Remote Server](manual/manual-01-settings-model.png)

*Figure 1. Settings screen — Local Model and Remote Server.*

Once the model is downloaded or selected, its path appears in the corresponding field and the **Model active** indicator (green dot) is shown in the application header, confirming the model is loaded and ready.

### 4.2 Remote server

Alternatively, the application can connect to a `llama-server` instance running on another machine on the local network. Enter the server's IP address and port (for example, `192.168.1.100:8089`) in the **Remote Server** section and press **Connect**.

> **Note:** Remote mode is useful for low-end Android devices: the model runs on a more powerful PC and the phone acts as the interface.

---

## 5. Using the application

### 5.1 Main screen

The main screen shows the application name, the model status and access to the main functions:

- **Status indicator** — the green "Model active" badge confirms the model is loaded. If the model has not been downloaded yet, the indicator turns red and reads "Model inactive".
- **New Chat** — the main card for starting a new conversation.
- **Recent Chats** — a list of previous conversations, each titled with its first question. A counter shows the total. Each entry has an (×) button to delete that conversation individually.
- **Settings icon** (top right) — opens the configuration screen.

![Teleco SLM main screen](manual/manual-02-home.png)

*Figure 2. Teleco SLM main screen.*

### 5.2 Conversations

Tapping **New Chat**, or selecting an existing conversation, opens the chat screen. It works much like any messaging app:

- Type your question in the text field at the bottom and press the send button (blue arrow).
- The answer is generated progressively, token by token, in real time.
- Your messages appear on the right (blue bubble with a person icon) and the model's answers on the left (dark bubble with the model icon).
- Every conversation is saved automatically to the local SQLite database and can be reopened from the **Recent Chats** section on the main screen.

At the bottom of the chat screen there is a legal notice reminding you that answers may contain errors and do not replace consulting official academic sources.

### 5.3 LaTeX rendering

Teleco SLM renders mathematical expressions written in LaTeX directly inside the answers. The model has been trained to generate formulas using the standard delimiters: `\(...\)` for inline expressions and `\[...\]` for block expressions. Formulas render automatically, with no extra action required from you.

![Chat screen with a generated answer containing a LaTeX formula](manual/manual-03-chat-latex.png)

*Figure 3. Chat screen with a generated answer including a LaTeX formula.*

---

## 6. Settings

The Settings screen is organised into the following sections:

**Local Model** — Shows the configured model's information (name, quantisation format, approximate size and execution mode). From here you can download the model from Hugging Face or select a locally stored GGUF file.

**Remote Server** — Connects the application to a `llama-server` instance running on the local network. Enter the IP address and port, then press **Connect**.

**Performance** — Opens the Inference Metrics panel, covered in section 7.

**Data** — The **Delete all history** button removes every conversation stored in the local database. This action cannot be undone.

**About** — Shows the application version, a short description and the technologies used: llama.cpp, SQLite and Offline mode.

![Settings — Performance, Data and About](manual/manual-04-settings-data.png)

*Figure 4. Settings — Performance, Data and About.*

---

## 7. Inference metrics

The Inference Metrics panel lets you monitor the model's performance on each request. Open it from **Settings > Performance > Inference Metrics**.

The following metrics are recorded for every query:

| Metric | Description |
|--------|-------------|
| Tokens generated | Total number of tokens produced in the answer. |
| Time to first token | Latency (in milliseconds) from sending the request to the first generated token. |
| Total time | Total duration of the answer generation (in seconds). |
| Speed | Generation rate measured in tokens per second (tok/s). |
| Memory (RSS) | Percentage of physical RAM used by the inference process. |

![Inference Metrics panel with data from one query](manual/manual-05-metrics.png)

*Figure 5. Inference Metrics panel with data from a single query.*

Each entry in the metrics history includes the time of the request, the source (local or remote `llama-server`) and the text of the query. This is useful for diagnosing performance problems or comparing inference speed across devices.

---

## 8. Data management

All information generated by the application is stored exclusively on your device. Teleco SLM never sends data to external servers. The data handled is:

- **Conversations** — stored in a local SQLite database. Each conversation holds your messages and the model's answers with timestamps.
- **Preferences** — application configuration (model path, remote server address) stored via SharedPreferences.
- **Model** — the model's GGUF file is stored in the application directory.

### Deleting conversations

You can delete individual conversations from the main screen by pressing the (×) button next to each chat, or delete the entire history from **Settings > Data > Delete all history**.

> **Warning:** Deleting the history cannot be undone. Deleted conversations cannot be recovered.

---

## 9. Troubleshooting

**The "Model active" indicator does not appear**
The model has not been downloaded, or the file path is wrong. Open Settings and check that the GGUF file path is valid. If needed, press "Select .gguf file" to set the path again.

**The model download keeps stopping**
Check your internet connection and the free space on the device (~1.1 GB). Restart the download from **Settings > Download model**.

**Answers are very slow**
Inference speed depends on the device's hardware. On low-end Android devices, consider using Remote Server mode with `llama-server` running on a PC with more resources. Typical speeds: 8–15 tok/s on modern phones, 15–30 tok/s on mid-range PCs.

**The application closes unexpectedly**
This is usually a lack of RAM. Close other background applications and restart Teleco SLM. The model needs roughly 1.5 GB of free RAM.

**LaTeX formulas do not render correctly**
Check that the answer contains the correct delimiters. The model occasionally produces malformed output; rephrasing the question and asking explicitly for the formula usually fixes it.

**Cannot connect to the remote server**
Check that both devices are on the same local network, that the IP address and port are correct, and that `llama-server` is running on the target machine.

---

## 10. Technical information

| Component | Detail |
|-----------|--------|
| Framework | Flutter (Android + Windows) |
| Inference engine | llama.cpp (ARM64 NEON on Android, HTTP on Windows) |
| Model | Qwen 3 1.7B Fine-tuned (LoRA) |
| Model format | GGUF — Q4_K_M (~1.1 GB) |
| Maximum context | 2,048 tokens |
| Database | SQLite (local conversation storage) |
| Configuration | SharedPreferences |
| State management | Provider (Flutter) |
| Math rendering | gpt_markdown (LaTeX delimiters) |
| Thinking-mode filtering | State machine with `/no_think` auto-retry |
| GPU (Android) | Disabled (`gpu_layers = 0`, Adreno 612 compatibility) |
| Version | 1.0.0 |

---

*Teleco SLM v1.0.0 — Arturo Fierro Pardo · Universidad CEU San Pablo — June 2026*
