# Setup Complete! 🎉

All dependencies have been successfully installed and compiled.

## What's Ready

✅ **Trunk** - Installed for building the frontend  
✅ **Cargo Watch** - Installed for auto-reload  
✅ **Backend Server** - Built and ready  
✅ **Frontend App** - Built and ready

## Running the App

### Quick Start (Recommended)

**Terminal 1 - Backend:**

```powershell
cd server
cargo run
```

**Terminal 2 - Frontend:**

```powershell
cd frontend
trunk serve
```

Then open http://localhost:8080 in your browser.

### With Auto-Reload

**Terminal 1 - Backend (with watch):**

```powershell
cd server
cargo watch -- cargo run
```

**Terminal 2 - Frontend:**

```powershell
cd frontend
trunk serve
```

## Project Structure

- `server/` - Axum backend server (port 8080)
- `frontend/` - Yew frontend application
- `target/` - Build artifacts

## API Endpoints

- `GET /api/hello` - Returns "hello from server!"
- Frontend routes are served by the backend automatically

Enjoy your full-stack Rust app! 🦀
