use chrono::Utc;
use futures::stream;
use influxdb2::models::{DataPoint, Query};
use influxdb2::{Client, RequestError};

use super::model;

pub async fn get_latest_records_from_all_sensors_body(
) -> Result<Vec<model::SensorData>, RequestError> {
    let client = get_influxdb_client();
    let bucket = get_default_bucket();
    let qs = format!(
        "from(bucket: \"{}\")
        |> range(start: 0)
        |> filter(fn: (r) => r._measurement == \"sensor_data\")
        |> last()",
        bucket
    );
    let query = Query::new(qs.to_string());
    let res = client
        .query::<model::SensorData>(Some(query))
        .await
        .map_err(|e| e)?;
    Ok(res)
}

pub async fn get_latest_record_by_sensor_id(
    id: &str,
) -> Result<Option<model::SensorData>, RequestError> {
    let client = get_influxdb_client();
    let bucket = get_default_bucket();
    let qs = format!(
        "from(bucket: \"{}\")
        |> range(start: 0)
        |> filter(fn: (r) => r._measurement == \"sensor_data\")
        |> filter(fn: (r) => r.sensor_id == \"{}\" )
        |> last()",
        bucket, id
    );
    let query = Query::new(qs.to_string());
    let res = client.query::<model::SensorData>(Some(query)).await?;
    if res.len() == 0 {
        return Ok(None);
    }
    Ok(Some(res[0].to_owned()))
}

pub async fn get_records_by_sensor_id_and_range(
    id: &str,
    start: i64,
    end: i64,
) -> Result<Vec<model::SensorData>, RequestError> {
    let client = get_influxdb_client();
    let bucket = get_default_bucket();
    let qs = format!(
        "from(bucket: \"{}\")
        |> range(start: {}, stop: {})
        |> filter(fn: (r) => r._measurement == \"sensor_data\")
        |> filter(fn: (r) => r.sensor_id == \"{}\" )",
        bucket, start, end, id
    );
    let query = Query::new(qs.to_string());
    let res = client.query::<model::SensorData>(Some(query)).await?;
    println!("{:?}", &res);
    Ok(res)
}

async fn get_all_latest_actuator_data() -> Result<Vec<model::ActuatorData>, RequestError> {
    let client = get_influxdb_client();
    let bucket = get_default_bucket();
    let qs = format!(
        "from(bucket: \"{}\")
        |> range(start: 0)
        |> filter(fn: (r) => r._measurement == \"actuator_data\")
        |> last()",
        bucket
    );
    let query = Query::new(qs.to_string());
    let res = client.query::<model::ActuatorData>(Some(query)).await?;
    Ok(res)
}

pub async fn get_all_latest_devices_data() -> Result<Vec<model::DeviceData>, RequestError> {
    let sensor_data = get_latest_records_from_all_sensors_body().await?;
    let actuator_data = get_all_latest_actuator_data().await?;
    let res: Vec<model::DeviceData> = sensor_data
        .into_iter()
        .map(|e| e.into())
        .chain(actuator_data.into_iter().map(|e| e.into()))
        .collect();
    Ok(res)
}

pub async fn get_latest_actuators_by_type(
    typ: &str,
) -> Result<Vec<model::ActuatorData>, RequestError> {
    let client = get_influxdb_client();
    let bucket = get_default_bucket();
    let qs = format!(
        "from(bucket: \"{}\")
        |> range(start: 0)
        |> filter(fn: (r) => r._measurement == \"actuator_data\")
        |> filter(fn: (r) => r.actuator_type == \"{}\" )
        |> last()",
        bucket, typ
    );
    let query = Query::new(qs.to_string());
    let res = client.query::<model::ActuatorData>(Some(query)).await;
    res
}

pub async fn debug_create_sample_data() -> Result<(), tide::Error> {
    let client = get_influxdb_client();
    let bucket = get_default_bucket();

    println!("debug_create_sample_data");
    let points = vec![DataPoint::builder("sensor_data")
        .tag("sensor_id", "sensor_test_1")
        .tag("sensor_type", "soil_moisture")
        .field("data", 89.0)
        .field("unit", "percent")
        .field("longitude", 31.0)
        .field("latitude", 121.8)
        .timestamp(Utc::now().timestamp_nanos())
        .build()?];

    let res = client
        .write(&bucket, stream::iter(points))
        .await
        .map_err(|e| e.into());
    return res;
}
fn get_influxdb_client() -> Client {
    let host = std::env::var("INFLUXDB_HOST").unwrap_or("http://localhost:8086".to_string());
    let org = std::env::var("INFLUXDB_ORG").unwrap_or("WaterBeats".to_string());
    let token = std::env::var("INFLUXDB_TOKEN").unwrap_or("".to_string());
    let client = Client::new(&host, &org, &token);
    client
}

fn get_default_bucket() -> String {
    std::env::var("INFLUXDB_BUCKET").unwrap_or("WaterBeats".to_string())
}

mod test {
    #[async_std::test]
    async fn test_get_latest_record_by_id() {
        let id = "test_sensor_1";
        let res = super::get_latest_record_by_sensor_id(id).await;
        assert!(res.is_ok(), "{:?}", res);
        let data = res.unwrap().unwrap();
        assert_eq!(data.sensor_id, id);
        assert_eq!(data.sensor_type, "temperature");
    }

    #[async_std::test]
    async fn test_get_lastest_record_for_all() {
        let res = super::get_latest_records_from_all_sensors_body().await;
        assert!(res.is_ok());
        let data = res.unwrap();
        assert!(data.len() > 0);
    }

    #[async_std::test]
    async fn test_get_sprinkler_data() {
        let res = super::get_latest_actuators_by_type("sprinkler").await;
        assert!(res.is_ok());
        let data = res.unwrap();
        assert!(data.len() == 1);
        let res = super::get_latest_actuators_by_type("transformer").await;
        assert!(res.is_ok());
        assert!(
            res.unwrap().len() == 0,
            "expected 0, got a Vec of {:?}",
            data
        );
    }
}
