---
name: "lang-lua"
description: "Provides software engineering patterns in Lua. Covers the use of local variables, efficient table manipulation, metamethods/metatables, closures, cooperative concurrency with coroutines, performance optimization, and C/C++ integration through the native API or the LuaJIT FFI."
---

# AI Skill: Lua Engineering (Lua Specialist)

This skill guides the AI to act as a specialist in the **Lua** language (applicable to both standard Lua 5.1-5.4 and LuaJIT), with a focus on performant, clean, maintainable, and idiomatic code. The goal is to avoid the common memory and performance pitfalls that arise from the language's syntactic simplicity.

---

## 🧭 Lua Development Guidelines

While working under this skill, apply the following patterns strictly:

### 1. Scope and Local Variables
- **Local by Default**: Always declare variables with the `local` keyword. Globals are costly to look up, pollute the global environment (`_G`), and can cause silent bugs.
- **Cache Globals**: If functions from global libraries (such as `math.sin`, `table.insert`, `string.format`) are called repeatedly inside loops or high-frequency functions, cache them locally:
  ```lua
  local sin = math.sin
  local insert = table.insert
  ```

### 2. Efficient Table Manipulation (Tables)
- **Tables as the Single Structure**: Tables in Lua are the only structural data type. They represent arrays and dictionaries alike.
- **Indexing**: Remember that Lua arrays are traditionally indexed from **1**, not 0.
- **Pre-allocation (LuaJIT)**: If you know the final table size and are using LuaJIT or specific APIs, use functions that pre-allocate memory to avoid constant resizing.
- **Avoid Excessive Creation**: Avoid instantiating temporary tables in high-frequency loops to reduce pressure on the Garbage Collector (GC). Reuse tables by clearing their fields.

### 3. Object-Oriented Programming with Metatables
- **Prototypes with `__index`**: Implement the prototype pattern in Lua using metatables. The metatable defines the table's behavior under special operations.
- **Basic Class Structure**:
  ```lua
  local Account = {}
  Account.__index = Account

  function Account.new(balance)
      local self = setmetatable({}, Account)
      self.balance = balance or 0
      return self
  end

  function Account:deposit(amount)
      self.balance = self.balance + amount
  end
  ```

### 4. Cooperative Concurrency (Coroutines)
- **Independent States**: Use coroutines to simulate cooperative multithreading or to implement generators.
- **Lifecycle**: Understand the flow among `coroutine.create`, `coroutine.resume`, `coroutine.yield`, and `coroutine.status`.

### 5. C/C++ Integration and LuaJIT FFI
- **Lua C API**: Understand how Lua's virtual stack manages communication and type exchange with native code.
- **FFI (Foreign Function Interface)**: In LuaJIT environments, prefer the `ffi` module to call native C functions without the overhead of traditional wrappers.

---

## 🧰 Recommended Code Patterns

### Classic Object-Oriented Implementation with Inheritance

```lua
-- Base Class
local Animal = {}
Animal.__index = Animal

function Animal.new(name)
    local self = setmetatable({}, Animal)
    self.name = name or "Unknown"
    return self
end

function Animal:makeSound()
    return "Some generic sound"
end

-- Derived Class
local Dog = setmetatable({}, Animal)
Dog.__index = Dog

function Dog.new(name, breed)
    -- Call base constructor
    local self = setmetatable(Animal.new(name), Dog)
    self.breed = breed or "Mixed"
    return self
end

-- Override method
function Dog:makeSound()
    return "Woof! Woof!"
end

-- Usage
local myDog = Dog.new("Rex", "German Shepherd")
print(myDog.name)       -- Output: Rex
print(myDog:makeSound()) -- Output: Woof! Woof!
```

### Dynamic Cache with Weak Tables

Weak tables help prevent memory leaks by caching references that can be collected when no other references to them exist.

```lua
-- Table with weak values
local cache = {}
setmetatable(cache, { __mode = "v" }) -- 'k' for weak keys, 'v' for weak values

local function getCachedObject(id, generator)
    local obj = cache[id]
    if not obj then
        obj = generator(id)
        cache[id] = obj
    end
    return obj
end
```

### Efficient Integration via LuaJIT FFI

```lua
local ffi = require("ffi")

-- Declare C prototypes
ffi.cdef[[
    int printf(const char *fmt, ...);
    typedef struct { double x, y; } point_t;
]]

-- Call C functions directly
ffi.C.printf("Hello from C printf via LuaJIT FFI!\n")

-- Create C structures directly in memory
local point = ffi.new("point_t", 10.5, 20.2)
ffi.C.printf("Point coordinates: x=%f, y=%f\n", point.x, point.y)
```

## 🔒 Security Issues and Safe Practices

- **Sandbox Escaping**: When running user-supplied Lua scripts, restrict access to dangerous global functions (`load`, `loadstring`, `require`, `os.execute`, `io`, and `package` modules).
- **Metatable Handling**: Protect the metatables of internal objects so external code cannot alter the application's native behavior or escalate privileges.
- **Overflows in LuaJIT / C APIs**: When integrating with C through the Lua API, validate Lua stack bounds rigorously to avoid corrupting the interpreter's native memory.
