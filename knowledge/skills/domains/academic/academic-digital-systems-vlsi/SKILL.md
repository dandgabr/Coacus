---
name: academic-digital-systems-vlsi
description: "Specializes in Digital Systems, Logic Synthesis, Hardware Description (Verilog, SystemVerilog, VHDL), and VLSI/CMOS Integrated Circuit Design building on Morris Mano (Digital Design), Weste & Harris (CMOS VLSI Design), Blaine Readler, and Douglas Perry. Covers RTL synthesis, finite state machines (Moore/Mealy FSM), simulation testbenches, Static Timing Analysis (STA - Setup/Hold times, Clock Skew, Jitter), the Elmore RC model, CMOS layout, DRC/LVS rules, FPGA mapping (AMD Xilinx Vivado, Intel Altera Quartus), and Design for Testability (DFT - Scan Chains, BIST)."
---

# Digital Systems, Logic Synthesis, HDL (Verilog/VHDL), and VLSI Design

This skill establishes the unified engineering methodology for modeling, hardware description (RTL), functional simulation, static timing analysis, and synthesis of ASIC and FPGA integrated circuits building on the works of **Morris Mano** (*Digital Design*) and **Neil Weste & David Harris** (*CMOS VLSI Design*).

---

## 💻 1. RTL Hardware Description: Verilog, SystemVerilog & VHDL

### 1.1 Synchronous Counter with Asynchronous Reset in Verilog / SystemVerilog
```verilog
// SystemVerilog IEEE 1800-2017
module counter_8bit (
    input  logic       clk,
    input  logic       rst_n,   // Reset assíncrono ativo em nível baixo (low-active)
    input  logic       enable,
    output logic [7:0] count
);

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 8'h00;
        end else if (enable) begin
            count <= count + 1'b1;
        end
    end

endmodule
```

### 1.2 Finite State Machine (Moore FSM) in VHDL
```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity fsm_moore is
    Port (
        clk    : in  STD_LOGIC;
        rst_n  : in  STD_LOGIC;
        din    : in  STD_LOGIC;
        dout   : out STD_LOGIC
    );
end entity fsm_moore;

architecture Behavioral of fsm_moore is
    type state_type is (STATE_IDLE, STATE_ACTIVE, STATE_DONE);
    signal current_state, next_state : state_type;
begin

    -- Processo Sequencial de Transição de Estado
    process(clk, rst_n)
    begin
        if rst_n = '0' then
            current_state <= STATE_IDLE;
        elsif rising_edge(clk) then
            current_state <= next_state;
        end if;
    end process;

    -- Lógica Combinacional de Próximo Estado e Saída
    process(current_state, din)
    begin
        case current_state is
            when STATE_IDLE =>
                dout <= '0';
                if din = '1' then next_state <= STATE_ACTIVE; else next_state <= STATE_IDLE; end if;
            when STATE_ACTIVE =>
                dout <= '1';
                next_state <= STATE_DONE;
            when STATE_DONE =>
                dout <= '0';
                next_state <= STATE_IDLE;
        end case;
    end process;

end architecture Behavioral;
```

---

## 📐 2. Static Timing Analysis (STA)

To avoid race conditions and metastability in clocked registers with period $T_{clk} = 1/f_{clk}$:

```
Flip-Flop 1 (Lauch) ──[t_cq]──> [ Lógica Combinacional t_comb ] ──> [t_setup/t_hold]──> Flip-Flop 2 (Capture)
      │                                                                                        │
      └──────────────────────────[ Clock Skew t_skew ]─────────────────────────────────────────┘
```

1. **Setup Time Condition**:
   $$T_{clk} \ge t_{cq} + t_{comb, max} + t_{setup} - t_{skew} + t_{jitter}$$
   - *Setup Violation*: Occurs when the combinational path is excessively long. Solution: Insertion of intermediate registers (*Pipelining*).
2. **Hold Time Condition**:
   $$t_{cq} + t_{comb, min} \ge t_{hold} + t_{skew}$$
   - *Hold Violation*: Depends exclusively on minimum delays and cannot be fixed by lowering the clock frequency. Solution: Insertion of delay buffers on the data path.

---

## 🔬 3. CMOS Physical Design, Layout, and DRC/LVS Rules

- **Elmore RC Delay Model**:
  $$t_{pd} \approx \sum_{i} R_i \cdot C_i \approx 0.69 \cdot R_{eq} C_L$$
- **Geometric Manufacturing Rules (DRC - Design Rule Checking)**: Minimum spacing between diffusions, polysilicon overlap, and minimum metal trace width ($M1-Mn$).
- **LVS (Layout Versus Schematic)**: Extraction of the parasitic netlist ($R, C$) from the physical layout and 1:1 verification of logic equivalence against the SPICE schematic.
- **Design for Testability (DFT)**: Automatic insertion of *Scan Chains* and built-in test pattern generators/analyzers (*BIST - Built-In Self-Test*) to achieve *Stuck-at Fault* coverage $> 99\%$.
