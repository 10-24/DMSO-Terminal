use std::{
    rc::Rc,
    sync::{Arc, RwLock},
};

use litemap::LiteMap;

pub struct BroadcastNode {
    children: ChildrenRcs<TickerId, TickerNode>,
}

impl BroadcastNode {
    pub fn subscribe(
        &mut self,
        ticker: &TickerId,
        interval: &IntervalId,
        indicators: Vec<crate::exchange::candle::indicator::Indicator>,
    ) -> Result<Subscription, String> {
        // Now you can access self.children here
        todo!()
    }
}

struct TickerNode {
    parent: ParentRef<BroadcastNode>,
    children: ChildrenRcs<IntervalId, IntervalNode>,
}

struct IntervalNode {
    parent: ParentRef<TickerNode>,
    children: ChildrenRcs<IndicatorId, IndicatorNode>,
}

struct IndicatorNode {
    parent: ParentRef<IntervalNode>,
}

pub struct Subscription {
    parents: Box<[Arc<Parent<IndicatorNode>>]>,
}

type Parent<PType> = RwLock<PType>;
type ParentRef<PType> = Rc<Parent<PType>>;

type Child<CType> = RwLock<CType>;
type ChildrenRcs<CId, CType> = LiteMap<Box<CId>, Rc<Child<CType>>>;

pub type ExchangeId = str;
pub type TickerId = str;
pub type IntervalId = u32;
pub type IndicatorId = str;
