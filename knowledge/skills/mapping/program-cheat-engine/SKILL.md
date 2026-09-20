---
name: "program-cheat-engine"
description: "Provides expertise in developing Auto Assembler and Lua scripts for Cheat Engine 7.5 and 7.7. Covers code injection patterns, memory manipulation, and script conversion and compatibility techniques between versions 7.5 and 7.7."
---

# AI Skill: Cheat Engine Engineering (Cheat Engine Specialist)

This skill guides the AI to act as a specialist in reverse engineering and automation in **Cheat Engine (CE)**, focusing specifically on versions **7.5** and **7.7**. It covers creating robust Auto Assembler (AA) scripts, Lua control scripts, DBVM debugging, and best practices for converting scripts and tables between versions 7.5 and 7.7.

---

## 🧭 Cheat Engine Development Guidelines

When working in this skill, apply the following principles:

### 1. Auto Assembler (AA) Robustness
- **AOBScan (Array of Bytes Scan)**: Always prefer `aobscan` or `aobscanmodule` over static addresses. Static addresses change with every game update, whereas byte signatures (AOB) are far more resilient.
- **Resource Cleanup**: Ensure every memory block allocated with `alloc` is properly released with `dealloc` in the script's `disable` section.
- **Symbol Registration**: Register important label names using `registerSymbol` so Lua scripts and the Cheat Engine interface can reference them. Make sure to use `unregisterSymbol` in `disable`.

### 2. Lua and GUI Integration
- **Lazarus/LCL Interface**: When designing forms (`Forms`) via Lua, use the CE visual designer and generate the corresponding XML/LFM, or instantiate the components dynamically while ensuring object lifecycle management.
- **Read/Write Safety**: Always handle possible memory read exceptions on dynamic pointers using `pcall` or by checking memory validity before attempting to read/write.

---

## 🔍 Cheat Engine 7.5 vs 7.7: Differences and Incompatibilities

### 1. Behavior of Lua Memory APIs
- **CE 7.5**: Methods such as `readInteger` or `readPointer` return `nil` if the address is invalid or cannot be read.
- **CE 7.7**: Stricter exception behavior. In certain contexts, attempting to read protected or unmapped addresses can throw a Lua execution error instead of merely returning `nil`, crashing script execution if not handled with `pcall`.

### 2. Auto Assembler Compiler Updates
- **Alloc Size**: In version 7.7, the Auto Assembler parser is stricter about allocations that omit the default size or depend on implicit directives.
- **AVX/AVX2/AVX-512 Support**: Version 7.7 has improved support and correct disassembly of newer vector instructions. Scripts written for 7.7 using these instructions may fail to assemble in version 7.5 if the internal assembler does not recognize the mnemonics.

### 3. GUI Modifications (LCL - Lazarus Component Library)
- Because of the Lazarus compiler update used to build Cheat Engine 7.7, some properties of Lazarus visual components (`TControl`, `TForm`, etc.) were modified or deprecated. Complex graphical customization Lua code written for 7.5 may raise nonexistent-property errors in 7.7.

---

## 🔄 Script Conversion and Compatibility Guide

To ensure a Cheat Table (`.CT`) works perfectly in both Cheat Engine 7.5 and 7.7, adopt the following conversion and backward-compatibility practices:

### 1. Dynamic Version Detection via Lua
Use the `getCEVersion()` function to adapt script behavior at runtime.

```lua
local ceVersion = getCEVersion()

if ceVersion >= 7.7 then
    -- CE 7.7 specific routine
    print("Running on Cheat Engine 7.7 or newer")
else
    -- CE 7.5 / Legacy fallback
    print("Running on legacy Cheat Engine version: " .. tostring(ceVersion))
end
```

### 2. Safe Address Reads with `pcall`
To avoid crashes in the Lua script due to stricter reads in version 7.7, wrap failure-prone memory reads:

```lua
-- Safe read helper compatible with both 7.5 and 7.7
function safeReadInteger(address)
    local success, value = pcall(readInteger, address)
    if success then
        return value
    else
        return nil
    end
end
```

### 3. Portable Auto Assembler Writing
- **Define sizes explicitly**:
  *Instead of:*
  `alloc(newmem)`
  *Use:*
  `alloc(newmem, 2048)` or the minimum size needed for your injected code.
- **Do not overuse specific directives**: Avoid overusing directives whose behavior changed or that were added recently if the script must run on version 7.5.

---

## 🧰 Recommended Code Patterns

### Classic Compatible Auto Assembler Script (7.5 and 7.7)

```assembly
[ENABLE]
// Find the instruction pattern in the game module
aobscanmodule(INJECT, game.exe, 8B 40 10 89 45 FC 48 8D)
alloc(newmem, 2048, INJECT)
label(code)
label(return)
registerSymbol(INJECT)

newmem:
  // Hook logic goes here
  // Example: Multiply value by 2
  mov eax, [rax+10]
  shl eax, 1
  mov [rbp-04], eax
  jmp return

code:
  // Original instruction
  mov eax,[rax+10]
  mov [rbp-04],eax
  jmp return

INJECT:
  jmp newmem
  nop
return:

[DISABLE]
INJECT:
  // Restore original instructions
  db 8B 40 10 89 45 FC

unregistersymbol(INJECT)
dealloc(newmem)
```

### Lua Script for Version-Conditional Injection

```lua
-- Activating script based on version check
local REQUIRED_VERSION = 7.5
local currentVersion = getCEVersion()

if currentVersion < REQUIRED_VERSION then
  showMessage("This cheat table requires at least Cheat Engine " .. tostring(REQUIRED_VERSION))
  return
end

-- Hook an event to handle version-based behaviors
local memrec = getAddressList().getMemoryRecordByDescription("Cheat Active State")
if memrec then
  memrec.OnActivate = function(sender, beforeState, currentState)
    if currentState then
      print("Cheat activated on Cheat Engine version " .. tostring(currentVersion))
      -- Safe execution block
      local status, err = pcall(function()
        if currentVersion >= 7.7 then
          -- Run 7.7 optimized routines (e.g., using new memory APIs)
        else
          -- Run 7.5 routines
        end
      end)
      if not status then
        print("Error during activation: " .. tostring(err))
      end
    end
    return true
  end
end
```
