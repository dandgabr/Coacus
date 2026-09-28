---
name: "applied-ai-automation"
description: "Provides expert patterns for applied AI programming and intelligent automation based on AI Programming with Python, AI with Python, AI for Big Data, the Python Beginner's Guide to AI, Learn Autonomous Programming with Python, and AI for Everyday IT. Covers the scikit-learn/Keras workflow, CNN/RNN/GAN architectures, reinforcement learning (Q-learning, SARSA, DQN), NLP and chatbot patterns, big-data AI pipelines with Spark/MLlib, RPA and hyperautomation, and applied GenAI in IT operations with function calling."
---

# AI Skill: Applied AI Programming and Intelligent Automation

This skill guides the AI to build practical AI features — from a baseline classifier to a reinforcement-learning agent to an IT automation copilot — and to prefer proven pipelines over novelty. It builds on *AI Programming with Python* (Xiao), *AI with Python* (Teoh & Rong), *AI for Big Data* (Deshpande & Kumar), *Python Beginner's Guide to AI* (Rothman et al.), *Learn Autonomous Programming with Python* (Divadkar), and *AI for Everyday IT* (LeMaire & Abshire).

Resolve current framework versions (TensorFlow/Keras, PyTorch, Spark, the `*rpa` libraries) from their publishers before pinning them.

---

## 🧭 When to Activate

- Building a first ML/DL model or a quick baseline comparison.
- Training image (CNN), sequence (RNN/LSTM) or generative (GAN) models.
- Implementing reinforcement learning for a routing/decision problem.
- Wiring NLP, chatbots, OCR or speech into an application.
- Automating IT/back-office work with RPA or a GenAI copilot.

---

## 🤖 The ML/DL Workflow

- Four learning categories: supervised, unsupervised, semi-supervised, reinforcement. Always `train_test_split`; report **train and test** error to expose over/underfit.
- **Estimator inventory:** SVM, Naive Bayes, LDA, decision tree, random forest, k-NN, MLP. Standardize with `StandardScaler().fit(X_train)`; inspect `confusion_matrix`, boxplots, outliers and feature importances, then iterate.
- **AutoML for baselines:** `PyCaret` (`setup`, `compare_models`) and `LazyPredict` fit dozens of models in one call.
- **Keras `Sequential`** is the canonical deep-learning template — `Dense`/`Conv2D`/`Flatten`/`Dropout`, `compile(optimizer='adam', loss='categorical_crossentropy')`, `fit`, `EarlyStopping`.
```python
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='relu'))
model.compile(loss='MSE', optimizer='Adamax', metrics=['accuracy'])
```
- **Transfer learning:** freeze a pretrained base (`MobileNetV2`, `ResNet50`, `EfficientNet`, `include_top=False`), add a head, feed data with `ImageDataGenerator().flow_from_directory`.
- **Architecture map:** LeNet, AlexNet, VGG, ResNet, DenseNet, MobileNet, EfficientNet, YOLO, U-Net, AutoEncoder, Siamese, Capsule; RNN/LSTM; transformers (BERT, GPT); GNNs; GANs (DCGAN, CycleGAN, StyleGAN, Pix2Pix).

---

## 🧭 NLP, Chatbots and Voice

`NLTK`, `spaCy`, `Gensim`, `TextBlob`: tokenization, POS, NER, summarization (TextRank/`summarize`), sentiment, translation, TTS (`pyttsx3`), STT (`SpeechRecognition`), OCR (`pytesseract`). Rule/retrieval chatbots via `ChatterBot` (`ChatterBotCorpusTrainer`); seq2seq LSTM chatbots with the Keras Functional API. For grounded generation, prefer the RAG patterns in [ai-application-engineering](../ai-application-engineering/SKILL.md).

---

## 🎮 Reinforcement Learning

Model the problem as an **MDP** (states, actions, rewards, transitions; the Markov property makes it memoryless). Tabular **Q-learning** update:

```text
new_value = (1 − α)·Q[s,a] + α·(reward + γ·max(Q[next_state]))
```

- Explore with ε-greedy; the canonical demo is a reward matrix over a routing graph or `gym.make("Taxi-v3")` (`α≈0.7`, `γ≈0.2`, `ε≈0.4`, tens of thousands of episodes).
- **SARSA** is on-policy; **Q-learning** is off-policy (max over next actions); **DQN** adds function approximation. Environments: OpenAI Gym, DeepMind Lab, Project Malmo.

---

## 🏭 Big-Data AI

- **Batch:** Hadoop HDFS (data-compute locality, intermediate disk I/O), MapReduce, Pig, Hive. **Real-time:** Spark (in-memory, RDDs), Storm/Flink (unbounded streams, native iteration).
- **Spark architecture:** driver (`SparkContext`/`SparkSession`, DAG) → executors; the driver is a single point of failure. **ML API** is transformer/estimator/Pipeline; persist models with `model.save(...)` then `PipelineModel.load(...).transform(...)`.
- **Distributed deep learning:** DeepLearning4j + Spark with `ParameterAveragingTrainingMaster` (data-parallel sharding + iterative averaging). NLP on big data: stop-words, stemming, n-grams, `CountVectorizer`, `HashingTF`+`IDF`, Word2Vec.
- **Streaming:** Spark Streaming `DStream`s (Kafka/Flume) with exactly-once semantics against reliable sources.

---

## 🤖 RPA and Hyperautomation

- **RPA platforms:** UiPath, Automation Anywhere, BluePrism; the Python `rpa` package for `init/url/type/click`.
- **Automation libraries:** `requests`+`beautifulsoup4` (scraping), `openpyxl`/`xlsxWriter` (Excel), `smtplib` (email), `PyPDF2`, `PIL`/`OpenCV`/`pytesseract`, `os`/`shutil`, `PyAutoGUI`/`PyWinAuto` (GUI control).
- **Orchestration** ("automation of automations") with `luigi` and `prefect`; **hyperautomation** = RPA + ML + AI (OCR document understanding + conversational agents). Test with Selenium, PyTest, Robot Framework.

---

## 🖥️ Applied GenAI for IT Operations

- **Prompting:** zero/single/few/many-shot; clarity, conciseness, relevance, specificity; recursive prompts, context injection, explicit constraints, prompt chaining, templating, meta-prompts. Watch hallucination, token-limit degradation and context exhaustion.
- **Function calling is the integration primitive:** define JSON-schema functions; the model returns JSON naming the function and arguments but **does not execute** them — your app validates and runs them. Keep `system`/`user`/`assistant` roles distinct; inject schema in `system`.
- **Security:** always use **read-only DB accounts**; AI validation is not the sole safeguard. Validate generated SQL with a separate `examine_sql` step before execution.
- **GenAIOps** lifecycle differs from MLOps/LLMOps; code assistants (Copilot, Cursor, Cline, Aider) require privacy review, tests before implementation, small chunks, and verification of every output.

---

## ⚠️ Pitfalls

- Overfitting (watch the train/test MSE gap), class imbalance, outliers.
- Hallucinated table/column names; short context in LLM sessions.
- Executing AI-authored commands without human verification.
- Treating RL as supervised — rewards are sparse and exploration is required.

---

## 🔗 Integration with Other Skills

- For the data-science workflow and cloud MLOps, see [data-science-workflow](../../../data/data-science-workflow/SKILL.md).
- For RAG, agents and production LLM systems, see [ai-application-engineering](../ai-application-engineering/SKILL.md).
- For scaling, see [distributed-ml-scaling](../../../data/distributed-ml-scaling/SKILL.md).
- For the security model of AI-assisted automation, see [ai-agentic-security](../../../security/ai/ai-agentic-security/SKILL.md).
