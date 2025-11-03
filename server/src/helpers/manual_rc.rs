use std::ops::{Deref, DerefMut};

#[derive(Debug)]
pub struct ManualRc<T> {
    pub value: T,
    references: u16,
}
impl<T> ManualRc<T> {
    pub fn new(value: T) -> Self {
        Self {
            value,
            references: 1,
        }
    }

    pub fn add_ref(&mut self) {
        self.references += 1;
    }
    /// Returns if references > 0
    pub fn remove_ref(&mut self) -> bool {
        self.references -= 1;
        self.references > 0
    }
}

impl<T> Deref for ManualRc<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.value
    }
}

impl<T> DerefMut for ManualRc<T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.value
    }
}
