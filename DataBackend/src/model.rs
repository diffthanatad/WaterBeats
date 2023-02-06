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
    longitude: f64,
    latitude: f64,
}
