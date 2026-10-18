// Agenda Math engine - clock-time arithmetic for running orders, in whole minutes.
// Mirrored by oracle.py; keep the op order identical.
// Times are 24-hour HH:MM. Anything past midnight is marked (+1 day).

function _time(s, label) {
  var m = /^([01][0-9]|2[0-3]):([0-5][0-9])$/.exec(String(s).trim());
  if (!m) throw new Error(label + " must be a time written like 09:30, from 00:00 to 23:59");
  return parseInt(m[1], 10) * 60 + parseInt(m[2], 10);
}

function _two(n) {
  return (n < 10 ? "0" : "") + n;
}

function _show(t) {
  var day = Math.floor(t / 1440), r = t % 1440;
  var s = _two(Math.floor(r / 60)) + ":" + _two(r % 60);
  if (day === 0) return s;
  return s + " (+" + day + (day === 1 ? " day)" : " days)");
}

function _plural(n, word) {
  return n + " " + word + (n === 1 ? "" : "s");
}

function _whole(x, lo, hi, msg) {
  if (!Number.isInteger(x) || x < lo || x > hi) throw new Error(msg);
  return x;
}

function _durations(list) {
  var parts = String(list).split(",").map(function (p) { return p.trim(); });
  if (parts.length < 1 || parts.length > 12) throw new Error("enter 1 to 12 durations in minutes separated by commas");
  return parts.map(function (p) {
    if (!/^[0-9]+$/.test(p) || parseInt(p, 10) < 1 || parseInt(p, 10) > 1440) {
      throw new Error("each duration must be a whole number of minutes from 1 to 1440");
    }
    return parseInt(p, 10);
  });
}

function _gap(g) {
  return _whole(g, 0, 120, "gap must be a whole number of minutes from 0 to 120");
}

// The end truth: a start time plus a number of minutes.
function endTruth(start, minutes) {
  var a = _time(start, "start time");
  var m = _whole(minutes, 0, 10000, "minutes must be a whole number from 0 to 10000");
  return _show(a) + " plus " + _plural(m, "minute") + ": " + _show(a + m) + ".";
}

// The run truth: start and end of every item in a running order.
function runTruth(start, list, gap) {
  var a = _time(start, "start time");
  var ds = _durations(list);
  var g = _gap(gap);
  var cur = a;
  var spans = ds.map(function (d) {
    var s = cur, e = cur + d;
    cur = e + g;
    return _show(s) + " to " + _show(e);
  });
  return "Start " + _show(a) + ", gap " + _plural(g, "minute") + ": " + spans.join("; ") + ".";
}

// The fit truth: a running order against the window it has to fit in.
function fitTruth(start, end, list, gap) {
  var a = _time(start, "start time");
  var b = _time(end, "end time");
  if (b <= a) throw new Error("end time must be after start time");
  var ds = _durations(list);
  var g = _gap(gap);
  var need = ds.reduce(function (x, y) { return x + y; }, 0) + g * (ds.length - 1);
  var win = b - a;
  var tail = need <= win ? "Spare: " + (win - need) + "." : "Short: " + (need - win) + ".";
  return "Window " + _show(a) + " to " + _show(b) + " is " + _plural(win, "minute") + ". Items and gaps need " + need + ". " + tail;
}
