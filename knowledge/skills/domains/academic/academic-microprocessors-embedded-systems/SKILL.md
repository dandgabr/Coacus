---
name: academic-microprocessors-embedded-systems
description: "Specializes in Microprocessor Architecture, Embedded Systems, RTOS, and Embedded Linux building on Patterson & Hennessy (Computer Organization and Design), Rodolfo Giometti (Yocto Project), and Andrew Eliasz (Zephyr RTOS). Covers ARM Cortex-M/A/R microcontrollers, RISC-V (RV32I/RV64G), Assembly, 5-stage pipelines with Data Forwarding and Branch Prediction, L1/L2/L3 cache hierarchies, buses (UART, SPI, I2C, CAN, USB), DMA, FreeRTOS, Zephyr RTOS, the Yocto Project (BitBake, .bb recipes, meta-layers), Device Trees, and U-Boot bootloaders."
---

# Microprocessor Architecture, RTOS, and Embedded Linux (Yocto & Zephyr)

This skill establishes the principles of computer architecture, microprocessor design (ARM and RISC-V), hardware peripheral control, deterministic real-time programming with **FreeRTOS / Zephyr RTOS**, and compilation of custom operating systems with the **Yocto Project**.

---

## 💻 1. Classic 5-Stage Pipeline (IF, ID, EX, MEM, WB)

```
[ IF: Busca de Instrução ] ──> [ ID: Decodificação & Registradores ]
                            ──> [ EX: Execução na ULA / Cálculo de Branch ]
                            ──> [ MEM: Acesso à Memória de Dados ]
                            ──> [ WB: Escrita de Retorno no Registrador ]
```

### 1.1 Hazard Resolution
- **Structural Hazard**: Separate Instruction and Data caches (Harvard Architecture / L1 Split).
- **Data Hazard**: Direct forwarding (*Data Forwarding / Bypassing*) from the ALU/MEM output directly to the ALU inputs of the next cycle without stall bubbles.
- **Control Hazard**: 2-bit dynamic (*Branch Predictor*) (bimodal / gshare) and *branch delay slots*.

---

## 🔌 2. Hardware Buses and Peripherals

| Bus | Topology | Wires / Signals | Typical Rate | Applications |
| :--- | :--- | :--- | :--- | :--- |
| **UART** | Point-to-point, asynchronous, Full-Duplex | TX, RX, GND | 9.6 kbps – 921.6 kbps | Debug logs, GPS/Bluetooth modules |
| **SPI** | Master-Slave, synchronous, Full-Duplex | MOSI, MISO, SCK, CS | 10 MHz – 80 MHz | OLED displays, NOR Flash memory, SD cards |
| **I2C** | Multi-master bus, synchronous, Half-Duplex | SDA, SCL (Pull-up) | 100 kHz, 400 kHz, 3.4 MHz | MEMS sensors (IMU, temperature), RTC, EEPROM |
| **CAN / CAN-FD** | Noise-immune differential bus | CAN_H, CAN_L (120 $\Omega$) | 1 Mbps (CAN) / 5-8 Mbps (FD) | Automotive industry, aerospace, automation |

---

## ⏱️ 3. Real-Time Programming: Zephyr RTOS & FreeRTOS

```c
#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#define STACK_SIZE 1024
#define PRIORITY 7

K_THREAD_STACK_DEFINE(sensor_stack, STACK_SIZE);
struct k_thread sensor_thread_data;
K_SEM_DEFINE(data_ready_sem, 0, 1);

void sensor_worker(void *p1, void *p2, void *p3) {
    while (1) {
        k_sem_take(&data_ready_sem, K_FOREVER);
        printk("Processando telemetria determinística no Zephyr RTOS\n");
        k_msleep(100);
    }
}

int main(void) {
    k_thread_create(&sensor_thread_data, sensor_stack,
                    K_THREAD_STACK_SIZEOF(sensor_stack),
                    sensor_worker, NULL, NULL, NULL,
                    PRIORITY, 0, K_NO_WAIT);
    
    while (1) {
        k_msleep(1000);
        k_sem_give(&data_ready_sem);
    }
    return 0;
}
```

---

## 🐧 4. Embedded Linux: Yocto Project, BitBake, and Device Trees

### 4.1 Layer Structure and BitBake Recipes
```
meta-custom-bsp/
├── conf/layer.conf
├── recipes-bsp/
│   ├── u-boot/u-boot-custom_%.bbappend
│   └── device-tree/custom-board.dts
└── recipes-kernel/
    └── linux/linux-yocto-custom_6.6.bb
```

### 4.2 Example Device Tree Source (`.dts`) for I2C Peripheral Mapping
```dts
&i2c1 {
    status = "okay";
    clock-frequency = <400000>;

    sensor_imu: mpu6050@68 {
        compatible = "invensense,mpu6050";
        reg = <0x68>;
        interrupt-parent = <&gpio1>;
        interrupts = <15 IRQ_TYPE_EDGE_RISING>;
    };
};
```

---

## 🔩 5. Bare-Metal Embedded C (Gbati)

Before any RTOS or Embedded Linux, a firmware engineer must own the hardware from reset. This section covers the STM32F411 / ARM Cortex-M4 path, generalizing to any Cortex-M part. Resolve the specific reference-manual register names from the vendor before use.

### 5.1 Memory map, memory-mapped I/O and clock gating
- Memory regions: Flash at `0x08000000` (`rx`), SRAM at `0x20000000` (`rwx`), peripherals around `0x40000000`.
- Registers are `volatile` memory-mapped words:
```c
#define GPIOA_MODER (*(volatile unsigned int *)(GPIOA_BASE + 0x00))
GPIOA_MODER |= (1U << 10);   /* PA5 as output */
```
  The CMSIS struct form is safer and readable: `typedef struct { volatile uint32_t MODER, OTYPER, ... } GPIO_TypeDef;` with `#define GPIOA ((GPIO_TypeDef *) 0x40020000)`. Pad register-map gaps with `volatile uint32_t DUMMY[n]`.
- **Enable the peripheral clock before touching its registers** (`RCC->AHB1ENR |= GPIOAEN`, `RCC->APB1ENR |= UART2EN`); forgetting it is the classic silent failure. Use `1U<<n` and `U`/`UL` suffixes. Prefer `BSRR` for atomic pin set/reset over read-modify-write on shared pins.
- **`volatile` is not optional** on MMIO: it stops the compiler from caching or eliding hardware reads.

### 5.2 Startup, linker script and vector table
`ENTRY(Reset_Handler)`; `MEMORY` declares `FLASH`/`SRAM` with `ORIGIN`/`LENGTH`; `_estack = ORIGIN(SRAM)+LENGTH(SRAM)`. `Reset_Handler` copies `.data` flash→SRAM and zeroes `.bss`, then calls `main()`:
```c
uint32_t data_mem_size = (uint32_t)&_edata - (uint32_t)&_sdata;
uint32_t *p_src = (uint32_t*)&_etext, *p_dst = (uint32_t*)&_sdata;
for (uint32_t i = 0; i < data_mem_size; i++) *p_dst++ = *p_src++;
```
The vector table's first word is the initial MSP (`&_estack`), the second is `&Reset_Handler`; every ISR is defaulted `__attribute__((weak, alias("Default_Handler")))`. Keep `.isr_vector_tbl` first in flash and mark it `KEEP(...)` in the linker script, or reset fails silently.

### 5.3 Interrupts, NVIC and peripherals
Cortex-M exceptions plus the NVIC give prioritization, nested preemption and dynamic priority. EXTI workflow: enable GPIO + SYSCFG clocks, configure the pin input, map the line via `SYSCFG->EXTICR[n]`, unmask `EXTI->IMR`, select the edge (`EXTI->RTSR`/`FTSR`), clear `EXTI->PR`, then `NVIC_EnableIRQ(...)`. Wrap setup in `__disable_irq()` / `__enable_irq()`.

Peripheral register groups to master: GPIO (`MODER/OTYPER/OSPEEDR/PUPDR/IDR/ODR/BSRR/AFRL/AFRH`), SysTick, timers (`PSC`/`ARR`/`CR1`/`SR`/`EGR`; `f = clk / ((PSC+1)*(ARR+1))`), UART (`CR1`/`BRR`/`SR`/`DR`; baud `= (periph_clk + baud/2)/baud`), ADC (single vs continuous via `CONT`), SPI (CPOL/CPHA), I2C, RTC (BCD values) and DMA (`SxCR`/`SxPAR`/`SxM0AR`, circular mode).

### 5.4 Boot, power and toolchain
Enter Standby by setting `PWR->CR |= PDRS`, `SCB->SCR |= (1U<<2)` (SLEEPDEEP) and `__WFI()`; wake via the WKUP pin, an RTC alarm or an internal event. Toolchain: `arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -O0 -ffunction-sections -fdata-sections -Wall -g3 -T<ld> -Wl,--gc-sections -Wl,-Map=out.map --specs=nano.specs`; debug over SWD with OpenOCD/ST-LINK; inspect with `arm-none-eabi-{nm,size,objdump,readelf,objcopy}`.

---

## ➕ 6. Modern C++ on Embedded (Viarheichyk)

"You do not pay for what you do not use" holds only under discipline.

- **No dynamic allocation, no exceptions.** Replace `std::vector` with `std::array`; preallocate everything. Exceptions have no provable worst-case unwinding time and are forbidden by MISRA/JSF in safety-critical code — return an `Expected<T>` (a `std::variant<T, std::error_code>`) by value instead. Global objects must have `noexcept` constructors plus an `IsValid()` accessor, since static-initialization failure has no `catch`.
- **Object pools and ring buffers** (`ObjectPool<T, N>`, `RingBuffer<T, N>`) avoid fragmentation and give deterministic timing; size buffers with `constexpr` constants.
- **RAII wrappers** for devices: the constructor opens, the destructor closes (`Lcd`, `SharedMem<T>`, `std::lock_guard`). Peripheral drivers split into a low-level bus half (`SendToI2C`) and a high-level command half (`Call(Function, value)`); on GNU/Linux use `libgpiod` rather than `wiringPi`.
- **Time**: `std::chrono` with `steady_clock` for intervals, `system_clock` for wall time, literal suffixes (`10ms`, `2s`).
- **Cooperative/testability**: debouncing as a polling helper taking a handler function makes real inputs injectable in tests; FreeRTOS (POSIX simulator) covers real-time scheduling, and Linux `SCHED_FIFO` gives only soft real-time. Cross-compile with CMake toolchain variables and `CMAKE_FIND_ROOT_PATH_MODE_*`.

### Reliability recipes
- **Watchdog**: the STM32 IWDG (LSI-clocked, independent of the main clock) starts with `IWDG_KR = 0xCCCC`, is kicked with `0xAAAA`, and unlocked for `IWDG_PR`/`IWDG_RLR` writes with `0x5555`; WWDG offers a true timing *window* for anti-masking. A software watchdog over `alarm()`/SIGALRM plus heartbeats over a `pipe()` and `poll()` give high-availability failover — and safety-critical designs should use *diverse* implementations so two components do not share a latent bug.
- **Memory protection**: statically bounded buffers plus `assert` pre/postconditions; never trust an input `size`. Bare-metal MPU regions and stack canaries harden further.
- **Power management**: Linux sleep states via `/sys/power/state`, RTC wake via `/sys/class/rtc/rtc0/wakealarm`, USB autosuspend; bare-metal equivalents are WFI/Standby with explicit wake sources.
- **Safety tooling**: MISRA C/C++, Adaptive AUTOSAR and JSF guidelines; `cppcheck --std=posix --enable=warning --addon=misra`; formal verification with CPAchecker.

### Pitfalls
Enable the clock before register access; keep `.isr_vector_tbl` first with a correct `_estack`; watch integer widths and treat `data_mem_size` as a **byte** count; avoid non-determinism (generic allocators, exception unwinding); handle endianness, alignment/padding and early-revision errata explicitly; debounce inputs, feed watchdogs and monitor heartbeats.
