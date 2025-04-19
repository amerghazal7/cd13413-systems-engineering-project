
# Systems Requirement Specification


## Introduction 

### 1.1. Purpose
Define the reason(s) for which the system is being developed or modified.

### 1.2. Scope
Define the scope of the system under consideration by:

a. Identifying the system to be produced by name. 

b. Referring to and stating the results of the earlier finalized needs analysis, in the form of a brief but clear expression of the user's problem(s). It explains what the system will and will not do to satisfy those needs.

c. Describing the application of the system being specified. As a portion of this, it should describe all relevant top level benefits, objectives, and goals as precisely as possible.

## Overview
### 2.1. System Context
Describe at a general level the major elements of the system, to include human elements, and how they interact. The system overview includes appropriate diagrams and narrative to provide the context of the system, defining all significant interfaces crossing the system's boundaries. 


### 2.2. System functions
Describe major system capabilities, conditions and constraints. 


### 2.3. User characteristics
Identify each type of user/operator/maintainer of the system (by function, location, type of device), the number in each group, and the nature of their use of the system.

## 3. Functional Requirements
Define functional requirements applicable to system operation.

## 4. Usability Requirements
Define usability (quality in use) requirements. Usability requirements and objectives for the system include measurable effectiveness, efficiency, and satisfaction criteria in specific contexts of use.

## 5. Performance Requirements
Define the critical performance conditions and their associated capabilities by including such considerations as

a. Dynamic actions or changes that occur (e.g., rates, velocities, movements, and noise levels).

b. Quantitative criteria covering endurance capabilities of the equipment required to meet the user needs under stipulated environmental and other conditions, including minimum total life expectancy. Indicate required operational session duration and planned utilization rate.

c. Performance requirements for the operational phases and modes.

## 6. System Interfaces
Specify requirements for interfaces among system elements and with external entities. Interfaces among system elements should include interfaces with the human element. Interfaces with external entities should include other systems.

Define any interdependencies or constraints associated with the interfaces (e.g., communication protocols, special devices, standards, fixed formats). Each interface may represent a bidirectional flow of information.

A graphic representation of the interfaces can be used when appropriate for the sake of clarity.

## 7. System Operations
### 7.1. Human system integration requirements
Reference applicable documents and specify any special or unique requirements, e.g., constraints on allocation of functions to personnel and communications and personnel/equipment interactions.
Define any specific areas, stations, or equipment that would require concentrated human engineering attention due to the sensitivity of the operation or criticality of the task (i.e., those areas where the effects of human error would be particularly serious). 


### 7.2. Maintainability
Specify the quantitative maintainability requirements that apply to maintenance in the planned maintenance and support environment. Examples are as follows:

a. Time (e.g., mean and maximum downtime, reaction time, turnaround time, mean and maximum times to repair, mean time between maintenance actions)

b. Rate (e.g., maintenance staff hours per specific maintenance action, operational ready rate, maintenance time per operating hour, frequency of preventative maintenance)

c. Maintenance complexity (e.g., number of people and skill levels, variety of support equipment, removing/replacing/repairing components)

d. Maintenance action indices (e.g., maintenance costs per operating hour, staff hours per overhaul)

e. Accessibility to components within systems and to parts within components


### 7.3. Reliability

Specify the system reliability requirements in quantitative terms, including the conditions under which the reliability requirements are to be met. This may also include the reliability apportionment model to support allocation of reliability values assigned to system functions for their share in achieving desired system reliability.

## 8. System modes and states
If the system can exist in various modes or states define these and, as appropriate, use diagrams. 


### 8.1. Physical requirements
Include constraints on weight, volume and dimension. 

Include the construction characteristics of where the system will be installed, requirements for materials to be used in the item or service covered by this specification, and requirements covering nameplates and system markings, interchangeability of equipment, and workmanship. 


### 8.2. Adaptability requirements
Define requirements for growth, expansion, capability, and contraction. For example, if the system will require future network bandwidth, the applicable hardware should be specified with extra card slots to accommodate new network cards as demand increases. 

### 8.3. Environmental conditions.
Include environmental conditions to be encountered by the system. The following areas should be addressed: natural environment (e.g., wind, rain, temperature, flora, fauna, fungus, mold, sand, salt spray, dust, radiation, chemical, and immersion); induced environment (e.g., motion, shock, noise, electromagnetic, thermal); electromagnetic signal environment; self-induced environment (e.g., motion, shock, noise, electromagnetic, thermal); threat; and cooperative environment. Consideration should also be given to legal/regulatory, political, economic, social, and business environment. 

### 8.4. System security
Define the system security requirements related to both the facility that houses the system and operational security requirements of the system itself. 

One example of security requirements might be to specify the security and privacy requirements, including access limitations to the system, such as existence of log-on procedures and passwords, and of data protection and recovery methods. This could include the factors that would protect the system from accidental or malicious access, use, modification, destruction, or disclosure. Especially in safety-critical embedded systems this might incorporate a distributed log or history of data sets, the assignment of certain functions to different single systems, or the restriction of communications between some areas of the system.


### 8.5. Information management (Optional)
Define the requirements for the system's management of information that it receives, generates, or exports.
Examples include types and amounts of information the system is required to receive and store, any proprietary or other protections levied on the information the system deals with, and what backup and archiving requirements exist for the information. 


### 8.6. Policies and regulations (Optional)
Detail any relevant organizational policies that will affect the operation or performance of the system as well as any relevant external regulatory requirements, or constraints imposed by normal business practices.
Examples of requirements include multilingual support, labour policies, protection of personnel information, and reports to a regulatory agency.

Specify health and safety criteria, including those basic to the design of the system, with respect to equipment characteristics, methods of operation, and environmental influences such as toxic systems and electromagnetic radiation.

### 8.7. System life cycle sustainment (Optional)
Outline quality activities, such as review, and measurement collection and analysis, to help realize a quality system. 

Life cycle sustainment also includes provision of facilities needed to provide operational- and depotlevel support, spares, sourcing and supply, provisioning, technical documentation and data, support-personnel training, initial cadre training and initial contractor-logistics support. 

### 8.8 Packaging, handling, shipping and transportation (Optional)
Define requirements imposed on the system to ensure that it can be packaged, handled, shipped and transported within its intended operational context.

## 9. Verification
Provide the verification approaches and methods planned to qualify the system or system element.

## 10. Assumption and dependencies
List any assumptions and dependencies applicable to the system requirements that should be taken into account in the allocation and derivation of lower-level system requirements