# Base Station

This branch contains the full base station functionality.

## Features

- stream processing using Faust
- sensor and actuator event management
- sensor and actuator interfaces for Faust
- sensor and actuator firmware for ESP32
- local database and cloud database connections

## Prerequisites
Download the latest stable Apache Kafka (3.4.0) binary for Scala 2.13 from https://kafka.apache.org/downloads.

Extract to the root directory (e.g., C:\ on Windows) and rename the directory to kafka.

## Quick Start

### Start zookeeper and kafka, then start a Faust worker
On Windows: `start_kafka.bat` then `start_faust.bat`

On MacOS: `start_kafka.sh` then `start_faust.sh`
