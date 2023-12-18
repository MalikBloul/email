document.getElementById('emailCopy').onclick = function () {
    const email = document.getElementById('email_template')

    const clipboardItem = new ClipboardItem({
        "text/plain": new Blob(
            [email.innerText],
            { type: "text/plain" }
        ),
        "text/html": new Blob(
            [email.outerHTML],
            { type: "text/html" }
        ),
    });
    
    navigator.clipboard.write([clipboardItem]);
  };