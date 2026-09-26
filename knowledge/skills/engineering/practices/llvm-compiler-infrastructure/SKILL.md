---
name: "llvm-compiler-infrastructure"
description: "Provides expert patterns in LLVM-based compiler and toolchain engineering based on Learn LLVM 17 and LLVM Code Generation, covering project build and libraries, LLVM IR and SSA, frontend construction with IRBuilder, the pass manager and custom passes, TableGen target description, instruction selection (SelectionDAG and GlobalISel), legalization, register allocation and scheduling, the MC layer and object emission, the ORC JIT, and the opt/llc/lit/FileCheck debugging workflow."
---

# AI Skill: LLVM Compiler and Toolchain Engineering

This skill guides the AI to act as a specialist in **LLVM-based compiler and toolchain engineering**, building on *Learn LLVM 17* (Nacke & Kwan) and *LLVM Code Generation* (Colombet). It spans the full path source → AST → IR → optimized IR → SelectionDAG/GlobalISel → Machine IR → MC → object, plus JIT and the test/debug loop.

Resolve the current LLVM release and C++ standard requirement from the LLVM project before pinning a version; the architecture below is stable across recent releases.

---

## 🧭 When to Activate

- Building a new language frontend, a JIT, or a clang tool/plugin.
- Writing an LLVM pass (analysis or transform) or wiring a pass pipeline.
- Adding or debugging a target backend: TableGen descriptions, instruction selection, calling conventions, frame lowering, register allocation.
- Diagnosing codegen: `opt`/`llc` output, `.mir` files, machine verifier failures.
- Designing IR-level optimizations and understanding legalization/profitability.

---

## 🏗️ Project, Build and IR

LLVM is a mono-repo: each project (`llvm/`, `clang/`, `lld/`, `mlir/`, …) sits alongside `llvm/`. Core IR is `LLVMCore` (`include/llvm/IR`, `lib/IR`); backend infrastructure in `lib/CodeGen`; target code in `lib/Target/<Target>`.

```bash
cmake -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_PROJECTS=clang -B build -S llvm
cmake --build build -j2
ninja check-all
```

Useful knobs: `LLVM_TARGETS_TO_BUILD`, `LLVM_ENABLE_ASSERTIONS` (keep ON in Release to use `-debug-only`), `LLVM_OPTIMIZED_TABLEGEN`, `LLVM_USE_SPLIT_DWARF`. Downstream projects use `find_package(LLVM REQUIRED CONFIG)` and `LLVM_LINK_COMPONENTS`.

**LLVM IR** is a typed, SSA form organized `Module → Function → BasicBlock → Instruction`. Every block ends in exactly one terminator (`br`, `switch`, `ret`). The `phi` node selects per incoming edge, must appear at block start, and cannot appear in the entry block; the `alloca`+`load`/`store` alternative is cleaned up by `mem2reg`.

---

## 🔤 Frontend Construction

The Kaleidoscope arc (`calc`, `tinylang`): hand-written lexer → recursive-descent parser (LL(1)-friendly) → AST → semantic analysis → IR via `IRBuilder`. Diagnostics use the `.def`/X-macro pattern (`Diagnostic.def` with `DIAG(ID, Level, Msg)`). ASTs use LLVM-style RTTI (`classof`, `dyn_cast`); scopes resolve with a `StringMap<Decl*>` per scope.

SSA is built with the Braun et al. "sealed block" algorithm: insert an empty `PHINode`, track `IncompletePhis` and a `Sealed` flag, backfill via `addIncoming`, then simplify. Arrays use `CreateAlloca`/`CreateInBoundsGEP`/`CreateLoad`; structs and vtables map to LLVM structs and globals. Exception handling uses Itanium-style IR (`landingpad`, `__cxa_allocate_exception`, `llvm.eh.typeid.for`); debug info uses `DIBuilder` (`DIFile`, `DISubprogram`, `llvm.dbg.declare`, `setDebugLoc`).

---

## 🔁 Passes and the Pass Manager

New-PM transforms derive from `PassInfoMixin<PassT>` with `PreservedAnalyses run(IRUnitT&, AnalysisManagerT&)`; analyses derive from `AnalysisInfoMixin` with a static `AnalysisKey Key` and a `Result` typedef. Register in `llvm/lib/Passes/PassRegistry.def`.

```cpp
void RegisterCB(PassBuilder &PB) {
  PB.registerPipelineParsingCallback(
    [](StringRef Name, ModulePassManager &MPM, ArrayRef<PassBuilder::PipelineElement>) {
      if (Name == "ppprofiler") { MPM.addPass(PPProfilerIRPass()); return true; }
      return false;
    });
}
```

Build a plugin with `add_llvm_pass_plugin(...)` and run: `opt -load-pass-plugin=PPProfiler.so -passes="ppprofiler" --stats hello.ll -o hello_inst.bc`. Drivers build pipelines with `PassBuilder::buildPerModuleDefaultPipeline(...)` and extension points; emission uses `TargetMachine::addPassesToEmitFile(...)`.

---

## 📋 TableGen and Instruction Selection

TableGen is a DSL producing *records* flattened at build time into `.inc` files. Constructs: `class`, `def`, `multiclass`+`defm`, `let`, `foreach`, `defvar`, bang operators.

```tablegen
multiclass Logic<bits<5> Fun, string OpcStr, SDNode OpNode> {
  let isCommutable = 1 in
  def rr : F_LR<Fun, 0b0, OpcStr, [(set i32:$rd, (OpNode GPROpnd:$rs1, GPROpnd:$rs2))]>;
  def rrc : F_LR<Fun, 0b1, OpcStr,
                 [(set i32:$rd, (OpNode GPROpnd:$rs1, (not GPROpnd:$rs2)))]>;
}
defm AND : Logic<0b01000, "and", and>;
defm XOR : Logic<0b01010, "xor", xor>;
```

Two selectors: **SelectionDAG** (build DAG → type legalization → operation legalization → DAG combine → select → schedule) and **GlobalISel** (modular: IRTranslator → Legalizer → RegBankSelect → InstructionSelect). Legalization actions: promote/widen/expand/legalize/custom. SDISel legal types are declared with `addRegisterClass(MVT::i16, &GPR16RegClass)` + `computeRegisterProperties(...)`; GlobalISel uses `LegalizeRuleSet`:

```cpp
getActionDefinitionsBuilder({G_LOAD, G_STORE})
  .legalForTypesWithMemDesc({{s8,p0,s8,8},{s16,p0,s8,8},{s32,p0,s32,8}})
  .clampScalar(0, s16, s32)
  .scalarize(0)
  .lower();
```

Matching uses TableGen patterns (`Pat`, `PatFrag`, `ComplexPattern`, `SDNodeXForm`); custom legalization needs `ReplaceNodeResults`/`LowerOperationWrapper`.

---

## ⚙️ Backend Pipeline: Calling Conventions, RA, Scheduling, Frame

Machine IR is typed `.mir` (YAML) with `MachineFunction`/`MachineFrameInfo`/`MachineRegisterInfo`. Register classes map `TargetRegisterClass` (Machine) to `MCRegisterClass` (MC); tied operands and early-clobber are the key constraints.

Calling conventions are described in TableGen via `CCState` + `CCValAssign`; SDISel hooks are `LowerFormalArguments`, `LowerReturn`, `LowerCall`, `CanLowerReturn`. Frame lowering uses `MachineFrameInfo` (fixed vs spill objects), `TargetFrameLowering` (`emitPrologue`/`emitEpilogue`), and `TargetRegisterInfo` (`eliminateFrameIndex`), with register scavenging and an emergency spill slot.

Scheduling uses `MachineScheduler` + `TargetSchedModel`/`MCSchedModel` (`SchedWriteRes`, `SchedReadAdvance`, `InstRW`); a scheduler without a real processor model defaults to a 4-cycle load latency and schedules poorly. Register allocation splits into coalescing (`RegisterCoalescer`) and assignment (`createGreedyRegisterAllocator`, or PBQP/linear-scan) over `SlotIndex`/`LiveInterval`; spilling uses `storeRegToStackSlot`/`loadRegFromStackSlot`.

---

## 🧾 MC Layer, JIT and Tooling

MC components: `MCInstPrinter` (MCInst → text), `MCTargetAsmParser` (text → MCInst), `MCCodeEmitter` (MCInst → bytes), `MCAsmBackend` (fixups), `MCObjectTargetWriter` (relocations) — most generated by TableGen and registered through `TargetRegistry::Register*`.

```cpp
uint64_t Encoding = getBinaryCodeForInstr(MI, Fixups, STI);
support::endian::write<uint32_t>(CB, Encoding, llvm::endianness::little);
```

The **ORC JIT** stack is `RTDyldObjectLinkingLayer` → `IRCompileLayer(ConcurrentIRCompiler)` → `IRTransformLayer(optimizeModule)`, with `ExecutionSession`, `MangleAndInterner`, `JITDylib`. `LLJIT` gives a working JIT (`LLJITBuilder().create()`, `addIRModule`, `lookup`); `InitializeNativeTarget*` is mandatory.

Debug loop:

```bash
opt -passes=simplifycfg input.ll -S -o -
opt -passes=slp-vectorizer -debug-only=SLP input.ll -S -o output.ll
llc -O1 -mtriple h2blb input.ll -debug-pass=Structure -stop-before=peephole-opt -o /dev/null
llc input.ll -run-pass=regalloc -verify-machineinstrs -o -
```

Lit tests encode commands and checks in one file (`; RUN: llc < %s -o - | FileCheck %s`); `FileCheck` directives include `CHECK`, `CHECK-NEXT`, `CHECK-DAG`, `--check-prefixes`; `llvm-reduce`/`bugpoint` shrink reproducers.

---

## ⚠️ Backend Pitfalls

Patterns must respect canonical form (else `Type set is empty for each HW mode`); ambiguous register classes need explicit `(i32 GPR32:$dst)` disambiguation; enabling the scheduler without a model yields poor schedules (and disables SDISel's own scheduling); aggressive coalescing inflates register pressure; physical-register pinning creates long live ranges; removing IR references from `.mir` loses alias information; spilling constants can often be avoided by recomputing them.

---

## 🔗 Integration with Other Skills

- For language-level C++ patterns that generate IR, see [lang-cpp](../../../languages/lang-cpp/SKILL.md) and [cpp-template-metaprogramming](../../../languages/cpp-template-metaprogramming/SKILL.md).
- For compiler frontend theory (lexing, parsing, SSA), see [academic-compilers-language-processors](../../../domains/academic/academic-compilers-language-processors/SKILL.md).
- For CI wiring of toolchain builds, see [program-github-actions](../../../platforms/program-github-actions/SKILL.md).
