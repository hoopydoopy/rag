(() => {
  const button = document.getElementById("generateBtn");
  const promptInput = document.getElementById("prompt");
  const statusEl = document.getElementById("status");
  const downloadBtn = document.getElementById("downloadBtn");

  if (!button || !promptInput || !statusEl || !downloadBtn) {
    console.error("Required DOM elements not found");
    return;
  }

  let downloadUrl = null;

  button.onclick = async () => {
    statusEl.innerText = "Generating...";
    downloadBtn.style.display = "none";
    downloadUrl = null;

    try {
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_request: promptInput.value,
        }),
      });

      if (!response.ok) {
        const text = await response.text();
        statusEl.innerText = `Error ${response.status}: ${text}`;
        return;
      }

      const data = await response.json();
      downloadUrl = `http://localhost:8000${data.download_url}`;

      downloadBtn.style.display = "inline";
      statusEl.innerText = "Ready to download";
    } catch (err) {
      console.error(err);
      statusEl.innerText = "Network error";
    }
  };

  downloadBtn.onclick = () => {
    if (!downloadUrl) return;
    window.location.href = downloadUrl;
  };
})();
