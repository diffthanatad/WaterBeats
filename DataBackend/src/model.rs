use chrono::DateTime;
use chrono::FixedOffset;
use influxdb2::FromDataPoint;
use serde::Serialize;

#[derive(Debug, FromDataPoint, Default, Serialize, Clone)]
pub struct SensorData {
    time: DateTime<FixedOffset>,
    pub sensor_id: String,
    pub sensor_type: String,
    data: f64,
    unit: String,
    longitude: f64,
    latitude: f64,
}

#[derive(Debug, Serialize, Clone)]
pub struct ActuatorData {
    status: String,
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

#[derive(Debug)]
enum DeviceData {
    Sensor(SensorData),
    Actuator,
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

impl Into<DeviceData> for SensorData {
    fn into(self) -> DeviceData {
        DeviceData::Sensor(self)
    }
}

mod test {
    use chrono::DateTime;

    use super::SensorData;
    use super::SensorDataExternal;

    #[test]
    fn test_convert_sensor_data_to_external_struct() {
        let sensor_data = SensorData {
            time: DateTime::parse_from_rfc3339("2020-01-01T00:00:00+00:00").unwrap(),
            sensor_id: "sensor_id".to_string(),
            sensor_type: "sensor_type".to_string(),
            data: 1.0,
            unit: "unit".to_string(),
            longitude: 1.0,
            latitude: -3.0,
        };
        let sensor_data_external: SensorDataExternal = sensor_data.clone().into();
        assert_eq!(sensor_data.time, sensor_data_external.time);
        assert_eq!(sensor_data.sensor_id, sensor_data_external.sensor_id);
        assert_eq!(sensor_data.sensor_type, sensor_data_external.sensor_type);
        assert_eq!(sensor_data.data, sensor_data_external.data);
        assert_eq!(sensor_data.unit, sensor_data_external.unit);
        assert_eq!(sensor_data.longitude, sensor_data_external.location.0);
        assert_eq!(sensor_data.latitude, sensor_data_external.location.1);
    }
}
