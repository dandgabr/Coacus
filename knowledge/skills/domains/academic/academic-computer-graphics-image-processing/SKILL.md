---
name: academic-computer-graphics-image-processing
description: "Senior specialist in Computer Graphics, Computer Vision, Digital Image Processing, and Digital Compositing building on Mathematics for Computer Graphics (John Vince), Computer Vision Metrics (Scott Krig), Mastering Computer Vision with PyTorch 2.0 (M. Arshad Siddiqui), The Art and Science of Digital Compositing (Ron Brinkmann), Numerical Algorithms (Justin Solomon), and Digital Image Processing (Gonzalez, Woods). Covers 3D Geometric Transformations, Quaternions and SLERP, Projective Geometry, Parametric Curves and Surfaces (Bézier, B-Splines, NURBS), Illumination Models (Phong, PBR Cook-Torrance BRDF/BSSRDF), Ray Tracing, Feature Detector and Descriptor Taxonomy (SIFT, ORB, FAST, BRISK), Deep Learning with PyTorch 2.0 (YOLO, Mask R-CNN, UNet, ViT, TorchDynamo), Digital Compositing Algebra (Porter-Duff, Alpha Premultiplication, ACES/Linear Color Spaces), and Geometric Numerical Methods (Laplace-Beltrami, ICP, Physical Simulation)."
---

# Computer Graphics, Computer Vision, and Image Processing

This skill establishes the rigorous mathematical foundations, rendering algorithms, modern computer vision, digital visual effects compositing, and numerical processing of 2D/3D geometry.

---

## 📐 1. 3D Geometric Transformations and Projection Algebra

### 1.1 Homogeneous Coordinates and the Transformation Pipeline
In computer graphics, points in $\mathbb{R}^3$ are represented in homogeneous coordinates $\mathbf{p} = [x, y, z, 1]^T$ to unify affine operations (translation, rotation, scale, and shear) into $4 \times 4$ matrices:

$$\mathbf{v}_{clip} = \mathbf{M}_{proj} \cdot \mathbf{M}_{view} \cdot \mathbf{M}_{model} \cdot \mathbf{v}_{local}$$

- **Translation Matrix**:
  $$\mathbf{T}(t_x, t_y, t_z) = \begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

- **Rotation Matrix around an Arbitrary Axis $\mathbf{u} = [u_x, u_y, u_z]^T$ with $\|\mathbf{u}\|=1$ (Rodrigues' Formula)**:
  $$\mathbf{R}(\theta, \mathbf{u}) = \cos\theta \mathbf{I} + (1 - \cos\theta) \mathbf{u}\mathbf{u}^T + \sin\theta [\mathbf{u}]_\times$$
  where $[\mathbf{u}]_\times$ is the skew-symmetric matrix:
  $$[\mathbf{u}]_\times = \begin{bmatrix} 0 & -u_z & u_y \\ u_z & 0 & -u_x \\ -u_y & u_x & 0 \end{bmatrix}$$

### 1.2 Quaternions and Spherical Interpolation (SLERP)
To avoid Gimbal Lock and guarantee smooth rotational interpolation of 3D orientations:
- **Unit Quaternion**: $\mathbf{q} = s + x\mathbf{i} + y\mathbf{j} + z\mathbf{k} = [\cos(\theta/2), \mathbf{u}\sin(\theta/2)]$ where $\|\mathbf{q}\| = 1$.
- **Rotation of a Point**: $\mathbf{p}' = \mathbf{q} \mathbf{p} \mathbf{q}^{-1} = \mathbf{q} \mathbf{p} \mathbf{q}^*$.
- **SLERP (Spherical Linear Interpolation)**:
  $$\text{SLERP}(\mathbf{q}_1, \mathbf{q}_2; t) = \frac{\sin((1-t)\Omega)}{\sin\Omega} \mathbf{q}_1 + \frac{\sin(t\Omega)}{\sin\Omega} \mathbf{q}_2 \quad \text{where } \cos\Omega = \mathbf{q}_1 \cdot \mathbf{q}_2$$

### 1.3 Perspective and Orthographic Projection Matrices
- **Symmetric Perspective Projection (Frustum with $fov$, $aspect$, $z_{near}$, $z_{far}$)**:
  $$\mathbf{M}_{persp} = \begin{bmatrix} \frac{1}{\text{aspect} \cdot \tan(fov/2)} & 0 & 0 & 0 \\ 0 & \frac{1}{\tan(fov/2)} & 0 & 0 \\ 0 & 0 & -\frac{z_f + z_n}{z_f - z_n} & -\frac{2 z_f z_n}{z_f - z_n} \\ 0 & 0 & -1 & 0 \end{bmatrix}$$
- **Perspective Division**: Normalized Device Coordinate (NDC) normalization: $\mathbf{v}_{ndc} = [x_c/w_c, y_c/w_c, z_c/w_c]^T$.

---

## 〰️ 2. Parametric Curves and 3D Surfaces

### 2.1 Bézier Curves and the De Casteljau Algorithm
A Bézier curve of degree $n$ defined by $n+1$ control points $\mathbf{P}_0, \mathbf{P}_1, \dots, \mathbf{P}_n$:
$$\mathbf{C}(t) = \sum_{i=0}^n B_{i,n}(t) \mathbf{P}_i, \quad t \in [0, 1]$$
where $B_{i,n}(t) = \binom{n}{i} t^i (1-t)^{n-i}$ are the Bernstein polynomials.

- **Cubic Bézier ($n=3$)**:
  $$\mathbf{C}(t) = (1-t)^3 \mathbf{P}_0 + 3t(1-t)^2 \mathbf{P}_1 + 3t^2(1-t) \mathbf{P}_2 + t^3 \mathbf{P}_3$$
- **De Casteljau Algorithm**: Numerically stable recursive evaluation by successive linear interpolations $\mathbf{P}_i^{(k)}(t) = (1-t)\mathbf{P}_i^{(k-1)}(t) + t\mathbf{P}_{i+1}^{(k-1)}(t)$.

### 2.2 B-Splines and NURBS Surfaces
- **B-Splines**: Offer local control and arbitrary $C^k$ continuity using a knot vector $U = \{u_0, u_1, \dots, u_m\}$ with Cox-de Boor basis functions.
- **NURBS (Non-Uniform Rational B-Splines)**: Allow exact representation of conics (circles, ellipses, spheres) through control points weighted by weights $w_i$:
  $$\mathbf{S}(u, v) = \frac{\sum_{i=0}^n \sum_{j=0}^m N_{i,p}(u) N_{j,q}(v) w_{i,j} \mathbf{P}_{i,j}}{\sum_{i=0}^n \sum_{j=0}^m N_{i,p}(u) N_{j,q}(v) w_{i,j}}$$

---

## 💡 3. Illumination Models, Shading, and Rendering

### 3.1 Empirical vs Physically Based Illumination (PBR)
| Model | Fundamental Equation | Main Characteristics |
| :--- | :--- | :--- |
| **Classical Phong** | $I = k_a I_a + k_d I_d (\mathbf{L} \cdot \mathbf{N}) + k_s I_s (\mathbf{R} \cdot \mathbf{V})^n$ | Empirical, does not conserve energy, uses the ideal reflection vector $\mathbf{R}$. |
| **Blinn-Phong** | $I = k_a I_a + k_d I_d (\mathbf{L} \cdot \mathbf{N}) + k_s I_s (\mathbf{H} \cdot \mathbf{N})^n$ | More efficient, uses the half-way vector $\mathbf{H} = \frac{\mathbf{L} + \mathbf{V}}{\|\mathbf{L} + \mathbf{V}\|}$. |
| **PBR Cook-Torrance (Microfacet)** | $f_r(\mathbf{x}, \omega_i, \omega_o) = \frac{D(\mathbf{h}) F(\omega_i, \mathbf{h}) G(\omega_i, \omega_o, \mathbf{h})}{4 (\mathbf{n} \cdot \omega_i) (\mathbf{n} \cdot \omega_o)}$ | Physically plausible, energy-conserving, microfacet-based. |

- **Cook-Torrance BRDF Terms**:
  1. **Normal Distribution $D(\mathbf{h})$ (GGX / Trowbridge-Reitz)**:
     $$D_{GGX}(\mathbf{h}) = \frac{\alpha^2}{\pi \left( (\mathbf{n} \cdot \mathbf{h})^2 (\alpha^2 - 1) + 1 \right)^2}$$
  2. **Fresnel $F(\omega_i, \mathbf{h})$ (Schlick Approximation)**:
     $$F_{Schlick}(\theta) = F_0 + (1 - F_0) (1 - \cos\theta)^5$$
  3. **Geometry / Shadowing $G(\omega_i, \omega_o, \mathbf{h})$ (Smith GGX)**:
     $$G(\mathbf{n}, \mathbf{v}, \mathbf{l}) = G_1(\mathbf{n}, \mathbf{v}) G_1(\mathbf{n}, \mathbf{l}), \quad G_1(\mathbf{n}, \mathbf{v}) = \frac{2 (\mathbf{n} \cdot \mathbf{v})}{(\mathbf{n} \cdot \mathbf{v}) + \sqrt{\alpha^2 + (1-\alpha^2)(\mathbf{n} \cdot \mathbf{v})^2}}$$

### 3.2 Kajiya's Rendering Equation (Global Ray Tracing)
$$L_o(\mathbf{x}, \omega_o) = L_e(\mathbf{x}, \omega_o) + \int_{\Omega} f_r(\mathbf{x}, \omega_i, \omega_o) L_i(\mathbf{x}, \omega_i) (\mathbf{n} \cdot \omega_i) \, d\omega_i$$
- **Spatial Acceleration Algorithms**: BVH (Bounding Volume Hierarchy), Octrees, and KD-Trees with the Surface Area Heuristic (SAH).

---

## 🔍 4. Taxonomy of Computer Vision Metrics & Descriptors

### 4.1 Local Feature Detectors and Descriptors (Scott Krig Taxonomy)
```
Taxonomia de Features Visuais:
├── Detectores de Cantos & Bordas:
│   ├── Gradiente Espacial: Sobel, Prewitt, Scharr
│   ├── Autovalores de Autocorrelação: Harris Corner Detector, Shi-Tomasi (Good Features to Track)
│   └── Testes de Segmento Acelerados: FAST (Features from Accelerated Segment Test), AGAST
├── Descritores Baseados em Histograma de Gradiente:
│   ├── SIFT (Scale-Invariant Feature Transform) - DoG (Difference of Gaussians), 128-dim vetor
│   ├── SURF (Speeded-Up Robust Features) - Box Filters e Imagens Integrais, 64-dim vetor
│   └── HOG (Histogram of Oriented Gradients) - Detecção densa de pedestres/objetos
└── Descritores Binários (Baixo Custo / Mobile):
    ├── BRIEF (Binary Robust Independent Elementary Features)
    ├── ORB (Oriented FAST and Rotated BRIEF) - Rotação invariante e resistente a ruído
    ├── BRISK (Binary Robust Invariant Scalable Keypoints) - Padrão de amostragem circular
    └── FREAK (Fast Retina Keypoint) - Amostragem inspirada na retina humana
```

### 4.2 Similarity, Distance, and Image Quality Metrics
- **Hamming Distance for Binary Descriptors**:
  $$D_H(\mathbf{a}, \mathbf{b}) = \text{popcount}(\mathbf{a} \oplus \mathbf{b})$$
- **PSNR (Peak Signal-to-Noise Ratio)**:
  $$\text{PSNR} = 10 \log_{10} \left( \frac{\text{MAX}_I^2}{\text{MSE}} \right), \quad \text{MSE} = \frac{1}{MN} \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} [I(x,y) - K(x,y)]^2$$
- **SSIM (Structural Similarity Index Measure)**:
  $$\text{SSIM}(x, y) = \frac{(2\mu_x\mu_y + c_1)(2\sigma_{xy} + c_2)}{(\mu_x^2 + \mu_y^2 + c_1)(\sigma_x^2 + \sigma_y^2 + c_2)}$$

---

## 🤖 5. Modern Computer Vision with PyTorch 2.0

### 5.1 PyTorch 2.0 High-Performance Stack (`torch.compile`)
- **TorchDynamo**: Captures Python execution graphs without modifying the model code.
- **TorchInductor**: Compiler with high-performance C++/Triton code generation for NVIDIA GPUs.
- **AOTAutograd**: Ahead-of-time tracing of the backpropagation graph for operator fusion.

```python
import torch
import torchvision.models as models

# Modelo Vision Transformer compilado com PyTorch 2.0
model = models.vit_b_16(weights=models.ViT_B_16_Weights.DEFAULT).cuda()
model.eval()

# Otimização TorchDynamo + TorchInductor
compiled_model = torch.compile(model, mode="max-autotune")

with torch.inference_mode():
    dummy_input = torch.randn(1, 3, 224, 224, device="cuda")
    output = compiled_model(dummy_input)
```

### 5.2 State-of-the-Art Computer Vision Architectures
1. **Object Detection**:
   - **One-Stage**: YOLOv8 / YOLOv9 / RetinaNet (Focal Loss for class imbalance).
   - **Two-Stage**: Faster R-CNN with RPN (Region Proposal Network) and RoIAlign.
   - **Transformer-Based**: DETR (Detection Transformer) with bipartite matching via Hungarian Loss.
2. **Image Segmentation**:
   - **Semantic**: UNet, DeepLabV3+ (with Atrous Spatial Pyramid Pooling - ASPP).
   - **Instance / Panoptic**: Mask R-CNN, Segment Anything Model (SAM).
3. **Vision Transformers (ViT & Swin)**:
   - Splitting the image into non-overlapping patches ($16 \times 16$).
   - Multi-Head Self-Attention mechanism and hierarchical Patch Merging (Swin).

---

## 🎨 6. Digital Compositing Algebra & Visual Effects (Brinkmann)

### 6.1 Porter-Duff Compositing Operators
In professional digital compositing, manipulating images with an Alpha channel follows the Porter-Duff algebra:

| Operator | Color Equation ($C_o$) | Alpha Equation ($A_o$) | Technical Description |
| :--- | :--- | :--- | :--- |
| **$A \text{ OVER } B$** | $C_A + C_B(1 - A_A)$ | $A_A + A_B(1 - A_A)$ | A over B (standard layer compositing). |
| **$A \text{ IN } B$** | $C_A \cdot A_B$ | $A_A \cdot A_B$ | Region of A contained within B's alpha. |
| **$A \text{ OUT } B$** | $C_A(1 - A_B)$ | $A_A(1 - A_B)$ | Region of A that does not intersect B's alpha. |
| **$A \text{ ATOP } B$** | $C_A \cdot A_B + C_B(1 - A_A)$ | $A_B$ | A within B's alpha, with B in the remaining parts. |
| **$A \text{ XOR } B$** | $C_A(1 - A_B) + C_B(1 - A_A)$ | $A_A(1 - A_B) + A_B(1 - A_A)$ | A or B, excluding their intersection. |

### 6.2 Premultiplied Alpha vs Straight Alpha
- **Premultiplied (Pre-multiplied RGB)**: The color value is already multiplied by the Alpha channel: $R' = R \cdot A$, $G' = G \cdot A$, $B' = B \cdot A$.
  - *Critical Advantage*: Allows linear interpolations, convolution filters (blur, transformations), and compositing without dark edge artifacts (*fringing*).
- **Straight (Unassociated Alpha)**: RGB and Alpha are independent. It must be pre-multiplied before blending or filtering operations.

### 6.3 Linear Color Management and the ACES Standard
- Render and light-compositing processing **must always occur in linear space** ($I_{linear} = I_{sRGB}^\gamma$, with $\gamma \approx 2.2$).
- **ACES (Academy Color Encoding System)**: Industry standard for wide-gamut color management (ACEScg for CGI/VFX and ACEScc for color grading).

---

## 🧮 7. Numerical Methods for Geometry and Graphics (Solomon)

### 7.1 Laplace-Beltrami Operator on 3D Triangular Meshes
The Laplacian on discrete triangulated surfaces governs mesh smoothing, conformal parameterization, and spectral analysis of 3D shapes through the Cotangent Weights formula:

$$(\Delta_S f)_i = \frac{1}{2 A_i} \sum_{j \in N(i)} (\cot \alpha_{ij} + \cot \beta_{ij}) (f_i - f_j)$$

where $A_i$ is the Voronoi area around vertex $i$, and $\alpha_{ij}, \beta_{ij}$ are the angles opposite edge $(i, j)$.

### 7.2 3D Shape Alignment: ICP (Iterative Closest Point) Algorithm
Given a source point set $\mathcal{P} = \{\mathbf{p}_i\}$ and target set $\mathcal{Q} = \{\mathbf{q}_i\}$:
1. Find the closest point $\mathbf{q}_i \in \mathcal{Q}$ for each $\mathbf{p}_i \in \mathcal{P}$ using a KD-Tree.
2. Compute the centered cross-covariance matrix $\mathbf{H} = \sum_{i=1}^N (\mathbf{p}_i - \bar{\mathbf{p}})(\mathbf{q}_i - \bar{\mathbf{q}})^T$.
3. Factor via SVD: $\mathbf{H} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$.
4. Optimal rotation: $\mathbf{R} = \mathbf{V} \mathbf{U}^T$ (with correction $\det(\mathbf{R}) = 1$) and translation $\mathbf{t} = \bar{\mathbf{q}} - \mathbf{R} \bar{\mathbf{p}}$.
5. Update $\mathbf{p}_i \leftarrow \mathbf{R}\mathbf{p}_i + \mathbf{t}$ and repeat until convergence $\|\mathbf{e}\| < \epsilon$.

---

## 🖼️ 8. Reference Image-Processing Implementation with CImg (Tschumperlé, Tilmant, Barra)

The **CImg** library is a single-header, template, header-only C++ toolkit for practical image processing — the reference implementation layer that turns the algorithms above into runnable code.

### 8.1 Core API and conventions
- `#include "CImg.h"` then `using namespace cimg_library;`. Four classes (`CImg<T>`, `CImgList<T>`, `CImgDisplay`, `CImgException`); helper functions in `cimg`. `T` defaults to `float`, so `CImg<>` means `CImg<float>`. On Linux with display: `g++ -o prog prog.cpp -lX11 -lpthread`.
- An image is always **4D**: width × height × depth (slices) × spectrum (channels), coordinates from `(0,0)`. Load/save: `CImg<unsigned char> img("kingfisher.bmp"); img.save("out.png");`.
- **Loop macros** (`cimg_forX`, `cimg_forXY`, `cimg_forC`, `cimg_for3x3`, `cimg_forNxN`) give cache-friendly traversal and readable code.
- **`get_` vs non-`get`**: `get_f()` allocates and returns a new image; `f()` mutates in place and returns a reference — use the non-`get` form on temporaries to avoid copies and enable chaining:
```cpp
CImg<> lum = img.get_norm().blur(sigma).normalize(0, 255);
CImgList<> grad = lum.get_gradient("xy");
CImg<> normGrad = (grad[0].get_sqr() += grad[1].get_sqr()).sqrt();
```

### 8.2 Algorithm families implemented
- **Point operations, histograms, LUTs**: `exp`/`sqrt`/`get_pow`/`cut`/`mul`/`div`, `operator|=|&|^`, `equalize`, `get_histogram`, `map(LUT)`, and the bytecode evaluator `img.fill("(x*y)%255", true)`.
- **Morphology**: `get_erode`/`get_dilate`/`get_opening`/`get_closing` with a structuring element; the dual/alternating filters, Beucher and half gradients, and skeletonization via two-pass `cimg_for3x3`.
- **Filtering**: spatial (`get_convolve`, mean/Gaussian, median/order, adaptive σ, Nagao windows), **recursive IIR** (the **Deriche** filter — `deriche(img, alpha, order, boundary)` with constant cost independent of α; orders 0/1/2 for smoothing and derivatives), **frequency** (`get_FFT`, ideal/Gaussian low/high-pass, ringing), and **PDE diffusion** (linear isotropic = Gaussian; **Perona-Malik** anisotropic diffusion on 2D images and 2D+T video).
- **Feature extraction**: **Harris & Stephens** corners from the structure tensor (`R = det(M) − k·Tr(M)²`, `k ∈ [0.04, 0.15]`), **Shi-Tomasi** (`R = min(λ₁, λ₂)`); the **Hough transform** for lines and circles; texture via LBP, texture spectrum and Tamura coefficients for CBIR.
- **Segmentation**: implicit **active contours / level sets** (signed distance, curvature and advection), **Otsu** and Bernsen thresholding, **k-means** on local mean/variance features, and **SLIC super-pixels** (k-means in CIE L*a*b*).
- **Motion, multispectral, 3D**: dense optical flow (Horn-Schunck, Lucas-Kanade), phase correlation and Kalman tracking, PCA dimension reduction over multispectral channels, color spaces (RGB/HSV/YCbCr/L*a*b*), JPEG DCT/IDCT compression, tomographic reconstruction and RBF warping.

### 8.3 Parallelism and best practices
CImg is header-only: only the used template combinations are instantiated (lighter binaries, longer compilations) and third-party features (display, PNG/JPEG) are compile-time flags. Optional **OpenMP** parallelization (`-fopenmp`) applies to the data-parallel loops the macros expose. Best practices: minimize allocations (prefer non-`get` in-place methods), use in-place operators (`+=`), reuse temporaries, traverse with loop macros, and build cache-friendly pipelines.
