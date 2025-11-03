use tokio::sync::mpsc;
use tokio_stream::wrappers::BroadcastStream;

use crate::{exchange::candle::indicator::Indicator, helpers::interval::Interval, Candle};


/// To `unsubscribe` from the broadcast, simply drop the struct.
#[derive(Debug)]
pub struct CandleSubscription {
    pub stream_rx: BroadcastStream<Candle>,
    unsub: Box<CandleSubscriptionUnsub>,
}

impl CandleSubscription {
    pub fn new(
        stream_rx: BroadcastStream<Candle>,
        unsub_weak_tx: mpsc::WeakSender<CandleSubscriptionUnsubMessage>,
        interval: Interval,
        indicators: &[Indicator],
    ) -> Self {
        let unsub = CandleSubscriptionUnsub {
            unsub_weak_tx,
            message: (interval, indicators.into()),
        };

        Self {
            stream_rx,
            unsub: Box::new(unsub),
        }
    }
}

impl Drop for CandleSubscription {
    // Unsubscribes from the broadcast
    fn drop(&mut self) {
        let unsub_tx = self.unsub.unsub_weak_tx.upgrade();

        // If the unsub channel has closed, then it gives up.
        if let Some(unsub_tx) = unsub_tx {
            let unsub_message = self.unsub.message.clone();
            let _ = unsub_tx.try_send(unsub_message);
        }
    }
}

#[derive(Debug)]
struct CandleSubscriptionUnsub {
    unsub_weak_tx: mpsc::WeakSender<CandleSubscriptionUnsubMessage>,
    message: CandleSubscriptionUnsubMessage,
}

pub type CandleSubscriptionUnsubMessage = (Interval, Box<[Indicator]>);
