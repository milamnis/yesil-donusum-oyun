import http from "node:http";
import { readFile, stat } from "node:fs/promises";
import { resolve, extname, sep } from "node:path";
import { spawn } from "node:child_process";
const root = resolve(import.meta.dirname, "dist");
const mime = {
  ".html": "text/html;charset=utf-8",
  ".js": "text/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".webp": "image/webp",
  ".jpg": "image/jpeg",
  ".woff2": "font/woff2",
};
const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, "http://localhost");
    let p = resolve(root, "." + decodeURIComponent(url.pathname));
    if (p !== root && !p.startsWith(root + sep)) {
      res.writeHead(403);
      res.end();
      return;
    }
    try {
      if ((await stat(p)).isDirectory()) p = resolve(p, "index.html");
    } catch {
      if (extname(p)) {
        res.writeHead(404);
        res.end();
        return;
      }
      p = resolve(root, "index.html");
    }
    const body = await readFile(p);
    res.writeHead(200, {
      "Content-Type": mime[extname(p)] ?? "application/octet-stream",
      "Cache-Control": "no-cache",
    });
    res.end(body);
  } catch {
    res.writeHead(500);
    res.end("Dosya okunamadi");
  }
});
server.on("error", (e) => {
  console.error("Sunucu baslatilamadi:", e.message);
  process.exitCode = 1;
});
server.listen(4173, "127.0.0.1", () => {
  console.log("Yesil Donusum: http://127.0.0.1:4173");
  if (process.argv.includes("--open") && process.platform === "win32") {
    const child = spawn("explorer.exe", ["http://127.0.0.1:4173"], {
      windowsHide: true,
    });
    child.on("error", () => console.log("Tarayicida yukaridaki adresi acin."));
  }
});
