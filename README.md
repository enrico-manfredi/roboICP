# roboICP

**roboICP** is an open-source laboratory automation platform for **high-throughput preparation of dissolution samples for ICP-AES / ICP-OES analysis**.  
The system automates repetitive and error-prone steps—solid dosing, reaction handling, vial filling, and dilution—using a modular combination of mechanical hardware, embedded control, and Python-based orchestration.

The project was developed to support materials and chemical research workflows where **large sample volumes**, **tight mass/volume control**, and **reproducibility** are required, and where manual preparation becomes a throughput bottleneck.

---

## Project goals

- Automate dissolution-to-vial workflows for ICP analysis  
- Improve **repeatability, throughput, and operator time efficiency**
- Enable **scalable sample counts** without proportional increases in labour
- Provide a **transparent, hackable platform** suitable for research labs

---

## System overview

roboICP integrates mechanical hardware, embedded control, and high-level software into a single automated workflow.

Key elements include:
- Reaction vessels and mixing hardware
- Automated vial handling and filling
- Automated solid dispensing
- Arduino-based low-level control of motors, actuators, and timing-critical tasks
- Python scripts and Jupyter notebooks for protocol definition, execution logic, and data logging

The system is intentionally modular: individual subsystems can be modified or replaced without redesigning the entire platform.

---

## Key design iterations (Mk1 → Mk2)

This repository documents multiple design iterations developed through hands-on operation.

**Mk2 hardware changes were driven by real operational bottlenecks identified during Mk1 use**, rather than theoretical design optimisation.

### New vial holder
- Increased total vial capacity
- Improved mechanical alignment and repeatability
- Enabled **simultaneous vial handling**, reducing cycle time per batch

### New solid feeder
- Developed to address **reliable automated solid dispensing**, a well-known challenge in laboratory automation
- Supports controlled dosing of solids and improved consistency across samples
- Designed to integrate directly with automated reaction and dilution workflows

Automated solids handling is substantially more difficult than liquid dispensing due to flow variability, bridging, and adhesion.  
The Mk2 solid feeder was developed specifically to address these issues rather than avoid them.

Design rationale, assembly details, and lessons learned are documented in the accompanying documentation and presentation files.

---

## Documentation

The repository includes detailed written documents and slide decks covering:
- Physical assembly of the system
- Mechanical and control design decisions
- Limitations observed during Mk1 operation
- Proposed architecture and improvements for Mk2

These materials are intended to make the system understandable and reproducible beyond the source code alone.

---

## Intended users

- Research labs running **ICP-AES / ICP-OES** with high sample volumes
- Chemists and materials scientists interested in **laboratory automation**
- Engineers working on **mechatronics for chemical workflows**
- Employers assessing practical experience in:
  - hardware–software integration
  - experimental automation
  - iterative prototyping under real constraints

---

## Current status and limitations

- The system is a **research-grade automation platform**, not a commercial product
- Safety, calibration, and compliance must be validated for each laboratory environment
- Hardware designs are provided as-is and may require adaptation

---

## Authors and contributors

**Primary author and system architect**  
**Enrico Manfredi**  
Overall system design, mechanical architecture, experimental specification, hardware–software integration, iterative Mk1 → Mk2 development, and project direction.

**Contributors**

**Sarthak Das** — Paid summer intern  
Worked on development of the **initial control code and concepts** for the solids hopper, rail-based filtration system, and elements of the dilution workflow.  
Also contributed CAD and documentation files included in this repository.

**Dewen Sun** — Paid summer intern  
Worked on development of the **initial automation logic and control scripts** for solids handling concepts, filtration workflow, and dilution system sequencing.  
Contributions focused on early-stage prototyping and proof-of-concept implementations.

*Note: Contributors were engaged as paid summer interns and worked on specific subsystems under supervision.  
System integration, final architecture, validation, and subsequent design iterations were led and completed by the primary author.*

---

## License

This project is released under the **MIT License**.  
You are free to use, modify, and build upon it with attribution.

## File Structure
roboICP/
├── Arduino Script/
│ └── main_script/
│ └── main_script.ino # Arduino firmware for motors, actuators, timing
│
├── Python Scripts/
│ ├── control/ # High-level experiment orchestration
│ ├── dilution/ # Dilution logic and sequencing
│ ├── filtration/ # Rail-based filtration control
│ └── analysis/ # Data handling and logging (Jupyter / Python)
│
├── Documents/
│ ├── build_notes.pdf # Assembly notes and build rationale
│ ├── system_overview.pptx # End-to-end system explanation
│ └── mk2_design_notes.pptx # Proposed Mk2 improvements
│
├── Final Assembly/
│ └── assembly_guides/ # Mechanical assembly references
│
├── Reaction System/
│ └── reactor_designs/ # Reaction vessel hardware designs
│
├── New Mixer Design/
│ └── mixer_cad/ # Updated mixer CAD files
│
├── New Solids Dispenser/
│ └── hopper_and_feeder/ # Mk2 solids dispensing hardware
│
├── Sarthaks CAD Files/
│ └── legacy_cad/ # Early CAD iterations and concepts
│
├── README.md
└── LICENSE