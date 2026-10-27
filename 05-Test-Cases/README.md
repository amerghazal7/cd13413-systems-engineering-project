# Smart Home Security System (SHSS): Systems Engineering Capstone

This is my submission for the capstone of the Udacity Systems Engineering Nanodegree (course cd13413): the design and validation of a smart home security system with motion, door/window and water-leak sensors, cameras, an alarm, smart-home controllers, a central control unit and a set of cloud services. The repository is a fork of [udacity/cd13413-systems-engineering-project](https://github.com/udacity/cd13413-systems-engineering-project); the original starter files are untouched under `starter/`.

## What is where

| # | Deliverable | Where to look |
|---|---|---|
| 1 | System Requirements Specification (IEEE 29148 §9.4 structure, all ten sections, optional ones included) | [`01-SysRS/SysRS_Smart_Home_Security_System.pdf`](01-SysRS/SysRS_Smart_Home_Security_System.pdf) is the submission. The Markdown I wrote it in is next to it. |
| 2 | Architecture diagram (draw.io) | [`02-Architecture/SHSS_Architecture.drawio`](02-Architecture/SHSS_Architecture.drawio), with a PNG preview beside it. |
| 3 | SysML diagrams (PlantUML) | [`03-SysML/`](03-SysML/): eight `.puml` files and their rendered PNGs in `images/`. |
| 4 | Decision matrices (.xlsx, Udacity template layout) | [`04-Decision-Matrix/SHSS_Decision_Matrices.xlsx`](04-Decision-Matrix/SHSS_Decision_Matrices.xlsx), one tab per trade-off plus a README tab. |
| 5 | Testomat test cases | [`05-Test-Cases/Testomat_export_Smart_Home_System_test_cases.xlsx`](05-Test-Cases/Testomat_export_Smart_Home_System_test_cases.xlsx) is the export from Testomat. `test_cases.md` is the same content in readable form, and `test_cases.py` is the file I generate both from. |

## How I went about it

1. **Requirements first, but not in one go.** I started with a short needs analysis (my own household, two neighbours, one installer, and a lot of one-star reviews) and wrote the purpose, scope and user types. The requirement tables came later and were revised twice.
2. **Trade-offs before locking the architecture.** The decision matrices decided the three things everything else depends on: Zigbee for battery devices, PoE cameras, and a local-first server with a thin cloud relay rather than local-only or cloud-only. After that I went back and corrected Sections 2, 6 and 8 of the SysRS.
3. **Models as code.** The architecture is a draw.io file; the SysML diagrams are PlantUML, so block names in the diagrams and in the document are literally the same strings and the figures can be regenerated.
4. **Tests traced to requirements.** Verification tests reference requirement IDs (FR-MD-01 and so on); validation scenarios go back to the needs N1 to N7. I added internet-outage, power-failure and guest-first-use scenarios on top of the ones the brief asked for.

## The design in one paragraph

A small Linux mini PC (Raspberry Pi 5 or Intel N100 class) in the house is the central control unit. It runs the Smart Home Manager stack: rules and alarm engine, REST/WebSocket API, MQTT broker, PostgreSQL, a network video recorder on a 2 TB encrypted SSD, a Zigbee 3.0 coordinator, an LTE backup modem and a UPS. All sensors and actuators are Zigbee 3.0 (PIR motion, door/window contacts, water leak, glass-break, smoke/CO; smart lock, lights, garage relay, indoor siren), the outdoor siren and strobe are wired to a 12 V relay on the control unit, and the cameras are PoE ONVIF cameras on a UPS-backed switch. Users interact through a mobile app, a web dashboard and a wall keypad. The cloud does only what cannot be done locally: an outbound TLS relay for remote access and video, push notifications, identity with MFA, encrypted backup and signed updates. If the internet goes down, nothing that matters stops working.

## SysML diagrams

| File | Diagram |
|---|---|
| `01_bdd_system_blocks.puml` | Block definition diagram: control unit, sensors, cameras, alarm, user interface, power supply, cloud services, controllers, network |
| `02_ibd_interfaces.puml` | Internal block diagram: parts and the protocol on every connection |
| `03_use_cases.puml` | Use cases for Admin, Resident, Guest, Installer, Monitoring Centre and Cloud |
| `04_requirements.puml` | Requirements diagram with derive, satisfy and verify relationships to blocks and test cases |
| `05_state_machine.puml` | Modes and states: Disarmed, Exit/Entry Delay, Armed Away/Home/Night, Alarm, Degraded, Maintenance, Setup |
| `06_seq_intrusion_alarm.puml` | Sequence: intrusion detection, siren, notification, monitoring report |
| `07_seq_remote_live_view.puml` | Sequence: remote login with MFA and camera live view through the cloud relay |
| `08_context_diagram.puml` | System context: boundary, actors, external systems |

To re-render: `java -jar plantuml.jar -tpng -o images 03-SysML/*.puml`, or paste a file into the editor at https://plantuml.com/plantuml.

## Test cases

The Testomat project is called *Smart Home System* (Classical). Each test has a name, objective, priority, type, precondition, numbered steps with the expected outcome of each step, and an overall expected result; some carry a short practical note.

* **Verification (7):** motion sensor, door/window sensor, water-leak sensor, camera and smart-lock integration; login with correct credentials; login with wrong credentials and lockout.
* **Validation (9):** motion detection and alert notification, door/window activation, remote camera access and live view, arm/disarm, guest first-use disarm (user acceptance); simultaneous sensor triggers and high-volume user access (load); internet outage and mains power failure (resilience).

## Tools

draw.io, PlantUML with Graphviz, python-markdown and headless Chrome for the PDF, openpyxl for the workbook, Testomat for the test cases.

## License

[License](LICENSE.txt)
