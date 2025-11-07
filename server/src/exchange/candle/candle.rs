use crate::exchange::candle::{indicator::Indicator, ohlcv_candle::OhlcvCandle};
use litemap::LiteMap;
use polars::{frame::DataFrame, prelude::NamedFrom, series::Series};

pub struct Candle {
    pub ohlcv: OhlcvCandle,
    indicators: LiteMap<Indicator,f32>,
}

impl Candle {

    pub fn get_indicator(&self, indicator: &Indicator) -> f32 {
        
        if let Some(val) = self.indicators.get(indicator) {
            return *val;
        }
        
        panic!(
            "Indicator {:?} not found in {:?}",
            indicator, self.indicators
        )
    }
}

impl Candle {

    pub fn as_dataframe(&self) -> DataFrame {

        let mut indicators = Vec::with_capacity(self.indicators.len());
        for (indicator, value) in self.indicators.iter() {
            let name = indicator.to_string();
            let series = Series::new(&name, &[*value]);

            indicators.push(series);
        }

        let ohlcv_frame = self.ohlcv.as_dataframe();
        ohlcv_frame.hstack(indicators.as_slice()).unwrap()
    }

}
