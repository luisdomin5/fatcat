#[macro_use]
extern crate fatcat_api;
extern crate chrono;
#[macro_use] extern crate diesel;
extern crate iron_diesel_middleware;
extern crate dotenv;
extern crate futures;
#[macro_use] extern crate hyper;
extern crate swagger;
#[macro_use] extern crate error_chain;
extern crate iron;
extern crate r2d2;
extern crate r2d2_diesel;

pub mod database_schema;
pub mod api_server;

mod errors {
    error_chain!{}
}

pub use self::errors::*;
use diesel::pg::PgConnection;
use diesel::prelude::*;
use dotenv::dotenv;
use std::env;
use iron::{Request, Response};
use iron::middleware::AfterMiddleware;
use r2d2_diesel::ConnectionManager;

pub type ConnectionPool = r2d2::Pool<r2d2_diesel::ConnectionManager<diesel::pg::PgConnection>>;

pub fn establish_connection() -> PgConnection {
    dotenv().ok();

    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    PgConnection::establish(&database_url).expect(&format!("Error connecting to {}", database_url))
}

/// Instantiate a new server.
pub fn server() -> Result<api_server::Server> {
    dotenv().ok();
    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    let manager = ConnectionManager::<PgConnection>::new(database_url);
    let pool = r2d2::Pool::builder().build(manager).expect("Failed to create database pool.");
    Ok(api_server::Server {
        db_pool: pool,
    })
}

/// HTTP header middleware
header! { (XClacksOverhead, "X-Clacks-Overhead") => [String] }

pub struct XClacksOverheadMiddleware;

impl AfterMiddleware for XClacksOverheadMiddleware {
    fn after(&self, _req: &mut Request, mut res: Response) -> iron::IronResult<Response> {
        res.headers.set(XClacksOverhead("GNU aaronsw, jpb".to_owned()));
        Ok(res)
    }
}
