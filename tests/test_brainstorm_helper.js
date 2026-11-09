const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const elements = [];
const document = {
  body: { appendChild: el => elements.push(el) },
  createElement: () => ({ style: {}, setAttribute(name, value) { this[name] = value; } }),
  querySelector: () => null,
  getElementById: id => elements.find(el => el.id === id),
  addEventListener: () => {},
};
let socket;
class WebSocket {
  constructor() { socket = this; }
}
const window = { location: { host: 'localhost', reload() {} } };
const source = fs.readFileSync(path.join(__dirname, '../methodology/workflows/brainstorming/scripts/helper.js'), 'utf8');
vm.runInNewContext(source, { window, document, WebSocket, setTimeout, clearTimeout });
socket.onmessage({ data: JSON.stringify({ type: 'error', message: 'Failed to save choice' }) });
assert.equal(elements.length, 1, 'server persistence failure must be visible');
assert.equal(elements[0].role, 'alert');
assert.match(elements[0].textContent, /failed to save choice/i);
socket.onmessage({ data: JSON.stringify({ type: 'error', message: '<img src=x onerror=alert(1)>' }) });
assert.equal(elements.length, 1, 'subsequent errors should reuse the alert');
assert.equal(elements[0].innerHTML, undefined, 'server messages must not be interpreted as HTML');
