use js_sys::Date;
use wasm_bindgen::JsCast;
use web_sys::{HtmlInputElement, InputEvent, KeyboardEvent};
use yew::prelude::*;

#[function_component(Terminal)]
pub fn terminal() -> Html {
    let input = use_state(|| String::new());
    let history = use_state(Vec::<String>::new);

    let on_input = {
        let input = input.clone();
        Callback::from(move |e: InputEvent| {
            let target = e.target().unwrap();
            let input_element = target.dyn_ref::<HtmlInputElement>().unwrap();
            input.set(input_element.value());
        })
    };

    let on_keydown = {
        let input = input.clone();
        let history = history.clone();
        Callback::from(move |e: KeyboardEvent| {
         
        })
    };

    html! {
        <div class="terminal-container">
            <style>
                {"
                .terminal-container {
                    background: #1e1e1e;
                    color: #d4d4d4;
                    font-family: 'Courier New', monospace;
                    height: 100vh;
                    padding: 20px;
                    display: flex;
                    flex-direction: column;
                }
                .terminal-header {
                    background: #2d2d30;
                    padding: 10px;
                    margin-bottom: 10px;
                    border-radius: 5px;
                }
                .terminal-history {
                    flex: 1;
                    overflow-y: auto;
                    padding: 10px;
                    margin-bottom: 10px;
                }
                .terminal-line {
                    margin: 5px 0;
                    white-space: pre-wrap;
                }
                .terminal-prompt {
                    color: #4ec9b0;
                    font-weight: bold;
                }
                .terminal-input-container {
                    display: flex;
                    align-items: center;
                }
                .terminal-input {
                    flex: 1;
                    background: #1e1e1e;
                    color: #d4d4d4;
                    border: none;
                    outline: none;
                    font-family: 'Courier New', monospace;
                    font-size: 14px;
                    padding: 5px;
                }
                .terminal-cursor {
                    display: inline-block;
                    width: 8px;
                    height: 14px;
                    background: #d4d4d4;
                    animation: blink 1s infinite;
                }
                @keyframes blink {
                    0%, 50% { opacity: 1; }
                    51%, 100% { opacity: 0; }
                }
                "}
            </style>
            <div class="terminal-header">
                <h2 style="margin: 0; color: #4ec9b0;">{"DMSO Terminal"}</h2>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #858585;">
                    {"Type 'help' for available commands"}
                </p>
            </div>
            <div class="terminal-history">
                {for (*history).iter().map(|line| {
                    html! {
                        <div class="terminal-line">{line}</div>
                    }
                })}
                <div class="terminal-line">
                    <span class="terminal-prompt">{"$"}</span>
                    {" "}
                    <input
                        class="terminal-input"
                        type="text"
                        value={(*input).clone()}
                        oninput={on_input}
                        onkeydown={on_keydown}
                        placeholder="Enter command..."
                    />
                </div>
            </div>
        </div>
    }
}
