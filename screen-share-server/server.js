const express = require("express");
const http = require("http");
const path = require("path");
const crypto = require("crypto");
const { WebSocketServer, WebSocket } = require("ws");

const app = express();
app.disable("x-powered-by");
app.use(express.json({ limit: "64kb" }));
app.use((req,res,next)=>{
  res.setHeader("X-Content-Type-Options","nosniff");
  res.setHeader("Referrer-Policy","no-referrer");
  res.setHeader("X-Frame-Options","DENY");
  next();
});

const ADMIN_PASSWORD = process.env.ADMIN_KEY;
if (!ADMIN_PASSWORD) {
  console.error("ADMIN_KEY is required");
  process.exit(1);
}

const tokens = new Map();
const clients = new Map();
const admins = new Map();

function newToken() {
  const token = crypto.randomBytes(32).toString("hex");
  tokens.set(token, Date.now() + 12 * 60 * 60 * 1000);
  return token;
}
function validToken(token) {
  const exp = tokens.get(token);
  if (!exp || exp < Date.now()) {
    if (token) tokens.delete(token);
    return false;
  }
  return true;
}
function auth(req,res,next) {
  const h = req.headers.authorization || "";
  const token = h.startsWith("Bearer ") ? h.slice(7) : "";
  if (!validToken(token)) return res.status(401).json({ error: "Unauthorized" });
  next();
}
function clientSnapshot() {
  return [...clients.values()].map(c => ({
    deviceId: c.deviceId,
    name: c.name,
    connectedAt: c.connectedAt,
    sharing: true
  }));
}
function broadcastClients() {
  const msg = JSON.stringify({ type: "clients", clients: clientSnapshot() });
  for (const a of admins.values()) {
    if (a.ws.readyState === WebSocket.OPEN) a.ws.send(msg);
  }
}

app.post("/api/login",(req,res)=>{
  if (req.body && req.body.password === ADMIN_PASSWORD) {
    return res.json({ token: newToken() });
  }
  res.status(401).json({ error: "Invalid password" });
});
app.get("/api/clients",auth,(req,res)=>res.json({ clients: clientSnapshot() }));
app.get("/health",(req,res)=>res.json({ ok:true, clients:clients.size }));
app.use(express.static(path.join(__dirname,"public")));

const server = http.createServer(app);
const wss = new WebSocketServer({ server, path: "/ws" });

wss.on("connection",(ws)=>{
  let identity = null;

  const helloTimer = setTimeout(()=> {
    if (!identity) ws.close(1008,"hello required");
  }, 10000);

  ws.on("message",(raw)=>{
    let m;
    try { m = JSON.parse(raw.toString()); } catch { return; }

    if (!identity) {
      if (m.type !== "hello") return;

      if (m.role === "client") {
        const deviceId = String(m.deviceId || "").slice(0,80);
        const name = String(m.name || "Android user").slice(0,80);
        if (!deviceId) return ws.close(1008,"deviceId required");

        identity = { role:"client", id:deviceId };
        clients.set(deviceId,{ ws, deviceId, name, connectedAt:new Date().toISOString() });
        clearTimeout(helloTimer);
        ws.send(JSON.stringify({ type:"hello-ok", id:deviceId }));
        broadcastClients();
        return;
      }

      if (m.role === "admin" && validToken(m.token)) {
        const id = "admin-" + crypto.randomBytes(6).toString("hex");
        identity = { role:"admin", id };
        admins.set(id,{ ws, id });
        clearTimeout(helloTimer);
        ws.send(JSON.stringify({ type:"hello-ok", id }));
        ws.send(JSON.stringify({ type:"clients", clients:clientSnapshot() }));
        return;
      }

      return ws.close(1008,"unauthorized");
    }

    if (m.type === "signal" && m.to && m.data) {
      const to = String(m.to);
      let target = clients.get(to)?.ws || admins.get(to)?.ws;
      if (target && target.readyState === WebSocket.OPEN) {
        target.send(JSON.stringify({
          type:"signal",
          from:identity.id,
          data:m.data
        }));
      }
    }
  });

  ws.on("close",()=>{
    clearTimeout(helloTimer);
    if (!identity) return;
    if (identity.role === "client") {
      const current = clients.get(identity.id);
      if (current && current.ws === ws) clients.delete(identity.id);
      broadcastClients();
    } else {
      admins.delete(identity.id);
    }
  });
});

setInterval(()=>{
  for (const [t,exp] of tokens) if (exp < Date.now()) tokens.delete(t);
}, 10 * 60 * 1000).unref();

const port = process.env.PORT || 10000;
server.listen(port, ()=>console.log("Screen-share admin server listening on", port));
