---
name: "computer-vision-deep-learning"
description: "Provides expert patterns for classical and deep-learning computer vision with Python based on Hands-On Image Processing and Computer Vision with Python (Dey), Computer Vision Metrics (Krig), and Mastering Computer Vision with PyTorch 2.0 (Siddiqui). Covers OpenCV/scikit-image fundamentals, color spaces and masks, edge/morphology/segmentation, the descriptor taxonomy (SIFT/ORB/BRISK), CNNs and transfer learning, detection (YOLO) and segmentation (U-Net/Mask R-CNN), torch.compile/TorchDynamo, and deployment."
---

# AI Skill: Computer Vision and Deep Learning

This skill guides the AI to solve image problems with the right tool at the right level — classical filtering when it suffices, deep learning when it does not — and to measure segmentation/detection quality with the correct metric. It builds on *Hands-On Image Processing and Computer Vision with Python* (Dey), *Computer Vision Metrics* (Krig), and *Mastering Computer Vision with PyTorch 2.0* (Siddiqui).

Resolve current versions of OpenCV, scikit-image, PyTorch and torchvision from their publishers before pinning them.

---

## 🧭 When to Activate

- Preprocessing images (color spaces, filtering, morphology, edges).
- Segmenting or detecting objects, and choosing a model family.
- Applying transfer learning or fine-tuning a CNN/ViT.
- Optimizing a PyTorch training/inference pipeline.
- Selecting the right evaluation metric (IoU, Dice, mAP).

---

## 🖼️ Classical Image Processing

Libraries by use: **Pillow/PIL** (I/O, resize, legibility), **OpenCV** (`cv2`; speed, video, `cv2.remap`), **scikit-image** (filters, segmentation, features), **SciPy** (`ndimage`, `fft`), **Matplotlib** (display).

- **Color spaces:** `cv2.cvtColor` (`BGR2HSV`, `BGR2LAB`, `BGR2YCrCb`). Fuse multiple space masks and **open** to remove speckle before a `bitwise_and` union:
```python
HSV_mask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), (0, 15, 0), (17, 170, 255))
HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
global_mask = cv2.bitwise_and(YCrCb_mask, HSV_mask)
```
- **Sampling/Fourier:** Nyquist–Shannon, anti-aliased downsampling; `numpy.fft`/`scipy.fft`; Butterworth via `skimage.filters`. **Transposed convolution ≠ upsampling** (a common misconception).
- **Edges/derivatives:** Sobel/Scharr/Prewitt → Laplacian → LoG/DoG → Canny. **A gradient kernel must sum to zero.**
- **Morphology:** `cv2.morphologyEx` (`MORPH_OPEN`/`MORPH_CLOSE`), distance transforms, watershed.
- **Segmentation ladder:** Otsu/multi-Otsu → watershed → SLIC/MaskSLIC superpixels → Chan–Vese active contours → GrabCut → CRF, then DL: FCN/DeepLabV3, Mask R-CNN, `YOLOv8`, and transformers (SETR, DPT, DETR, SegFormer, Mask2Former).
- **Foundation segmentation:** SAM, CLIPSeg (text-to-mask), monocular depth (DPT).

---

## 🧭 Descriptor Taxonomy (Krig)

Four descriptor families, matched to a distance metric:

1. **Local binary** (LBP, FREAK, ORB, BRISK, Census) — bit comparisons, **Hamming** distance.
2. **Spectra** (SIFT, SURF, GLOH, RIFF) — local gradients/region averages.
3. **Basis-space** (FFT, wavelets, HAAR, Zernike, KLT, steerable filters) — transformed coefficients.
4. **Polygon/shape** (area, perimeter, centroid, **Hu invariant moments**).

A 3-axis taxonomy (*shape/pattern* × *density* × *spectra*) organizes them; it is fuzzy by design and not a performance ranking. Detectors (Harris, FAST, Hessian, SUSAN) are distinct from descriptors (SIFT, BRISK, FREAK). Integral images make HAAR-style features cheap (four array references). Distance metrics: Euclidean/Manhattan, χ²/Mahalanobis, Hamming.

---

## 🔥 Deep Learning with PyTorch 2.0

**`torch.compile`** decomposes into **TorchDynamo** (graph capture via frame-evaluation hooks), **AOTAutograd** (ahead-of-time backward), **PrimTorch** (operator canonicalization) and **TorchInductor** (codegen). It is not free — keep a fallback and benchmark.

```python
compiled = torch.compile(model)
```

- Autograd: `requires_grad=True`, `.backward()` (scalars; non-scalars need `.sum().backward()`), `.detach()`, `torch.no_grad()` for inference; `torch.jit.trace`/`@torch.jit.script` for deployment.
- CNN blocks: `nn.Conv2d`, `nn.MaxPool2d`, `nn.BatchNorm2d`, `nn.Dropout`, `nn.Linear`.
- **Transfer learning:** replace the head, then optionally freeze the backbone. Prefer `weights="IMAGENET1K_V2"` over the legacy `pretrained=True`; standard ImageNet normalization `mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]`.
```python
from torchvision.models import resnet50
model = resnet50(weights="IMAGENET1K_V2")
model.fc = nn.Linear(model.fc.in_features, num_classes)
```
- **Detection:** `fasterrcnn_resnet50_fpn` (two-stage), `ssd300_vgg16`, YOLOv5 via `torch.hub`.
- **Training craft:** dropout + batch norm, LR schedules, early stopping, ensembles; **PyTorch Lightning** (`LightningModule`, `pl.Trainer`) removes boilerplate and handles multi-GPU/distributed.
- **Deployment:** TorchServe for REST; quantization (dynamic/static/QAT) and pruning for efficiency.

---

## 📏 Evaluation Metrics

- **Segmentation:** IoU, Dice (and Dice loss), pixel accuracy, mean pixel accuracy.
- **Detection:** precision/recall → Average Precision → **COCO-style mAP**; VOC for PASCAL.
- **Classification:** accuracy, confusion matrix, ROC-AUC; t-SNE embeddings and Gradio dashboards for qualitative review.

---

## ⚠️ Pitfalls

- Preprocessing is pipeline-specific — one recipe does not fit LBP, SIFT and CNNs alike.
- Verify morphological results on binary masks before logic unions; speckle ruins contours.
- Benchmark `torch.compile`; it fails on a minority of models.
- Re-initialize the classifier head before fine-tuning; mismatched normalization silently degrades accuracy.
- Choose the metric before training (imbalanced segmentation rewards IoU/Dice over pixel accuracy).

---

## 🔗 Integration with Other Skills

- For image-processing GPU kernels, see [gpu-programming-cuda](../../../languages/gpu-programming-cuda/SKILL.md).
- For the numerical methods behind graphics/CV, see [academic-computer-graphics-image-processing](../../academic/academic-computer-graphics-image-processing/SKILL.md).
- For adversarial attacks on vision, see [ai-computer-vision-security](../../../security/ai/ai-computer-vision-security/SKILL.md).
- For deep-learning engineering, see [ai-application-engineering](../ai-application-engineering/SKILL.md).
