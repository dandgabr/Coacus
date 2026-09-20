---
description: Acts as a Specialist in Voice Processing, Speech (STT/ASR), and Voice
  Synthesis (TTS) Security, covering the HAVOC model for voice-controlled devices,
  inaudible ultrasonic attacks, voice deepfakes, voice biometrics defense, and
  alignment with OWASP ML Top 10 and OWASP API Security.
metadata:
  mitre:
  - T1203
  phase: exploitation
  tools:
  - librosa
  - praat
  type: defensive
name: ai-voice-stt-tts-security
---
# AI Skill: Voice, STT, and TTS Security Specialist

This skill guides the AI to act as a **Security Engineer in Speech Recognition (STT/ASR), Voice Synthesis (TTS), and Voice-Controllable Devices (VCDs)**. The goal is to provide protection guidelines, threat modeling, and mitigation of acoustic vulnerabilities, adversarial audio attacks, inaudible ultrasonic commands, laser injections into microphones, generative-AI voice cloning, and alignment with the **OWASP Machine Learning Security Top 10** and **OWASP API Security Top 10**.

---

## 🧭 OWASP Theoretical References and Frameworks & Literature

This skill consolidates architectures and methodologies from the following reference works:

- **OWASP Machine Learning Security Top 10 (ML Top 10)**: A standard for the security of audio/voice models (ML01: Audio Manipulation, ML02: Audio Poisoning, ML05: Voice Model Extraction, ML06: Audio Model Supply Chain).
- **OWASP API Security Top 10 (2023)**: Protection of the REST/gRPC and WebSocket APIs that feed STT/TTS engines (API4: Unrestricted Resource Consumption in audio streams, API7: SSRF via NLU intent parsing, API1: BOLA on recordings).
- **Hacking Voice-Controllable Devices (Sergio Esposito, Daniele Sgandurra et al.)**: The **HAVOC (Hacking Voice-Controllable Devices)** threat model, the 7-stage *kill chain* for voice assistants, exploitation of MEMS microphone non-linearity (*DolphinAttack*, *LightCommands*), and weaknesses in NLU/NLP processing.
- **Practical AI Security (Chris Harr)**: Adversarial perturbations in audio signals in the time and frequency domains, spectrogram perturbation, and robustness of acoustic classifiers.
- **Red Teaming AI: Attacking & Defending Intelligent Systems (Philip A. Dursey)**: Red teaming on voice interfaces, bypassing safety filters with masked audio, and attacks on biometric verifiers.
- **The Art of Cyber Defense (Youssef Baddi et al.)**: Voice traffic monitoring, security in audio-driven IoT ecosystems, and attack prevention on edge devices.
- **ASVspoof Protocols (Automatic Speaker Verification Spoofing Countermeasures)**: International standards for testing and mitigating spoofing attacks with synthetic, cloned, or replayed voice (*replay attacks*).

---

## 📌 Full Mapping: OWASP ML Top 10 & OWASP API Security (Voice & STT/TTS)

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                 OWASP Risk Matrix for Voice & STT/TTS Pipelines                   │
├───────────────────────────────────────┬───────────────────────────────────────────┤
│ Vulnerabilidade OWASP                 │ Controles Arquiteturais e Mitigações      │
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ OWASP ML01: Input Manipulation        │ AudioSignalSanitizer (passa-baixa 16kHz), │
│ (Ultrasonic, Laser, Audio CW Attacks) │ amortecedor acústico MEMS, compressão MP3.│
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ OWASP ML05: Voice Model Theft         │ Mascaramento de embeddings de voz,        │
│ (Extracao de biometria por API)       │ rate limiting e adição de ruído a scores. │
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ OWASP ML06: AI Supply Chain           │ Carregamento exclusivo de `.safetensors`  │
│ (Pesos maliciosos de ASR/TTS Pickle)  │ para modelos Whisper/Kaldi/Coqui TTS.     │
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ OWASP API4: Unrestricted Consumption  │ Limite de duração de stream de áudio,     │
│ (Flooding de GPU em ASR em tempo real)│ timeouts estritos e max_duration (máx 30s).│
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ OWASP API7: Server Side Request Forgery│ Sanitização estrita de URLs extraídas de  │
│ (SSRF via NLU Intent Parsing)         │ comandos de voz antes de requisições HTTP.│
└───────────────────────────────────────┴───────────────────────────────────────────┘
```

---

## 📌 The HAVOC Model: Kill Chain & VCD Access Matrix

Based on the research described in *Hacking Voice-Controllable Devices* (Esposito et al.), the **HAVOC** model divides the attack vector into 7 sequential stages and 3 accessibility profiles:

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌──────────────────┐
│ 1. Reconnais-   │ ──► │ 2. Initial       │ ──► │ 3. Triggering /   │ ──► │ 4. Command       │
│    sance        │     │    Foothold      │     │    Activation     │     │    Injection     │
└─────────────────┘     └──────────────────┘     └───────────────────┘     └──────────────────┘
                                                                                     │
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐               │
│ 7. Persistence/ │ ◄── │ 6. Action        │ ◄── │ 5. NLU Intent     │ ◄─────────────┘
│    Exfiltration │     │    Execution     │     │    Manipulation   │
└─────────────────┘     └──────────────────┘     └───────────────────┘
```

### Adversarial Access Profiles (`.access` State)

- **`.access == none`**: The attacker is neither physically near the device nor on its network.
- **`.access == temporary`**: The attacker has momentary physical access or access through unprotected speakers.
- **`.access == proximal`**: The attacker is physically close with line of sight (for example, aiming a laser diode from a window or positioning an ultrasonic transmitter).

---

## 🛠️ Practical Engineering and Defense Guidelines in Audio and Voice

### 1. Preventing Malicious Code in Audio Checkpoints (OWASP ML06)

- **Blocking STT/TTS Models in Pickle Format**:
  - Models such as Whisper, Coqui TTS, Kaldi, or SpeechBrain often use PyTorch `.pt` files containing `pickle`.
  - Require every ASR/TTS artifact to be converted and loaded strictly in the **`safetensors`** or **ONNX** format.

```python
import numpy as np
import scipy.signal as signal
from safetensors.torch import load_file
import torch

class AudioSignalSanitizer:
    """Sanitizador defensivo de sinal de áudio contra injeções ultrassônicas e ruído adversarial (OWASP ML01)."""
    def __init__(self, sample_rate: int = 44100, cutoff_freq: int = 16000):
        self.sample_rate = sample_rate
        self.cutoff_freq = cutoff_freq

    def apply_lowpass_filter(self, audio_data: np.ndarray) -> np.ndarray:
        """Aplica um filtro Butterworth passa-baixa digital para cortar ultrassom (>16kHz)."""
        nyquist = 0.5 * self.sample_rate
        normal_cutoff = self.cutoff_freq / nyquist
        b, a = signal.butter(6, normal_cutoff, btype='low', analog=False)
        sanitized_audio = signal.lfilter(b, a, audio_data)
        return sanitized_audio

    def sanitize(self, raw_pcm_audio: np.ndarray) -> np.ndarray:
        # 1. Eliminação de frequências ultrassônicas acima de 16kHz
        clean_audio = self.apply_lowpass_filter(raw_pcm_audio)
        # 2. Normalização de amplitude para prevenir picos de saturação
        max_val = np.max(np.abs(clean_audio))
        if max_val > 0:
            clean_audio = clean_audio / max_val
        return clean_audio

def load_secure_asr_model(weights_path: str, model: torch.nn.Module):
    """Carrega modelos ASR/TTS imunes a RCE em conformidade com OWASP ML06."""
    if not weights_path.endswith(".safetensors"):
        raise ValueError("ERRO DE SEGURANÇA: Apenas arquivos .safetensors são permitidos para evitar RCE via Pickle.")
    state_dict = load_file(weights_path)
    model.load_state_dict(state_dict)
    return model
```

### 2. Mitigation of Inaudible Ultrasonic and Laser Attacks (DolphinAttack & LightCommands)

- **DolphinAttack (Exploitation of MEMS Non-linearity)**:
  - Modulation of an ultrasonic carrier wave (>20 kHz). The physical non-linearity of the MEMS microphone demodulates the signal into the audible range recorded by the ASR.
  - **Mitigation**: Digital low-pass filters (`AudioSignalSanitizer`) and physical acoustic dampers in hardware.
- **LightCommands (Sound Injection via Modulated Laser)**:
  - Modulated intensity of a laser beam aimed at the MEMS microphone opening, generating an electrical signal equivalent to a voice command.
  - **Mitigation**: Install physical light baffles that block direct line of sight to the diaphragm.

### 3. Protection Against Voice Cloning and Vocal Deepfakes in TTS (ASV Anti-Spoofing)

- **Anti-Spoofing Classifiers (RawNet2 and AASIST Models)**:
  - Integrate deep audio neural networks trained on **ASVspoof** to identify spectral phase anomalies and vocoding artifacts from TTS synthesis.
- **Vocal Liveness Detection**:
  - **Doppler Shift Lip Movement (CaField)**: Validate lip and jaw movements through Doppler shift variation while occlusive consonants are pronounced.
  - **Dynamic Challenge-Response**: Ask the user to read randomized numeric sequences sent on screen at access time.

### 4. Protecting Audio APIs Against Excessive Consumption and SSRF (OWASP API4 & API7)

- **Protection Against Resource Exhaustion in STT (OWASP API4)**:
  - Limit audio transmissions to a maximum of 30 seconds per request and set strict *rate limits* per authenticated user token on the streaming WebSocket/gRPC.
- **Preventing SSRF via Intent Parsing (OWASP API7)**:
  - If the transcribed voice command includes URLs for search or navigation (for example, *"open page X"*), validate the URL against an *allowlist* and prevent the assistant from reaching internal loopback IP addresses (`127.0.0.1`, `169.254.169.254`).

---

## 📝 Voice Security Assessment Template (HAVOC Security Audit)

When assessing a voice assistant or STT/TTS system:

```markdown
### 🎙️ Voice Security Assessment: [Device / STT-TTS Application]

#### 🔍 Audio Interface Architecture
- **STT/ASR Engine**: [e.g., Whisper Large v3 / Kaldi / Vosk / Cloud Speech-to-Text]
- **Weight Format**: [safetensors / ONNX (Pickle Forbidden)]
- **TTS Engine**: [e.g., ElevenLabs / Coqui TTS / Custom Model]
- **Capture Sensor**: [MEMS Microphone Array / WebRTC Channel / IoT Device]

#### 🛡️ Acoustic and Logical Vulnerability Matrix (HAVOC & OWASP)

| ID | Threat Vector (HAVOC / OWASP) | Risk Level | Robustness Diagnosis | Mitigation Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **VCD-01** | Ultrasonic Injection (DolphinAttack / ML01) | High | Vulnerable (no physical frequency filter) | Apply `AudioSignalSanitizer` (16 kHz low-pass) and MEMS acoustic damper. |
| **VCD-02** | ASR/TTS Weights in Pickle (OWASP ML06) | Critical | Vulnerable to RCE on the server | Convert and load models strictly in the `.safetensors` format. |
| **VCD-03** | Voice Cloning via TTS (Spoofing / ML05) | Critical | Vulnerable if a static phrase is used | Integrate the AASIST/RawNet2 anti-spoofing model and dynamic authentication. |
| **VCD-04** | GPU Exhaustion from Audio Stream (API4) | High | No audio time limit | Enforce a strict 30 s recording limit per request and rate limiting at the gateway. |
| **VCD-05** | SSRF via Voice Command Injection (API7) | High | NLU parser reaches internal URLs | Validate and sanitize URLs extracted from voice, blocking access to metadata IPs (169.254.169.254). |
```

---

## 🔗 Integration with Other Skills in the Ecosystem

- To connect translated voice commands to secure backend API calls, see [backend-developer](../../../roles/backend-developer/SKILL.md) and [pentester-owasp-api-security-2023](../../appsec/pentester-owasp-api-security-2023/SKILL.md).
- To align the storage and processing of voice biometrics with privacy regulations, see [security-privacy](../../grc/security-privacy/SKILL.md).
- To model general threats in the ecosystem where the voice assistant is installed, see [threat-modeler](../../operations/threat-modeler/SKILL.md).
