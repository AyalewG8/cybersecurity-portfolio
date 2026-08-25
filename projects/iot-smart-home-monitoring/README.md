# Project 06 — IoT Smart Home Monitoring System

## Sensor-Based Monitoring with MQTT and Raspberry Pi

### Objective
Design a prototype smart-home monitoring system using IoT sensors for temperature, humidity, and air quality with a Raspberry Pi and cloud dashboard for real-time and historical analysis.

### My Role
Designed the system concept, identified hardware and software components, and focused on reliable telemetry, dashboard visibility, secure communication, and resilience.

## Architecture & Approach

- Raspberry Pi 4B
- DHT22 temperature and humidity sensor
- MQ135 air-quality sensor
- MQTT publish/subscribe communication
- TLS-protected transport to a cloud broker
- AWS IoT Core / Blynk concepts
- Time-series database for historical trending
- Web/mobile dashboard
- Threshold-based email, SMS, or push alerts
- Local buffering for temporary network loss

## Monitoring Data Flow

```text
Sensors
Temp / Humidity / Air
        |
        v
Raspberry Pi
Collect + Buffer
        |
        v
MQTT over TLS
        |
        v
Cloud Broker
   |          |
   v          v
Time-Series   Dashboard
Database      Charts + Status
                 |
                 v
               Alerts
         Email / SMS / Push
```

## Performance Targets

- 95% sensor reading accuracy target
- Dashboard refresh every 10 seconds
- 95%+ system uptime target
- Threshold-based alerts
- TLS + token authentication

## Deliverables

- Prototype collecting data at 10-second intervals
- Dashboard for current readings and trends
- Historical trending target of 30 days
- Threshold alert concept
- Deployment guidance

## Security & Reliability Considerations

- MQTT is appropriate for low-bandwidth IoT environments
- TLS protects telemetry in transit
- Token authentication helps protect access to services
- Sensor calibration is necessary before raw readings can drive reliable alerts
- Offline buffering improves resilience during network interruptions

## Key Learning
IoT systems combine hardware, software, networking, cloud services, and security. Reliable monitoring depends on both secure communication and operational resilience.

## Career Relevance
This project demonstrates systems thinking, telemetry awareness, secure communication concepts, dashboard monitoring, and the ability to design around availability and reliability requirements.

---

**Presentation alignment:** Project 06 in my 2026 IT / Cybersecurity Portfolio presentation.
