---
description: Acts as a Specialist in Computer Vision (CV) Security, covering mitigation
  of adversarial attacks (FGSM, PGD, Patch Attacks), image data poisoning, visual
  backdoors, sensor spoofing, deepfake detection, and alignment with the OWASP
  Machine Learning Security Top 10.
metadata:
  mitre:
  - T1068
  phase: exploitation
  tools:
  - robustness-kits
  - openCV
  - PyTorch
  type: defensive
name: ai-computer-vision-security
---
# AI Skill: Computer Vision Security Specialist

This skill guides the AI to act as a **Security Engineer in Computer Vision and Visual Deep Learning**. The goal is to guide the development, hardening, and auditing of convolutional neural network (CNN) models, Vision Transformers (ViTs), and image/video processing pipelines against adversarial attacks, real-world physical tampering, deepfakes, visual model poisoning, and infrastructure risks based on the **OWASP Machine Learning Security Top 10** and **OWASP MLSVS**.

---

## 🧭 OWASP Theoretical References and Frameworks & Literature

This skill consolidates guidelines and research drawn from the following sources:

- **OWASP Machine Learning Security Top 10 (ML Top 10)**: The OWASP reference standard for vulnerabilities in ML systems (ML01: Input Manipulation, ML02: Data Poisoning, ML03: Model Inversion, ML04: Membership Inference, ML05: Model Theft, ML06: AI Supply Chain).
- **OWASP MLSVS (Machine Learning Security Verification Standard)**: A security requirements verification standard for machine learning models, training data, and inference infrastructure.
- **Applied Computer Vision through Artificial Intelligence (Sandhu et al.)**: Visual feature extraction, image preprocessing, bio-inspired attribute selection algorithms, and hybrid architectures (DenseNet + LSTM) for secure classification.
- **Practical AI Security (Chris Harr)**: Adversarial perturbations in images ($L_\infty, L_2$), visual dataset poisoning, *feature squeezing*, bit-depth reduction, and spatial smoothing.
- **Red Teaming AI: Attacking & Defending Intelligent Systems (Philip A. Dursey)**: Adversarial attacks in the physical world (*Adversarial Patches*, LED lighting projection, stickers on signage), trojan injection (*BadNets*, *Neural Cleanse*), and certified robustness through *Randomized Smoothing*.
- **The Art of Cyber Defense (Youssef Baddi et al.)**: Behavioral analysis in visual IoT ecosystems, edge Docker container processing, and proactive detection of visual anomalies.
- **MITRE ATLAS**: Techniques specific to optical sensor manipulation and evasion of computer vision classifiers (T1565.001 - Image Poisoning, T1484 - Physical Perturbation).

---

## 📌 Full Mapping: OWASP Machine Learning Security Top 10 (Computer Vision)

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│              OWASP Machine Learning Security Top 10 (CV Pipeline)                 │
├───────────────────────────────────────┬───────────────────────────────────────────┤
│ Vulnerabilidade OWASP ML              │ Controles Arquiteturais e Mitigações      │
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ ML01: Input Manipulating Attacks      │ Adversarial Training (TRADES/PGD),        │
│ (FGSM, PGD, Patch Attacks)            │ VisionInputSanitizer, Feature Squeezing. │
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ ML02: Data Poisoning Attacks          │ Detecção de triggers por Neural Cleanse,  │
│ (Clean-Label & Trojan Backdoors)      │ análise de entropia STRIP, DBSCAN.        │
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ ML03: Model Inversion Attacks         │ Differential Privacy (DP-SGD) no treino,  │
│ (Reconstrução de faces a partir de V) │ difusão controlada de probabilidades.    │
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ ML04: Membership Inference Attacks    │ Regularização L2/Dropout no modelo,       │
│ (Identificação de imagens no dataset) │ mascaramento de vetores de confiança.     │
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ ML05: Model Theft / Extraction        │ Limitador de consultas (rate limiting),   │
│ (Treino de modelo espelho por API)    │ adição de ruído a log-probabilidades.     │
├───────────────────────────────────────┼───────────────────────────────────────────┤
│ ML06: AI Supply Chain Attacks         │ Carregamento exclusivo de `.safetensors`, │
│ (Modelos Pickle maliciosos de CV)     │ assinaturas Cosign para pesos pré-treinados│
└───────────────────────────────────────┴───────────────────────────────────────────┘
```

---

## 📐 Mathematical Formulation of Visual Adversarial Attacks (OWASP ML01)

### 1. Fast Gradient Sign Method (FGSM)

A single-step attack that computes the sign of the loss function gradient with respect to the input image:

$$x_{adv} = x + \epsilon \cdot \text{sign}\left(\nabla_x J(\theta, x, y)\right)$$

### 2. Projected Gradient Descent (PGD)

A multi-step iterative attack formulated as the projection of the gradient inside the perturbation ball $\mathcal{S} = \{x' : \|x' - x\|_\infty \le \epsilon\}$:

$$x^{t+1} = \Pi_{x + \mathcal{S}} \left( x^t + \alpha \cdot \text{sign}\left(\nabla_{x^t} J(\theta, x^t, y)\right) \right)$$

---

## 🛠️ Practical Engineering and Defense Guidelines in Computer Vision

### 1. Weight Supply Chain Security (OWASP ML06 & MLSVS)

- **Blocking Deserialization of Visual Models**:
  - Pre-trained visual models (YOLO, ResNet, ViT) distributed in `.pt` or `.pkl` format can execute arbitrary code through `pickle`.
  - Require conversion and loading strictly in **`safetensors`** or **ONNX**.

```python
import torch
import torch.nn as nn
import torchvision.transforms as T
from safetensors.torch import load_file

class VisionInputSanitizer(nn.Module):
    """Camada defensiva de sanitização de imagens contra ataques adversariais (OWASP ML01)."""
    def __init__(self, bit_depth: int = 4, blur_kernel_size: int = 3):
        super().__init__()
        self.bit_depth = bit_depth
        self.blur = T.GaussianBlur(kernel_size=blur_kernel_size, sigma=(0.1, 2.0))

    def quantize_bits(self, x: torch.Tensor) -> torch.Tensor:
        """Reduz a profundidade de bits dos pixels da imagem."""
        max_val = (2 ** self.bit_depth) - 1
        return torch.round(x * max_val) / max_val

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 1. Quantização de bits (destrói ruído adversarial de baixa intensidade)
        x_quantized = self.quantize_bits(x)
        # 2. Suavização gaussiana leve (elimina gradientes pontuais)
        x_sanitized = self.blur(x_quantized)
        return x_sanitized

def load_secure_vision_model(weights_path: str, model: nn.Module):
    """Carrega modelos visuais imunes a RCE em conformidade com OWASP ML06."""
    if not weights_path.endswith(".safetensors"):
        raise ValueError("ERRO DE SEGURANÇA: Apenas arquivos .safetensors são permitidos para evitar execução remota de código via Pickle.")
    state_dict = load_file(weights_path)
    model.load_state_dict(state_dict)
    return model
```

### 2. Defenses Against Adversarial Evasion Attacks (OWASP ML01)

- **Adversarial Training (Madry's min-max formulation)**:
  - Formulate the optimization process during training to mitigate the worst-case adversarial perturbation:
  $$\min_\theta \mathbb{E}_{(x,y)\sim D} \left[ \max_{\delta \in \mathcal{S}} J(\theta, x + \delta, y) \right]$$
- **Certified Robustness via Randomized Smoothing**:
  - To guarantee computationally that no perturbation of radius $R$ changes the image class, add Gaussian noise $\eta \sim \mathcal{N}(0, \sigma^2 I)$ and evaluate the probability of the majority vote under Monte Carlo.

### 3. Detection of Visual Trojans and Backdoors (OWASP ML02)

- **Neural Cleanse**:
  - For each model class, optimize a minimalist mask pattern that forces any image to be classified into that class. If the size of an optimized mask is statistically smaller than the others (measured by the median absolute deviation - MAD), a trojan is present in that class.
- **STRIP (Strong Intentional Perturbation)**:
  - Overlay test samples with random background images. If the entropy of the model's output probability distributions is abnormally low regardless of the mixed image, the input activated a persistent backdoor trigger.

### 4. Mitigation of Model Inversion and Face Extraction (OWASP ML03 & ML04)

- **Anonymization and Rounding of Confidence Vectors**:
  - Return only the predicted class label (`class_id`) in the public API instead of exposing the full output probability vector with high-precision floats, thwarting image reconstruction attacks (*Model Inversion*) and substitute training (*Model Theft*).

### 5. Facial Biometric Recognition & Deepfake Detection

- **Multispectral Liveness Detection & rPPG**:
  - **Remote Photoplethysmography (rPPG)**: Extract microscopic color variations in the facial skin caused by the cardiac pulse across sequences of video frames.
- **Content Credentials and Authenticity (C2PA Standard)**:
  - Sign optical sensor metadata using cryptographic keys in hardware (TPM/Secure Enclave) at the moment the photo/video is captured.

---

## 📝 Computer Vision Security Report Template

When auditing a computer vision pipeline or model:

```markdown
### 🖼️ Security Audit: [Computer Vision System / Component]

#### 🔍 Technical Specification
- **Model Architecture**: [e.g., ResNet-50 / YOLOv8 / ViT-Base / Hybrid DenseNet+LSTM]
- **Weight Format**: [safetensors / ONNX (Pickle Forbidden)]
- **Application**: [e.g., Facial Recognition / Autonomous Vehicle Obstacle Detection / Medical Analysis]
- **Deployment Mode**: [Edge IoT Device / Cloud GPU Server / Docker Container]

#### 🛡️ Vulnerability and Robustness Assessment (OWASP ML Top 10)

| Attack Vector | OWASP ML Assessment | Robustness Status | Hardening Recommendation |
| :--- | :--- | :--- | :--- |
| **PGD Adversarial Attack** | ML01: Input Manipulation | Vulnerable | Retrain the model with PGD adversarial training and bit-depth reduction. |
| **Malicious Weights RCE** | ML06: AI Supply Chain | Protected | Load models strictly in the `.safetensors` format. |
| **Trojan / Visual Backdoor** | ML02: Data Poisoning | Not Audited | Apply static inspection with Neural Cleanse and verification with STRIP. |
| **Model Inversion (Face Extraction)** | ML03: Model Inversion | Vulnerable | Hide floating-point probabilities from the public inference API. |
| **Deepfake Liveness Bypass** | ML01: Input Manipulation | Vulnerable | Implement rPPG extraction and C2PA signature validation in hardware. |
```

---

## 🔗 Integration with Other Skills in the Ecosystem

- To integrate Computer Vision pipelines into edge and IoT nodes securely, see [network-security-onprem-cloud](../../operations/network-security-onprem-cloud/SKILL.md).
- To align the use of facial biometric data with data protection laws (LGPD/GDPR), see [security-privacy](../../grc/security-privacy/SKILL.md).
- To implement real-time image/video inference in the backend, see [backend-developer](../../../roles/backend-developer/SKILL.md).
