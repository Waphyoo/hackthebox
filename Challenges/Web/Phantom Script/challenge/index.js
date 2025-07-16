const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const app = express();
const path = require("path");
const nunjucks = require("nunjucks");
const routes = require("./routes");
const { setIo } = require("./helpers/botHelper"); // Import the setter function

app.use(express.json());

nunjucks.configure("views", {
  autoescape: true,
  express: app,
});

app.set("views", "./views");
app.use("/static", express.static(path.resolve("static")));
app.set("etag", false);

app.use(routes());

app.all("*", (req, res) => {
  return res.status(404).send({
    message: "404 page not found",
  });
});

// Create an HTTP server
const server = http.createServer(app);

// Initialize socket.io
const io = socketIo(server);

setIo(io);

io.on("connection", (socket) => {
  console.log("Socket.io client connected");

  socket.on("message", (message) => {
    console.log("Received:", message);
  });

  // Example of emitting an event to the client
  socket.emit("welcome", "Welcome to the WebSocket server!");
});

// Start the server and WebSocket server
server.listen(1337, "0.0.0.0", () => console.log("Listening on port 1337"));
