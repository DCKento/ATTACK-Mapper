# ATT&CK Mapper
A webapp tool designed to help organizations map their current security controls and posture against the Mitre ATT&amp;CK framework.

## Description
The ATT&CK Mapper tool is designed to help organizations map their current security controls and posture against the Mitre ATT&CK framework. The tool provides an interactive graphical representation of the Mitre ATT&CK framework, allowing users to input and visualize controls for each technique and sub-technique, and assess the effectiveness of these controls through colour-coded indicators.

## Purpose
The primary purpose of this tool is to enable organizations to:

Visualize their security posture.

Identify gaps in their security controls.

Plan and prioritize future security improvements.

## Technical Details
Front-end: HTML, CSS, JavaScript

Back-end: Python (Flask or Django)

Data Storage: Browser memory (LocalStorage), JSON for export/import

Deployment: On-premises

Architecture: Monolithic

Communication: To be determined (consider RESTful API if using Flask or Django)

Colour-coding: Red, Orange, Green to indicate control effectiveness

## Requirements
### Functional Requirements
Mapping Controls:

Users can input controls (people, process, technology) for each technique.

Manual input through text boxes.

Option to upload screenshots.

Ability to change the color/rating (Red, Orange, Green) for each technique.

Graphical Representation:

Flat tree structure with techniques horizontally across the top and sub-techniques vertically.

Sub-techniques will be lightly colored to indicate control effectiveness.

Reporting:

Export data in JSON and CSV formats.

Non-functional Requirements

Scalability: Single concurrent user.

Performance: No specific benchmarks.

## Implementation Plan
### Set Up Development Environment:

Install Python and necessary libraries (Flask/Django).
Set up HTML, CSS, and JavaScript for the front-end.

### Develop Front-end:

Create the graphical representation of the Mitre ATT&CK framework.

Implement user interaction features for inputting controls and changing colors.

### Develop Back-end:

Set up Flask/Django server.

Implement RESTful API (if needed) for communication between front-end and back-end.

### Implement Data Management:

Use LocalStorage for temporary data storage.

Develop functionality for exporting and importing data in JSON and CSV formats.

### Testing and Iteration:

Test the MVP for functionality and usability.

Iterate based on feedback.

## Next Steps
Define the Mitre ATT&CK framework structure in JSON format.

Set up the development environment.

Develop the front-end and back-end components.

Implement data management and reporting features.

Test the MVP and gather initial feedback.

Plan for future enhancements (authentication, user roles, database, security features).
