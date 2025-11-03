use crate::{
    exchange::{
        candle::indicator::Indicator,
        candle_streams::candle_subscription::{CandleSubscription, CandleSubscriptionUnsubMessage},
    },
    helpers::{interval::Interval, manual_rc::ManualRc},
    Candle,
};
use litemap::LiteMap;
use tokio::sync::{broadcast, mpsc};
use tokio::time;

#[derive(Debug)]
pub struct CandleStreams {
    pub broadcasts: LiteMap<Interval, ManualRc<Broadcast>>,

    unsub_tx: mpsc::Sender<CandleSubscriptionUnsubMessage>,
    unsub_rx: mpsc::Receiver<CandleSubscriptionUnsubMessage>,
}

impl CandleStreams {
    
    pub fn new() -> Self {
        let (unsub_tx, unsub_rx) = mpsc::channel(16);

        Self {
            unsub_tx,
            unsub_rx,
            broadcasts: LiteMap::new(),
        }
    }

    pub fn subscribe(
        &mut self,
        interval: Interval,
        indicators: &[Indicator],
    ) -> CandleSubscription {
        let candle_stream = self
            .broadcasts
            .entry(interval)
            .or_insert_with(|| ManualRc::new(Broadcast::new()));

        // Incrementing References
        candle_stream.add_ref();

        for idr in indicators {
            if let Some(x) = candle_stream.indicators.get_mut(idr) {
                x.add_ref();
            } else {
                candle_stream.indicators.insert(*idr, ManualRc::new(()));
            }
        }

        let stream_rx = candle_stream.tx.subscribe().into();
        let unsub_weak_tx = self.unsub_tx.downgrade();
        CandleSubscription::new(stream_rx, unsub_weak_tx, interval, indicators)
    }

    fn unsubscribe(&mut self, unsub_message: CandleSubscriptionUnsubMessage) {
        let (interval, indicators) = unsub_message;

        let stream = self.broadcasts.get_mut(&interval).unwrap();

        for idr in indicators {
            let x = stream.indicators.get_mut(&idr).unwrap();
            if !x.remove_ref() {
                stream.indicators.remove(&idr);
            }
        }

        if !stream.remove_ref() {
            self.broadcasts.remove(&interval);
        }
    }


}

#[derive(Debug)]
pub struct Broadcast {
    /// Mapping of indicators its the number of subscriptions
    indicators: LiteMap<Indicator, ManualRc<()>>,
    tx: broadcast::Sender<Candle>,
}

impl Broadcast {
    pub fn new() -> Self {
        let (broadcast_tx, _broadcast_rx) = broadcast::channel(16);
        Self {
            tx: broadcast_tx,
            indicators: LiteMap::new_vec(),
        }
    }
}
