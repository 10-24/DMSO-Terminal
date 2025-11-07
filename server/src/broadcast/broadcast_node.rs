use std::{
    rc::Rc,
    sync::{Arc, RwLock},
};

use litemap::LiteMap;

use crate::broadcast::hierarchy::{
    Broadcast, IndicatorNode, IntervalId, IntervalNode, Subscription, TickerId, TickerNode,
};
use crate::exchange::candle::indicator::Indicator;

impl Broadcast {
    pub fn subscribe(
        &mut self,
        ticker_id: Box<TickerId>,
        interval_id: IntervalId,
        indicators: Box<[Indicator]>,
    ) -> Result<Subscription, String> {
        // Create and register ticker node
        let ticker_node = Rc::new(RwLock::new(TickerNode {
            children: LiteMap::default(),
        }));
        self.tickers.insert(ticker_id, Rc::downgrade(&ticker_node));

        // Create and register interval node
        let interval_node = Rc::new(RwLock::new(IntervalNode {
            parent: ticker_node.clone(),
            children: LiteMap::default(),
        }));
        ticker_node
            .write()
            .unwrap()
            .children
            .insert(interval_id, Rc::downgrade(&interval_node));


        // Create and register indicator nodes
        let indicator_nodes =
            indicators
                .iter()
                .map(|indicator| {
                    Arc::new(RwLock::new(IndicatorNode {
                        parent: interval_node.clone(),
                    }))
                })
                .collect();
        
        let subscription = Subscription {
            indicators: indicator_nodes,
        };
        let indicator_nodes_map = LiteMap::from_iter(iter)
        let interval_guard = interval_node.write().unwrap();
            
        

        Ok()
    }
}
