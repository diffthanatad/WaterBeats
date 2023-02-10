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

pub async fn get_latest_record_by_id(id: &str) -> Result<model::SensorData, RequestError> {
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
    println!("{:?}", &res);
    Ok(res[0].to_owned())
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
        let res = super::get_latest_record_by_id(id).await;
        assert!(res.is_ok(), "{:?}", res);
        let data = res.unwrap();
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
}
