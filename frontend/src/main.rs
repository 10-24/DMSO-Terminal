use gloo_net::http::Request;
use wasm_bindgen_futures::spawn_local;
use yew::prelude::*;
use yew_router::prelude::*;

mod terminal;
use terminal::Terminal;

#[derive(Clone, Routable, PartialEq)]
enum Route {
    #[at("/")]
    Terminal,
    #[at("/hello-server")]
    HelloServer,
    #[at("/chart")]
    Chart,
}

fn switch(routes: Route) -> Html {
    match routes {
        Route::Terminal => html! { <Terminal /> },
        Route::HelloServer => html! { <HelloServer /> },
        Route::Chart => html! { <ChartDemo /> },
    }
}

#[function_component(App)]
fn app() -> Html {
    html! {
        <BrowserRouter>
            <Switch<Route> render={switch} />
        </BrowserRouter>
    }
}

#[function_component(HelloServer)]
fn hello_server() -> Html {
    let data = use_state(|| None);

    // Request `/api/hello` once
    {
        let data = data.clone();
        use_effect(move || {
            if data.is_none() {
                spawn_local(async move {
                    let resp = Request::get("/api/hello").send().await.unwrap();
                    let result = {
                        if !resp.ok() {
                            Err(format!(
                                "Error fetching data {} ({})",
                                resp.status(),
                                resp.status_text()
                            ))
                        } else {
                            resp.text().await.map_err(|err| err.to_string())
                        }
                    };
                    data.set(Some(result));
                });
            }

            || {}
        });
    }

    match data.as_ref() {
        None => {
            html! {
                <div>{"No server response"}</div>
            }
        }
        Some(Ok(data)) => {
            html! {
                <div>{"Got server response: "}{data}</div>
            }
        }
        Some(Err(err)) => {
            html! {
                <div>{"Error requesting data from server: "}{err}</div>
            }
        }
    }
}

#[function_component(ChartDemo)]
fn chart_demo() -> Html {
    let chart_container_id = use_state(|| "chart-container".to_string());

    html! {
        <div style="padding: 20px;">
            <h2>{ "Charming Chart Demo" }</h2>
            <div id={(*chart_container_id).clone()} style="width: 800px; height: 500px;"></div>
        </div>
    }
}

fn main() {
    wasm_logger::init(wasm_logger::Config::new(log::Level::Trace));
    console_error_panic_hook::set_once();
    yew::Renderer::<App>::new().render();
}
