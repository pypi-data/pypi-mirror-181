true&&(function polyfill() {
    const relList = document.createElement('link').relList;
    if (relList && relList.supports && relList.supports('modulepreload')) {
        return;
    }
    for (const link of document.querySelectorAll('link[rel="modulepreload"]')) {
        processPreload(link);
    }
    new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            if (mutation.type !== 'childList') {
                continue;
            }
            for (const node of mutation.addedNodes) {
                if (node.tagName === 'LINK' && node.rel === 'modulepreload')
                    processPreload(node);
            }
        }
    }).observe(document, { childList: true, subtree: true });
    function getFetchOpts(script) {
        const fetchOpts = {};
        if (script.integrity)
            fetchOpts.integrity = script.integrity;
        if (script.referrerpolicy)
            fetchOpts.referrerPolicy = script.referrerpolicy;
        if (script.crossorigin === 'use-credentials')
            fetchOpts.credentials = 'include';
        else if (script.crossorigin === 'anonymous')
            fetchOpts.credentials = 'omit';
        else
            fetchOpts.credentials = 'same-origin';
        return fetchOpts;
    }
    function processPreload(link) {
        if (link.ep)
            // ep marker = processed
            return;
        link.ep = true;
        // prepopulate the load record
        const fetchOpts = getFetchOpts(link);
        fetch(link.href, fetchOpts);
    }
}());

const site = '';

const CYCLE = 500;
const title = document.body.querySelector("#title");
const article = document.body.querySelector("article");
const template = document.createElement("template");
const diff_key = "diff";
const long_zip = function* (...iterables) {
  const iterators = iterables.map((i) => i[Symbol.iterator]());
  while (true) {
    const acc = iterators.map((i) => i.next());
    if (acc.every((r) => r.done ?? false)) {
      break;
    } else {
      yield acc.map((r) => r.value);
    }
  }
};
const api_request = async () => await (await fetch(`${location.origin}/api/info`)).json();
const ws_connect = async function* () {
  const remote = `ws://${location.host}/ws`;
  let cb = () => {
  };
  let ws = new WebSocket(remote);
  const provision = () => {
    ws.onmessage = ({ data }) => cb(data);
    ws.onclose = async () => {
      await new Promise((resolve) => setTimeout(resolve, CYCLE));
      ws = new WebSocket(remote);
      provision();
    };
  };
  provision();
  while (true) {
    const next = new Promise((resolve) => cb = resolve);
    yield next;
  }
};
const reconciliate = (lhs, rhs) => {
  let diff = false;
  for (const [l, r] of long_zip([...lhs.childNodes], [...rhs.childNodes])) {
    if (l && !r) {
      diff = true;
      l.remove();
    } else if (!l && r) {
      diff = true;
      lhs.appendChild(r);
    } else if (l instanceof Element && r instanceof Element) {
      if (l.tagName !== r.tagName) {
        l.replaceWith(r);
      } else {
        const attrs = new Map(
          function* () {
            for (const { name, value } of r.attributes) {
              yield [name, value];
            }
          }()
        );
        for (const { name } of l.attributes) {
          if (!attrs.has(name)) {
            if (name !== diff_key) {
              diff = true;
            }
            l.removeAttribute(name);
          }
        }
        for (const [name, value] of attrs) {
          if (l.getAttribute(name) !== value) {
            diff = true;
            l.setAttribute(name, value);
          }
        }
        reconciliate(l, r);
      }
    } else {
      if (l.nodeType !== r.nodeType) {
        diff = true;
        lhs.replaceChild(r, l);
      } else if (l.nodeValue !== r.nodeValue) {
        diff = true;
        l.nodeValue = r.nodeValue;
      }
    }
  }
  if (diff && lhs instanceof Element && lhs !== article) {
    lhs.setAttribute(diff_key, String(true));
  }
};
const update = ((sha) => async (follow, new_sha) => {
  if (new_sha === sha) {
    return;
  } else {
    sha = new_sha;
  }
  const page = await (await fetch(`${location.origin}/api/markdown`)).text();
  template.innerHTML = page;
  template.normalize();
  reconciliate(article, template.content);
  await new Promise((resolve) => requestAnimationFrame(resolve));
  const marked = document.body.querySelectorAll(`[${diff_key}="${true}"]`);
  const [focus, ..._] = marked;
  if (follow && focus) {
    focus.scrollIntoView({
      behavior: "smooth",
      block: "center",
      inline: "center"
    });
  }
})("");
const main = async () => {
  const info = await api_request();
  document.title = info.title;
  title.textContent = info.title;
  const loop1 = async () => {
    while (true) {
      try {
        for await (const _ of ws_connect()) {
          await update(info.follow, info.sha);
        }
      } catch (err) {
        console.error(err);
      }
    }
  };
  const loop2 = async () => {
    while (true) {
      try {
        const info2 = await api_request();
        await update(info2.follow, info2.sha);
      } catch (err) {
        console.error(err);
      }
      await new Promise((resolve) => setTimeout(resolve, CYCLE));
    }
  };
  await Promise.all([loop1(), loop2()]);
};
await main();
