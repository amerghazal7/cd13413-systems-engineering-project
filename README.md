# Smart Home Security System (SHSS) — Systems Engineering Capstone

Design and validation of a Smart Home Security System (motion sensors, door/window and water-leak sensors, cameras, alarm, controllers, a local central control unit and cloud services), produced for the Udacity Systems Engineering Nanodegree capstone. Forked from [udacity/cd13413-systems-engineering-project](https://github.com/udacity/cd13413-systems-engineering-project); the original starter files are kept under `starter/`.

## Deliverables

| # | Deliverable | Files |
|---|---|---|
| 1 | **System Requirements Specification (SysRS)** — ISO/IEC/IEEE 29148:2018 §9.4 structure, all 10 sections (optional ones included) | [`01-SysRS/SysRS_Smart_Home_Security_System.pdf`](01-SysRS/SysRS_Smart_Home_Security_System.pdf) (submission), Markdown source [`01-SysRS/SysRS_Smart_Home_Security_System.md`](01-SysRS/SysRS_Smart_Home_Security_System.md) |
| 2 | **Architecture diagram** (draw.io) — local server with database/storage/services and its local + cloud access, controllers and sensors with their connectivity, user interaction channels, cloud services, legend | [`02-Architecture/SHSS_Architecture.drawio`](02-Architecture/SHSS_Architecture.drawio), preview [`02-Architecture/SHSS_Architecture.png`](02-Architecture/SHSS_Architecture.png) |
| 3 | **SysML diagrams** (PlantUML source + rendered PNG) — block definition, internal block (interfaces), use cases, requirements, state machine, two sequence diagrams, system context | [`03-SysML/`](03-SysML/) (`*.puml` code, `images/*.png`) |
| 4 | **Decision matrices** (.xlsx, Udacity template layout, one tab per matrix) — motion / door-window / water-leak sensors, cameras (4 options), smart lock / lighting / siren controllers, local vs cloud vs hybrid server | [`04-Decision-Matrix/SHSS_Decision_Matrices.xlsx`](04-Decision-Matrix/SHSS_Decision_Matrices.xlsx) |
| 5 | **Testomat test cases** — Verification suite (7) and Validation suite (9), exported from Testomat | [`05-Test-Cases/Testomat_export_Smart_Home_System_test_cases.xlsx`](05-Test-Cases/Testomat_export_Smart_Home_System_test_cases.xlsx) (submission), readable copy [`05-Test-Cases/test_cases.md`](05-Test-Cases/test_cases.md), import file used to load Testomat `05-Test-Cases/testomat_import_SHSS.xlsx` |

## Design baseline (consistent across all deliverables)

* **Server / manager:** hybrid, local-first. A Central Control Unit (Raspberry Pi 5 / Intel N100 class mini PC, Linux) runs the *Smart Home Manager* stack: rules & alarm engine, REST/WebSocket API, MQTT broker, PostgreSQL, NVR with 2 TB encrypted SSD, Zigbee 3.0 coordinator, LTE backup modem, UPS. Cloud is used only for remote access (outbound TLS relay, WebRTC), push notifications, identity/MFA, encrypted backup and OTA updates.
* **Sensors:** Zigbee 3.0 battery devices — PIR motion (pet-immune), door/window contacts, water leak, glass-break, smoke/CO.
* **Cameras:** PoE IP cameras (ONVIF/RTSP) on a UPS-backed PoE switch; video stays local.
* **Controllers:** Zigbee smart lock, lights/plugs, garage relay; Zigbee indoor siren plus wired 12 V outdoor siren + strobe.
* **User interfaces:** mobile app, web dashboard, wall keypad/touch panel (PIN, NFC).

## SysML diagrams

| File | Diagram |
|---|---|
| `01_bdd_system_blocks.puml` | Block definition diagram — control unit, sensors, cameras, alarm, user interface, power supply, cloud services, controllers, network |
| `02_ibd_interfaces.puml` | Internal block diagram — parts, ports and the protocol on every connection |
| `03_use_cases.puml` | Use case diagram — Admin, Resident, Guest, Installer, Monitoring Centre, Cloud |
| `04_requirements.puml` | Requirements diagram — derive / satisfy / verify relationships to blocks and test cases |
| `05_state_machine.puml` | State machine — Disarmed, Exit/Entry Delay, Armed Away/Home/Night, Alarm, Degraded, Maintenance, Setup |
| `06_seq_intrusion_alarm.puml` | Sequence — intrusion detection, siren, notification, monitoring report |
| `07_seq_remote_live_view.puml` | Sequence — remote login with MFA and camera live view through the cloud relay |
| `08_context_diagram.puml` | System context — boundary, actors, external systems |

Render with PlantUML: `java -jar plantuml.jar -tpng -o images 03-SysML/*.puml` (or paste the code into https://plantuml.com/plantuml).

## Test cases

Testomat project *Smart Home System* (Classical). Every test follows the required format: name, objective, priority, type, precondition, numbered steps each with an expected outcome, and an overall expected result; requirement IDs trace back to the SysRS.

* **Verification:** motion sensor, door/window sensor, water-leak sensor, security camera and smart-lock integration; login with correct credentials; login with wrong credentials and lockout.
* **Validation:** user acceptance — motion detection and alert notification, door/window activation, remote camera access and live view, arm/disarm, guest first-use disarm; load — simultaneous sensor triggers (≥ 3), high-volume user access (≥ 3 devices); resilience — internet outage, mains power failure.

## License

[License](LICENSE.txt)
