use chrono::DateTime;
use chrono::FixedOffset;
use influxdb2::FromDataPoint;
use serde::Serialize;

#[derive(Debug, FromDataPoint, Default, Serialize, Clone)]
pub struct SensorData {
    time: DateTime<FixedOffset>,
    sensor_id: String,
    sensor_type: String,
    data: f64,
    unit: String,
    longitude: f64,
    latitude: f64,
}

/// The data structure of sensor data returned by the API
#[derive(Debug, Serialize, Clone)]
pub struct SensorDataExternal {
    time: DateTime<FixedOffset>,
    sensor_id: String,
    sensor_type: String,
    data: f64,
    unit: String,
    /// the location of the sensor, in the format of (longitude, latitude)
    location: (f64, f64),
}

impl Into<SensorDataExternal> for SensorData {
    fn into(self) -> SensorDataExternal {
        SensorDataExternal {
            time: self.time,
            sensor_id: self.sensor_id,
            sensor_type: self.sensor_type,
            data: self.data,
            unit: self.unit,
            location: (self.longitude, self.latitude),
        }
    }
}
