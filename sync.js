/* Synchronisation : le journal (séances cochées, renfo) est enregistré dans journal.json
   sur la branche « journal » de ce dépôt GitHub. Téléphone et ordinateur partagent ainsi
   les mêmes données, et Claude peut les lire. La clé GitHub ne quitte jamais ce navigateur
   (elle n'est envoyée qu'à api.github.com). Fusion par élément : rien n'est perdu quand les
   deux appareils ont servi hors ligne. */
(function(root){
  var FILE = "journal.json", BRANCH = "journal";

  /* ---------- fusion pure ---------- */
  function mergeMap(a, b){
    a = a || {}; b = b || {}; var o = {};
    Object.keys(a).concat(Object.keys(b)).forEach(function(k){
      var x = a[k], y = b[k];
      o[k] = !x ? y : !y ? x : ((y.t || 0) > (x.t || 0) ? y : x);
    });
    return o;
  }
  function merge(a, b){
    a = a || {}; b = b || {};
    return { v: 1, done: mergeMap(a.done, b.done), renfo: mergeMap(a.renfo, b.renfo), notes: mergeMap(a.notes, b.notes) };
  }
  function canon(s){
    s = merge(s, {});
    function so(o){ if (!o || typeof o !== "object" || Array.isArray(o)) return o; var r = {}; Object.keys(o).sort().forEach(function(k){ r[k] = so(o[k]); }); return r; }
    return JSON.stringify(so(s));
  }
  root.TSyncCore = { merge: merge, canon: canon };
  if (typeof document === "undefined") return;

  var A = root.APP; if (!A) return;
  var LS = { get: function(k){ try { return localStorage.getItem(k); } catch(e){ return null; } }, set: function(k, v){ try { localStorage.setItem(k, v); } catch(e){} }, del: function(k){ try { localStorage.removeItem(k); } catch(e){} } };

  /* dépôt : déduit de l'adresse GitHub Pages (utilisateur.github.io/depot), sinon réglages */
  function repo(){
    var saved = LS.get("sync_repo"); if (saved) return saved;
    var h = location.hostname, p = location.pathname.split("/").filter(Boolean);
    if (/\.github\.io$/.test(h) && p[0]) return h.split(".")[0] + "/" + p[0];
    return "rleger/coach-trail";
  }
  function token(){ return LS.get("sync_token") || ""; }
  function api(method, path, body){
    return fetch("https://api.github.com/repos/" + repo() + path, {
      method: method, cache: "no-store",
      headers: { "Authorization": "Bearer " + token(), "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" },
      body: body ? JSON.stringify(body) : undefined
    }).then(function(r){
      if (r.status === 401) throw { kind: "auth" };
      if (r.status === 403) throw { kind: "forbidden" };
      if (r.status === 404) throw { kind: "missing" };
      if (r.status === 409 || r.status === 422) throw { kind: "conflict" };
      if (!r.ok) throw { kind: "http", status: r.status };
      return r.status === 204 ? null : r.json();
    }, function(){ throw { kind: "net" }; });
  }
  function b64enc(s){ return btoa(unescape(encodeURIComponent(s))); }
  function b64dec(s){ return decodeURIComponent(escape(atob((s || "").replace(/\s/g, "")))); }

  function ensureBranch(){
    return api("GET", "/git/ref/heads/" + BRANCH).catch(function(e){
      if (e.kind !== "missing") throw e;
      return api("GET", "").then(function(info){ return api("GET", "/git/ref/heads/" + (info.default_branch || "main")); })
        .then(function(ref){ return api("POST", "/git/refs", { ref: "refs/heads/" + BRANCH, sha: ref.object.sha }); });
    });
  }
  function fetchRemote(){
    return api("GET", "/contents/" + FILE + "?ref=" + BRANCH).then(function(f){
      var snap = {}; try { snap = JSON.parse(b64dec(f.content)); } catch(e){}
      return { snap: snap, sha: f.sha };
    }, function(e){ if (e.kind === "missing") return { snap: {}, sha: null }; throw e; });
  }
  function save(snap, sha){
    var body = { message: "journal : mise à jour depuis l'app", content: b64enc(JSON.stringify(snap, null, 1) + "\n"), branch: BRANCH };
    if (sha) body.sha = sha;
    return api("PUT", "/contents/" + FILE, body);
  }

  var busy = false, timer = null, lastErr = null;
  function setStatus(st, msg){ lastErr = st === "error" ? msg : null; var b = document.getElementById("syncBtn"); if (b) b.setAttribute("data-state", st); renderSheet(); }
  function once(){
    return ensureBranch().then(fetchRemote).then(function(r){
      var local = A.readJournal(), merged = merge(local, r.snap), changed = canon(merged) !== canon(local);
      A.writeJournal(merged);
      var p = canon(merged) !== canon(r.snap) ? save(merged, r.sha) : Promise.resolve();
      return p.then(function(){ return changed; });
    });
  }
  function syncNow(){
    if (!token() || busy) return Promise.resolve(false);
    if (!navigator.onLine){ setStatus("off"); return Promise.resolve(false); }
    busy = true; setStatus("busy");
    return once().catch(function(e){ if (e && e.kind === "conflict") return once(); throw e; })
      .then(function(changed){ busy = false; LS.set("sync_last", String(Date.now())); setStatus("ok"); if (changed) A.refresh(); return true; })
      .catch(function(e){
        busy = false;
        var msg = !e ? "Erreur inconnue" :
          e.kind === "auth" ? "GitHub refuse la clé. Vérifie-la ou crée-en une nouvelle." :
          e.kind === "forbidden" ? "La clé n'a pas le droit d'écrire dans ce dépôt (Contents : Read and write)." :
          e.kind === "missing" ? "Dépôt introuvable : " + repo() :
          e.kind === "net" ? "GitHub injoignable. Nouvel essai plus tard." : "Erreur GitHub " + (e.status || "");
        setStatus(e && e.kind === "net" ? "off" : "error", msg);
        return false;
      });
  }
  A.onSave = function(){ if (!token()) return; clearTimeout(timer); timer = setTimeout(syncNow, 3000); };
  document.addEventListener("visibilitychange", function(){ if (!token()) return; if (document.hidden){ if (timer){ clearTimeout(timer); timer = null; syncNow(); } } else syncNow(); });
  window.addEventListener("online", function(){ syncNow(); });

  /* ---------- sauvegarde fichier ---------- */
  function download(){
    var blob = new Blob([JSON.stringify(A.readJournal(), null, 1)], { type: "application/json" });
    var a = document.createElement("a"), d = new Date();
    a.href = URL.createObjectURL(blob); a.download = "trail-journal-" + d.toISOString().slice(0, 10) + ".json";
    document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }
  function importFile(file){
    var rd = new FileReader();
    rd.onload = function(){
      try { var s = JSON.parse(rd.result); if (!s || typeof s !== "object" || !("renfo" in s || "done" in s)) throw 0;
        A.writeJournal(merge(A.readJournal(), s)); A.toast("Sauvegarde fusionnée"); A.refresh(); A.onSave();
      } catch(e){ A.toast("Ce fichier n'est pas une sauvegarde de l'app."); }
    };
    rd.readAsText(file);
  }

  /* ---------- interface ---------- */
  var sheet = document.getElementById("syncSheet"), btn = document.getElementById("syncBtn");
  function ago(t){ if (!t) return "jamais"; var s = Math.round((Date.now() - t) / 1000); return s < 60 ? "à l'instant" : s < 3600 ? "il y a " + Math.round(s / 60) + " min" : s < 86400 ? "il y a " + Math.round(s / 3600) + " h" : new Date(t).toLocaleDateString("fr-FR"); }
  function renderSheet(){
    if (!sheet || sheet.hidden) return;
    var on = !!token(), st = btn.getAttribute("data-state") || (on ? "ok" : "none"), esc = A.esc;
    var h = '<div class="sheet-card" role="document"><div class="sheet-head"><h2>Synchronisation</h2><button type="button" class="icon-btn" data-sync="close" aria-label="Fermer">✕</button></div>';
    if (on){
      h += '<p class="sync-state s-' + st + '">' + (st === "busy" ? "Synchronisation…" : st === "error" ? esc(lastErr || "Erreur") : st === "off" ? "Hors ligne : tout est gardé ici et partira plus tard." : "Synchronisé " + ago(+(LS.get("sync_last") || 0))) + '</p>' +
        '<p class="hint">Journal enregistré dans <b>' + esc(repo()) + '</b>, branche <b>' + BRANCH + '</b>, fichier <b>' + FILE + '</b>. Claude le lit à cet endroit.</p>' +
        '<div class="row"><button type="button" class="btn primary" data-sync="now">Synchroniser</button><button type="button" class="btn" data-sync="off">Déconnecter cet appareil</button></div>';
    } else {
      h += '<p class="hint">Colle une clé GitHub limitée à ce dépôt. La même clé sert sur le téléphone et l\'ordinateur.</p>' +
        '<ol class="steps"><li>github.com : Settings → Developer settings → Personal access tokens → <b>Fine-grained tokens</b> → Generate new token.</li>' +
        '<li>Repository access : <b>Only select repositories</b> → ' + esc(repo()) + '.</li><li>Permissions → Repository → <b>Contents : Read and write</b>. Rien d\'autre.</li><li>Copie la clé (github_pat_…) et colle-la ici.</li></ol>' +
        '<input type="password" id="syncTok" class="input" placeholder="github_pat_…" autocomplete="off" autocapitalize="off" spellcheck="false">' +
        '<div class="row"><button type="button" class="btn primary" data-sync="connect">Connecter</button></div>';
    }
    h += '<hr><p class="hint">Sauvegarde fichier (sans GitHub)</p><div class="row"><button type="button" class="btn" data-sync="dl">Télécharger</button><button type="button" class="btn" data-sync="imp">Importer</button></div><input type="file" id="syncFile" accept="application/json,.json" hidden></div>';
    sheet.innerHTML = h;
  }
  function open(){ sheet.hidden = false; document.documentElement.classList.add("lock"); renderSheet(); }
  function close(){ sheet.hidden = true; document.documentElement.classList.remove("lock"); }
  btn.addEventListener("click", open);
  sheet.addEventListener("click", function(e){
    if (e.target === sheet){ close(); return; }
    var b = e.target.closest("[data-sync]"); if (!b) return;
    switch (b.getAttribute("data-sync")){
      case "close": close(); break;
      case "now": syncNow(); break;
      case "connect":
        var v = (document.getElementById("syncTok").value || "").trim();
        if (!/^(ghp_|github_pat_)[A-Za-z0-9_]{20,}$/.test(v)){ A.toast("Ce n'est pas une clé GitHub (github_pat_…)."); return; }
        LS.set("sync_token", v); renderSheet();
        syncNow().then(function(ok){ if (ok) A.toast("Connecté : cet appareil se synchronise."); });
        break;
      case "off": ["sync_token", "sync_last"].forEach(LS.del); btn.removeAttribute("data-state"); A.toast("Cet appareil ne se synchronise plus. Le journal reste ici."); renderSheet(); break;
      case "dl": download(); break;
      case "imp": document.getElementById("syncFile").click(); break;
    }
  });
  sheet.addEventListener("change", function(e){ if (e.target.id === "syncFile" && e.target.files[0]) importFile(e.target.files[0]); });
  document.addEventListener("keydown", function(e){ if (!sheet.hidden && e.key === "Escape") close(); });
  if (token()){ btn.setAttribute("data-state", "ok"); setTimeout(syncNow, 300); }
})(typeof window !== "undefined" ? window : globalThis);
