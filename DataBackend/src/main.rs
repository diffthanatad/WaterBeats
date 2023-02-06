mod data;
mod model;

use serde::{Deserialize, Serialize};
use tide::prelude::json;

use data::get_latest_records_from_all_sensors_body;

#[async_std::main]
async fn main() -> tide::Result<()> {
    let mut app = tide::new();
    app.at("/sensors/allLatest")
        .get(get_latest_records_from_all_sensors_api);
    app.at("/sensors/getLatestById")
        .get(get_latest_record_by_id);
    app.at("/debug/create").get(debug_create_sample_data_api);
    app.listen("127.0.0.1:8080").await?;
    Ok(())
}

#[derive(Debug, Serialize)]
struct ApiResponse<T> {
    pub error: i32,
    pub message: Option<String>,
    pub data: Option<T>,
}

async fn get_latest_records_from_all_sensors_api(_req: tide::Request<()>) -> tide::Result {
    let sensor_data_list = get_latest_records_from_all_sensors_body().await?;
    Ok(json!(ApiResponse {
        error: 0,
        message: None,
        data: Some(sensor_data_list),
    })
    .into())
}

#[derive(Debug, Deserialize)]
struct SensorIdQuery {
    id: String,
}

async fn get_latest_record_by_id(req: tide::Request<()>) -> tide::Result {
    let id: Result<SensorIdQuery, tide::Error> = req.query();
    // let id: SensorIdQuery = req.query()?;
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
    println!("id: {:?}", id);
    let data_res = data::get_latest_record_by_id(&id.id).await;
    println!("get_latest_record_by_id: {:?}", data_res);
    if let Err(e) = data_res {
        return Ok(tide::Response::builder(500)
            .body(json!(ApiResponse::<()> {
                error: 1,
                message: Some(format!("read error: {:?}", e)),
                data: None,
            }))
            .into());
    }
    Ok(json!(ApiResponse {
        error: 0,
        message: None,
        data: Some(data_res.unwrap()),
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
    // println!("debug_create_sample_data done");
    Ok("OK".into())
}
