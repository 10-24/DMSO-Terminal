use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum Interval {
    Second1 = 1_000,
    Second5 = 5_000,
    Second15 = 15_000,
    Second30 = 30_000,
    Minute1 = 60_000,
    Minute5 = 300_000,
    Minute15 = 900_000,
    Minute30 = 1_800_000,
    Hour1 = 3_600_000,
    Hour4 = 14_400_000,
    Day1 = 86_400_000,
}

impl Interval {
    pub fn as_ms(self) -> u32 {
        self as u32
    }
}

impl fmt::Display for Interval {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Interval::Second1 => write!(f, "1s"),
            Interval::Second5 => write!(f, "5s"),
            Interval::Second15 => write!(f, "15s"),
            Interval::Second30 => write!(f, "30s"),
            Interval::Minute1 => write!(f, "1m"),
            Interval::Minute5 => write!(f, "5m"),
            Interval::Minute15 => write!(f, "15m"),
            Interval::Minute30 => write!(f, "30m"),
            Interval::Hour1 => write!(f, "1h"),
            Interval::Hour4 => write!(f, "4h"),
            Interval::Day1 => write!(f, "1d"),
        }
    }
}