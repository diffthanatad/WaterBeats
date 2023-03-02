mod data;
mod model;

use chrono::{DateTime, FixedOffset};
use model::DeviceDataExternal;
use serde::{Deserialize, Serialize};
use tide::prelude::json;

use data::get_latest_records_from_all_sensors_body;

use crate::model::SensorDataExternal;

#[async_std::main]
async fn main() -> tide::Result<()> {
    env_logger::init();

    let listen_addr = std::env::var("WB_ADDRESS").unwrap_or("localhost:8080".to_string());
    let mut app = tide::new();

    let cors = tide::security::CorsMiddleware::new()
        .allow_methods(
            "GET, POST, OPTIONS"
                .parse::<tide::http::headers::HeaderValue>()
                .unwrap(),
        )
        .allow_origin(tide::security::Origin::from("*"));

    app.with(cors);
    app.with(tide::log::LogMiddleware::new());

    app.at("/sensor/allLatest")
        .get(get_latest_records_from_all_sensors_api);
    app.at("/sensor/getLatestById").get(get_latest_record_by_id);
    app.at("/sensor/record").get(get_range_data_by_sensor_id);
    app.at("/device/latest").get(get_all_latest_devices_record);
    app.at("/actuator/latestByType").get(get_actuators_by_type);
    app.at("/debug/create").get(debug_create_sample_data_api);
    app.listen(&listen_addr).await?;
    Ok(())
}

#[derive(Debug, Serialize)]
struct ApiResponse<T> {
    pub error: i32,
    pub message: Option<String>,
    pub data: Option<T>,
}

async fn get_latest_records_from_all_sensors_api(_req: tide::Request<()>) -> tide::Result {
    let sensor_data_list = get_latest_records_from_all_sensors_body().await;
    if let Err(e) = sensor_data_list {
        return Ok(tide::Response::builder(500)
            .body(json!(ApiResponse::<()> {
                error: 1,
                message: Some(format!("failed to get data from DB: {:?}", e)),
                data: None,
            }))
            .into());
    }
    let sensor_data_list = sensor_data_list.unwrap();
    Ok(json!(ApiResponse::<Vec<SensorDataExternal>> {
        error: 0,
        message: None,
        data: Some(sensor_data_list.into_iter().map(|e| e.into()).collect()),
    })
    .into())
}

#[derive(Debug, Deserialize)]
struct SensorIdQuery {
    sensor_id: String,
}

async fn get_latest_record_by_id(req: tide::Request<()>) -> tide::Result {
    let id: Result<SensorIdQuery, tide::Error> = req.query();
    if let Err(e) = id {
        println!("id error: {:?}", e);
        println!("{:?}", e.status());
        println!("{:?}", e.type_name());
        return Ok(tide::Response::builder(e.status())
            .body(json!(ApiResponse::<()> {
                error: 1,
                message: Some(format!("read error: {:?}", e)),
                data: None,
            }))
            .into());
    }
    let id = id.unwrap();
    let data_res = data::get_latest_record_by_sensor_id(&id.sensor_id).await;
    if let Err(e) = data_res {
        return Ok(tide::Response::builder(500)
            .body(json!(ApiResponse::<()> {
                error: 1,
                message: Some(format!("failed to get data from DB: {:?}", e)),
                data: None,
            }))
            .into());
    }
    Ok(json!(ApiResponse::<SensorDataExternal> {
        error: 0,
        message: None,
        data: data_res.unwrap().map(|e| e.into()),
    })
    .into())
}

async fn get_all_latest_devices_record(_req: tide::Request<()>) -> tide::Result {
    let data_res = data::get_all_latest_devices_data().await;
    if let Err(e) = data_res {
        println!("{:?}", e);
        return Ok(tide::Response::builder(500)
            .body(json!(ApiResponse::<()> {
                error: 1,
                message: Some(format!("failed to get data from DB: {:?}", e)),
                data: None,
            }))
            .into());
    }
    Ok(json!(ApiResponse::<Vec<DeviceDataExternal>> {
        error: 0,
        message: None,
        data: Some(data_res.unwrap().into_iter().map(|e| e.into()).collect()),
    })
    .into())
}

#[derive(Deserialize)]
struct SensorDataRangeQuery {
    pub id: String,
    pub start: DateTime<FixedOffset>,
    pub end: DateTime<FixedOffset>,
}

async fn get_range_data_by_sensor_id(req: tide::Request<()>) -> tide::Result {
    let q = req.query::<SensorDataRangeQuery>();
    if let Err(e) = q {
        return Ok(tide::Response::builder(500)
            .body(json!(ApiResponse::<()> {
                error: 1,
                message: Some(format!(": {:?}", e)),
                data: None,
            }))
            .into());
    }
    let q = q.unwrap();
    let start_ts = q.start.timestamp();
    let end_ts = q.end.timestamp();
    let data_res = data::get_records_by_sensor_id_and_range(&q.id, start_ts, end_ts).await;
    if let Err(e) = data_res {
        return Ok(tide::Response::builder(500)
            .body(json!(ApiResponse::<()> {
                error: 1,
                message: Some(format!("failed to get data from DB: {:?}", e)),
                data: None,
            }))
            .into());
    }
    Ok(json!(ApiResponse::<Vec<SensorDataExternal>> {
        error: 0,
        message: None,
        data: Some(data_res.unwrap().into_iter().map(|e| e.into()).collect()),
    })
    .into())
}

#[derive(Deserialize)]
struct ActuatorTypeQuery {
    #[serde(rename = "type")]
    pub actuator_type: String,
}

async fn get_actuators_by_type(req: tide::Request<()>) -> tide::Result {
    let query = req.query::<ActuatorTypeQuery>();
    if let Err(e) = query {
        return Ok(tide::Response::builder(500)
            .body(json!(ApiResponse::<()> {
                error: 1,
                message: Some(format!("Error parsing query: {:?}", e)),
                data: None,
            }))
            .into());
    }
    let actuator_type = query.unwrap().actuator_type;
    let data_res = data::get_latest_actuators_by_type(&actuator_type).await;
    if let Err(e) = data_res {
        return Ok(tide::Response::builder(500)
            .body(json!(ApiResponse::<()> {
                error: 1,
                message: Some(format!("failed to get data from DB: {:?}", e)),
                data: None,
            }))
            .into());
    }
    Ok(json!(ApiResponse::<Vec<model::ActuatorDataExternal>> {
        error: 0,
        message: None,
        data: Some(data_res.unwrap().into_iter().map(|e| e.into()).collect()),
    })
    .into())
}

async fn debug_create_sample_data_api(_req: tide::Request<()>) -> tide::Result {
    let res = data::debug_create_sample_data().await;
    if res.is_err() {
        return Ok(tide::Response::builder(500)
            .body(json!(ApiResponse::<()> {
                error: 1,
                message: Some(format!("write error: {:?}", res)),
                data: None,
            }))
            .into());
    }
    Ok("OK".into())
}
