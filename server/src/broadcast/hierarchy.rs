use litemap::LiteMap;
use std::{
    rc::{self, Rc, Weak},
    sync::{self, Arc, RwLock},
};

use crate::exchange::candle::indicator::Indicator;

#[derive(Debug)]
pub struct Broadcast {
    tickers: LiteMap<Box<TickerId>,rc::Weak<RwLock<TickerNode>>>,
}

#[derive(Debug)]
struct TickerNode {
    children: LiteMap<IntervalId,rc::Weak<RwLock<IntervalNode>>>,
}
#[derive(Debug)]
struct IntervalNode {
    parent: ParentRef<TickerNode>,
    children: LiteMap<Indicator,sync::Weak<RwLock<IndicatorNode>>>,
}
#[derive(Debug)]
struct IndicatorNode {
    parent: ParentRef<IntervalNode>,
}
#[derive(Debug)]
pub struct Subscription {
    indicators: Box<[Arc<Parent<IndicatorNode>>]>,
}

type Parent<PType> = RwLock<PType>;
type ParentRef<PType> = Rc<Parent<PType>>;




pub type ExchangeId = str;
pub type TickerId = str;
pub type IntervalId = u32;


#[path = "broadcast_node.rs"]
mod broadcast_node;
