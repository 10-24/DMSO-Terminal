use axum::{response::IntoResponse, routing::get, Router};
use ta::DataItem;
use tower_http::{services::ServeDir, trace::TraceLayer};
mod broadcast;
mod exchange;
mod helpers;

// Type aliases for cleaner naming
type Candle = DataItem;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    // Build the router
    let app = Router::new()
        .route("/api/hello", get(hello))
        .fallback_service(ServeDir::new("../dist")) // Serve static files
        .layer(TraceLayer::new_for_http());

    let addr = std::net::SocketAddr::from(([0, 0, 0, 0], 8080));

    tracing::info!("🚀 Server listening on http://{}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn hello() -> impl IntoResponse {
    "hello from server!"
}
// Example struct for working with candle data
pub struct Candles {
    pub ticker: Box<str>,
    pub candles: Vec<Candle>,
}
