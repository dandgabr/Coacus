---
name: "framework-qt6"
description: "Provides engineering patterns for desktop and mobile applications with the Qt 6 framework based on the Qt 6 C++ GUI Programming Cookbook (Lee Zhi Eng). Covers the Qt Widgets vs Qt Quick/QML dual track, signals and slots with pointer-to-member syntax, properties and stylesheets, animations and state machines, 2D/3D graphics and OpenGL, networking and file/database access, threading with QThread/QRunnable, QtWebEngine and C++/JavaScript bridging, and Qt 5 to Qt 6 migration."
---

# AI Skill: Qt 6 Application Engineering

This skill guides the AI to build cross-platform GUI applications with Qt 6, choosing deliberately between the **Qt Widgets** (mature, desktop) and **Qt Quick/QML** (declarative, touch/mobile) tracks. It builds on the *Qt 6 C++ GUI Programming Cookbook* (Lee Zhi Eng).

Resolve the current Qt 6 release, supported compilers and QML versions from the Qt project before pinning them.

---

## 🧭 When to Activate

- Building a desktop or mobile GUI in C++.
- Choosing between Qt Widgets and Qt Quick/QML.
- Wiring signals/slots, models/views, or C++/QML integration.
- Adding animations, threading, networking, or SQL to a Qt app.
- Migrating a project from Qt 5 to Qt 6.

---

## 🎨 Look-and-Feel and the Widget/QML Tracks

- **Qt Widgets**: `QWidget`-based, mature, best for form/desktop applications. Style with **Qt Designer** and **stylesheet** resources; customize **properties and sub-controls**; `Q_PROPERTY` for exposed state.
- **Qt Quick/QML**: declarative, best for touch/mobile and fluid UI. Style in QML; expose a C++ object to QML or register a type with `qmlRegisterType<MyLabel>("MyLabelLib", 1, 0, "MyLabel")`. **Qt Design Studio** separates design from code.
- Choose the track by target (touch vs desktop) and by team skill, not by novelty.

---

## 🔗 Signals and Slots

The `Q_OBJECT` macro enables the meta-object system. Prefer the modern **pointer-to-member** connect syntax over string-based connects:

```cpp
connect(this, &MainWindow::doNow, myclass, &MyClass::doSomething);
```

Lambda slots and callbacks are supported. Signals/slots are the primary decoupling mechanism — use them instead of tight coupling between widgets.

---

## 🎞️ States and Animations

- `QPropertyAnimation` animates a property on an object (`new QPropertyAnimation(ui->pushButton, "geometry")`), with **easing curves**, animation groups and nested groups.
- Qt 6 **state machine** (`QStateMachine`) for complex behavior; QML states/transitions/animations, animators and sprite animation for the declarative track.

---

## 🖌️ Graphics, OpenGL and 3D

- 2D with `QPainter` (drawing, coordinate transforms, SVG export, image effects); a 2D canvas in QML.
- OpenGL: context setup, 2D/3D shapes, texturing, lighting, keyboard-controlled movement; **Qt Quick 3D** for QML-driven 3D.

---

## 🌐 Networking, Data and WebEngine

- **Networking:** TCP server/client; FTP up/download via `QNetworkAccessManager`, `QNetworkRequest`, `QNetworkReply` (`readyRead`, `downloadProgress`, `finished`).
- **Files/Database:** JSON parse/serialize; **SQL driver** connection, queries, a login screen, and SQL-backed **model/view** lists; advanced queries.
- **QtWebEngine:** embed web content, configure settings, embed maps, and call between **C++ and JavaScript in both directions**.

---

## 🧵 Threading

- `QThread` with a `QObject` worker moved to the thread (the recommended pattern), protecting shared data; **`QRunnable`** processes for pool-based tasks.
- Never touch GUI objects from a non-GUI thread; signal back to the GUI thread.

---

## 🔄 Qt 5 → Qt 6 Migration

Changed C++ classes and QML types; use **Clazy** (a Clang-based static checker) to find migration issues; review the Qt 6 porting guides for removed/deprecated APIs.

---

## ⚡ Performance

- Optimize forms and C++ hot paths; profile and optimize **QML** rendering (binding loops, overdraw, excessive property changes).
- Keep the GUI thread free; move heavy work to worker threads and communicate via signals.

---

## ⚠️ Pitfalls

- Calling widget/QML methods from a worker thread.
- Heavy or blocking work on the GUI thread (freezes).
- String-based signal/slot connects (no compile-time checking).
- Excessive QML bindings causing re-evaluation storms.
- Ignoring the Widgets-vs-QML choice and mixing tracks without cause.

---

## 🔗 Integration with Other Skills

- For the host language, see [lang-cpp](../../languages/lang-cpp/SKILL.md) and [cpp-template-metaprogramming](../../languages/cpp-template-metaprogramming/SKILL.md).
- For concurrency primitives, see [functional-concurrent-programming](../../engineering/practices/functional-concurrent-programming/SKILL.md).
- For desktop UI principles, see [ui-ux-principles](../../engineering/practices/ui-ux-principles/SKILL.md).
- For data access, see [db-postgresql](../../data/db-postgresql/SKILL.md) and [db-sqlite](../../data/db-sqlite/SKILL.md).
