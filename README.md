Digianalix Plant Growth Monitoring System (DPMS) for Hydroponics and Aquaponics
A Python-based real-time monitoring system for hydroponic and aquaponic environments with dual dashboards and external data integration capabilities.

<img width="1675" height="1389" alt="Screenshot from 2025-08-25 10-39-23" src="https://github.com/user-attachments/assets/90ae49ed-b705-4640-8d69-81e3b35515e6" />

🌱 Overview

This system provides a comprehensive solution for monitoring plant growth conditions in both hydroponic and aquaponic systems. It features:

    Real-time data visualization for critical environmental parameters

    Dual dashboard interface with specialized views for hydroponics and aquaponics

    External device integration allowing WiFi-connected sensors to submit data

    Historical data tracking and trend analysis

    Device management for connected sensors and data sources

<img width="3747" height="1259" alt="Screenshot from 2025-08-25 10-40-38" src="https://github.com/user-attachments/assets/58ee39f7-55b6-4138-8896-4e9ea6d7bfec" />

<img width="3755" height="1628" alt="Screenshot from 2025-08-25 10-41-14" src="https://github.com/user-attachments/assets/f05fd4be-b27c-43ed-81d5-24ada31f4805" />

✨ Features
Monitoring Capabilities

    Hydroponics Dashboard: pH, temperature, humidity, water level, light intensity, electrical conductivity (EC)

    Aquaponics Dashboard: pH, temperature, humidity, water level, dissolved oxygen, ammonia, nitrate levels

    Real-time charts with configurable scales and automatic updates

    Data source tracking to distinguish between internal and external sensors

External Integration

    RESTful API endpoints for data submission from external devices

    Device registration and management system

    Automatic device status monitoring (online/offline detection)

    Flexible data format supporting various sensor types

Technical Features

    Flask-based web application with responsive design

    SQLite database for data storage (easily configurable for other databases)

    Chart.js integration for beautiful, interactive data visualization

    Threaded data collection for non-blocking operation

🚀 Getting Started
Prerequisites

    Python 3.7+

    pip (Python package manager)


1. Installation

    Clone the repository:

bash cmd/ linux terminal

git clone https://github.com/yourusername/plant-growth-monitoring-system.git
cd plant-growth-monitoring-system

  2. Install required dependencies:

bash cmd/ linux terminal

pip install -r requirements.txt

  3. Run the application:

bash cmd/ linux terminal

python app.py


**Configuration**

The system can be customized through several aspects:

    Database: Modify init_db() in app.py to use different database systems

    Data Collection Interval: Adjust the time.sleep() value in collect_internal_sensor_data()

    Chart Parameters: Modify the chart configuration in the HTML templates

    Device Timeout: Change the online/offline threshold in devices.html




**  Development**
Adding New Sensor Types

    Extend the database schema in init_db()

    Add new API endpoints for data接收

    Update the appropriate dashboard template to display the new data

    Modify the data collection functions to handle the new parameters

Customizing Dashboards

The chart configuration in the HTML templates can be modified to:

    Change chart types (line, bar, etc.)

    Adjust visual styling and colors

    Modify data ranges and scales

    Add new data visualizations

**🌐 Deployment**

For production deployment, consider:

    Using a production WSGI server (e.g., Gunicorn)

    Setting up a reverse proxy (e.g., Nginx)

    Implementing HTTPS encryption

    Using a more robust database (PostgreSQL, MySQL)

    Adding authentication and authorization

    Setting up proper logging and monitoring


**    Acknowledgments**

    Built with Flask

    Charts powered by Chart.js

    Example client using Requests


    📞 Support

This project is licensed under the MIT License.

For any issues or suggestions, please reach out to:

    Author: Dr Mukesh nitin
    Email: drrmukeshnitin@gmail.com
    https://github.com/drmukeshnitin/Digianalix-Plant-monitoring-system-DPMS-/tree/main
