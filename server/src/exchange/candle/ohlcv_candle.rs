use polars::{df, frame::DataFrame, prelude::{DataType, TimeUnit}};

#[derive(Debug, Clone, Copy)]
pub struct OhlcvCandle {
    timestamp: u64,
    open: f32,
    close: f32,
    high: f32,
    low: f32,
    volume: f32,
}

impl OhlcvCandle {
    pub fn as_dataframe(&self) -> DataFrame {
        df!(
            "timestamp" => [self.timestamp],
            "open" => [self.open],
            "close" => [self.close],
            "high" => [self.high],
            "low" => [self.low],
            "volume" => [self.volume],
        )
        .unwrap()
    }
}

pub const OHLCV_POLARS_COLUMNS: [(&str, DataType); 6] = [
    (
        "timestamp",
        DataType::Datetime(TimeUnit::Milliseconds, Option::None),
    ),
    ("open", DataType::Float32),
    ("high", DataType::Float32),
    ("low", DataType::Float32),
    ("close", DataType::Float32),
    ("volume", DataType::Float32),
];