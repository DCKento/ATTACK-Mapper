# ATT&CK Mapper
A webapp tool designed to help organizations map their current security controls and posture against the Mitre ATT&amp;CK framework.

## Description
The ATT&CK Mapper tool is designed to help organizations map their current security controls and posture against the Mitre ATT&CK framework. The tool provides an interactive graphical representation of the Mitre ATT&CK framework, allowing users to input and visualize controls for each technique and sub-technique, and assess the effectiveness of these controls through colour-coded indicators.

## Purpose
The primary purpose of this tool is to enable organizations to:

 - Visualize their security posture
 - Identify gaps in their security controls
 - Plan and prioritize future security improvements.

## Technical Details
Front-end: HTML, CSS, JavaScript
Back-end: Python (Flask)
Data Storage: Browser memory (LocalStorage), JSON for export/import
Deployment: On-premises
Architecture: Monolithic
Communication: To be determined (consider RESTful API)
Colour-coding: Red, Orange, Green to indicate control effectiveness

## Requirements
### Functional Requirements
Mapping Controls:

 - Users can input controls (people, process, technology) for each technique
 - Manual input through text boxes
 - Option to upload screenshots
 - Ability to change the colour/rating (Red, Orange, Green) for each technique.

Graphical Representation:

 - Flat tree structure with techniques horizontally across the top and sub-techniques vertically
 - Sub-techniques will be lightly colored to indicate control effectiveness.

Reporting:

 - Export data in JSON and CSV formats.

Non-functional Requirements
 - Scalability: Single concurrent user.
 - Performance: No specific benchmarks.

## Implementation Plan
### Set Up Development Environment:

 1. Install Python and necessary libraries (Flask)
 2. Set up HTML, CSS, and JavaScript for the front-end.

### Develop Front-end:

 1. Create the graphical representation of the Mitre ATT&CK framework.
 2. Implement user interaction features for inputting controls and changing colors.

### Develop Back-end:

 1. Set up Flask server
 2. Implement RESTful API (if needed) for communication between front-end and back-end.

### Implement Data Management:

 1. Use LocalStorage for temporary data storage.
 2. Develop functionality for exporting and importing data in JSON and CSV formats.

### Testing and Iteration:

 1. Test the MVP for functionality and usability
 2. Iterate based on feedback.

## Next Steps

 1. Define the Mitre ATT&CK framework structure in JSON format.
 2. Set up the development environment.
 3. Develop the front-end and back-end components.
 4. Implement data management and reporting features.
 5. Test the MVP and gather initial feedback.
 6. Plan for future enhancements (authentication, user roles, database, security features).
