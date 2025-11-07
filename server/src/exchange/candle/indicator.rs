use std::fmt;

use crate::helpers::interval::Interval;

#[derive(PartialEq, Eq, Debug,PartialOrd, Ord,Clone, Copy)]
pub enum Indicator {
    Average,
    Ema(Interval),
    Sma(Interval),
}

impl fmt::Display for Indicator {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Indicator::Average => write!(f, "Average"),
            Indicator::Ema(i) => write!(f, "EMA({:})", i),
            Indicator::Sma(i) => write!(f, "SMA({:})", i),
        }
    }
}
