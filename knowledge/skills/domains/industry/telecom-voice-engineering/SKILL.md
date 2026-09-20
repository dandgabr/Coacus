---
name: "telecom-voice-engineering"
description: "Provides architecture, engineering, and security standards in telephony and voice networks. Covers VoIP protocols (SIP, SDP, RTP, SRTP), Session Border Controllers (SBC), legacy networks (PSTN, E1/T1, ISDN, SS7), WebRTC, audio codecs (G.711, G.729, Opus), Softswitches (Kamailio, OpenSIPS, FreeSWITCH, Asterisk), QoS (DSCP EF), STIR/SHAKEN, and telephony fraud prevention."
---

# AI Skill: Voice and Telephony Engineering (Telecom & Voice Specialist)

This skill guides the artificial intelligence to act as a **Voice Engineering, Telephony, and Real-Time Communications Specialist**, spanning legacy switched telephone networks (**PSTN**) to advanced **VoIP (Voice over IP)** architectures, **SBC (Session Border Controllers)**, **WebRTC**, and telecommunications security.

---

## 🧭 Telephony Network Architecture and Voice Protocols

### 1. VoIP Signaling and Transport
- **SIP (Session Initiation Protocol - RFC 3261)**:
  - Fundamental methods: `INVITE`, `ACK`, `BYE`, `CANCEL`, `REGISTER`, `OPTIONS`, `INFO`, `SUBSCRIBE`, `NOTIFY`.
  - Response Codes: `1xx` (Informational - 180 Ringing, 183 Session Progress), `2xx` (Success - 200 OK), `3xx` (Redirection), `4xx` (Client Error - 404 Not Found, 486 Busy, 488 Not Acceptable), `5xx` (Server Error), `6xx` (Global Failure).
  - **SDP (Session Description Protocol - RFC 4566)**: Negotiation of media, IP addresses, UDP ports, and supported codecs during the SIP handshake.
- **RTP / RTCP / SRTP**:
  - **RTP (Real-time Transport Protocol - RFC 3550)**: Transport of voice packets over UDP.
  - **RTCP (RTP Control Protocol)**: Monitoring of transmission quality metrics (jitter, packet loss, RTT).
  - **SRTP (Secure Real-time Transport Protocol - RFC 3711)**: Media encryption via AES-128/256 negotiated by SDES or DTLS-SRTP.

### 2. Traditional Telephony and PSTN Interconnection
- **PSTN (Public Switched Telephone Network) & TDM**:
  - E1 trunks (30 channels at 64kbps / 2.048 Mbps) and T1 (24 channels / 1.544 Mbps) using **ISDN PRI** (Q.931) or CAS (R2/Digital) signaling.
  - **SS7 (Signaling System No. 7)**: Out-of-band signaling protocol between public network telephone exchanges (ISUP, TCAP, MAP).
  - Analog interfaces: **FXS** (provides dial tone and ring voltage) and **FXO** (connects to the carrier's telephone line).

---

## 🛠️ Session Border Controllers (SBC) & SIP Proxies

The **SBC** acts as the security, routing, and normalization boundary between internal VoIP networks, carriers (SIP Trunks), and the internet:

### 1. Essential Functions of an SBC
- **B2BUA (Back-to-Back User Agent)**: Total separation of sessions between the *ingress* and *egress* legs, hiding the internal network topology (*Topology Hiding*).
- **NAT Traversal**: Resolution of private/public IP addresses in SIP packets and RTP flows using *Media Anchoring* algorithms, STUN, TURN, and ICE.
- **HMR / HPL (Header Manipulation Rules)**: Dynamic rewriting and sanitization of SIP headers (`From`, `To`, `Contact`, `P-Asserted-Identity`, `Diversion`).
- **Call Admission Control (CAC)**: Rate limiting of calls per second (CPS) and simultaneous calls for overload prevention and SIP DoS/DDoS attack mitigation.

### 2. Market Technologies
- **Carrier / Enterprise SBCs**: Oracle Acme Packet, Ribbon (Sonus), AudioCodes Mediant.
- **Open-Source Softswitches and SIP Proxies**:
  - **Kamailio / OpenSIPS**: Ultra-high-performance SIP proxies for routing millions of calls, load balancing, and static/dynamic registrars.
  - **FreeSWITCH / Asterisk**: B2BUA media servers, IVR, call recording, and transcoding.

---

## 🔊 Audio Codecs, QoS, and WebRTC

### 1. Codec Selection and Comparison
| Codec | Bitrate | Band Type | Typical Use |
| :--- | :--- | :--- | :--- |
| **G.711 (PCMU / PCMA)** | 64 kbps | Narrowband (8 kHz) | Traditional PSTN/VoIP standard with no compression loss. |
| **G.729a/b** | 8 kbps | Narrowband (8 kHz) | High compression (CS-ACELP) for low-bandwidth trunks. |
| **Opus** | 6 to 510 kbps (dynamic) | Fullband / Superwideband (48 kHz) | WebRTC gold standard; dynamic adaptation to network fluctuation. |
| **AMR-WB (G.722.2)** | 6.6 to 23.85 kbps | Wideband (16 kHz) | HD Voice standard in mobile networks (VoLTE / VoNR). |

### 2. Quality of Service (QoS) and Metrics
- **DiffServ Marking (DSCP)**:
  - RTP Media Packets: Mandatory **DSCP EF (Expedited Forwarding - 46 / 0xb8)** marking.
  - SIP Signaling Packets: **DSCP AF31 (26)** or **CS3 (24)** marking.
- **Target Production Metrics**:
  - **Latency (One-Way)**: < 150 ms (RTT < 300 ms).
  - **Jitter**: < 30 ms.
  - **Packet Loss**: < 1%.
  - **MOS (Mean Opinion Score)**: > 4.0 on a scale of 1 to 5.

### 3. WebRTC and Web Telephony
- Signaling over encrypted WebSockets (`wss://`).
- DTLS-SRTP negotiation for mandatory media encryption with no cleartext keys in SDP.
- Codec requirements: Mandatory support for Opus and G.711.

---

## 🔒 Voice Security, STIR/SHAKEN, and Fraud Mitigation

### 1. Hardening and Protection of VoIP Infrastructure
- **SIPS (SIP over TLS)**: Encryption of SIP signaling on port `5061` with mTLS validation of carrier certificates.
- **Toll Fraud Prevention**:
  - Strict restriction of dial plans to high-cost international destinations.
  - Mandatory authentication for all internally originated `INVITE` requests.
  - Immediate blocking of passwordless `REGISTER` scanning (tools such as SIPP, Friendly-Scanner, Svwar).

### 2. Call Authentication with STIR/SHAKEN
- **STIR (Secure Telephony Identity Revisited - RFC 8224)**: X.509 cryptographic signature in the SIP `Identity` header to attest the authenticity of the originating number (*Caller ID*).
- **SHAKEN (Signature-based Handling of Asserted information using tokens)**: Operational framework for carriers to assign attestation levels (A, B, C) to eliminate number spoofing (*Caller ID Spoofing*).

---

## 🔗 Integration with Other Skills

- For voice security in voice-assistant devices, STT/TTS, and IVR, consult [ai-voice-stt-tts-security](../../../security/ai/ai-voice-stt-tts-security/SKILL.md).
- For developing call-control APIs (Twilio, Asterisk AGI/ARI, FreeSWITCH ESL), consult [backend-developer](../../../roles/backend-developer/SKILL.md) and [lang-python](../../../languages/lang-python/SKILL.md).
- For on-premises and cloud network security (firewalls, voice microsegmentation), consult [network-security-onprem-cloud](../../../security/operations/network-security-onprem-cloud/SKILL.md) and [auth-protocols-mfa](../../../security/operations/auth-protocols-mfa/SKILL.md).
