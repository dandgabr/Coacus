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
