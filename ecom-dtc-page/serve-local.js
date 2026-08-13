const http = require("http");
const fs = require("fs");
const path = require("path");

const root = __dirname;
const port = Number(process.env.PORT || 4177);

const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
};

function send(res, status, headers, body) {
  res.writeHead(status, {
    "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
    Pragma: "no-cache",
    Expires: "0",
    ...headers,
  });
  res.end(body);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const requestPath = decodeURIComponent(url.pathname);
  const filePath = path.normalize(path.join(root, requestPath === "/" ? "index.html" : requestPath));

  if (!filePath.startsWith(root)) {
    send(res, 403, { "Content-Type": "text/plain; charset=utf-8" }, "Forbidden");
    return;
  }

  fs.readFile(filePath, (error, data) => {
    if (error) {
      send(res, 404, { "Content-Type": "text/plain; charset=utf-8" }, "Not found");
      return;
    }

    const contentType = types[path.extname(filePath).toLowerCase()] || "application/octet-stream";
    send(res, 200, { "Content-Type": contentType }, data);
  });
});

server.listen(port, "127.0.0.1", () => {
  console.log(`Lymphaflow preview running at http://127.0.0.1:${port}/`);
});
