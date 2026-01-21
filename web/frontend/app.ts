(() => {
  // Get elements once
  const button = document.getElementById("generateBtn") as HTMLButtonElement;
  const promptInput = document.getElementById("prompt") as HTMLTextAreaElement;
  const statusEl = document.getElementById("status") as HTMLParagraphElement;
  const downloadBtn = document.getElementById(
    "downloadBtn",
  ) as HTMLButtonElement;

  // Track download URL
  let downloadUrl: string | null = null;

  // Generate button click
  button.onclick = async () => {
    if (!button || !promptInput || !statusEl || !downloadBtn) return;

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
        const errorText = await response.text();
        statusEl.innerText = `Error ${response.status}: ${errorText}`;
        return;
      }

      const data: { download_url: string } = await response.json();
      downloadUrl = `http://localhost:8000${data.download_url}`;
      downloadBtn.style.display = "inline";
      statusEl.innerText = "Ready to download";
    } catch (err) {
      console.error("Fetch failed:", err);
      statusEl.innerText = `Fetch error: ${err}`;
    }
  };

  // Download button click
  downloadBtn.onclick = () => {
    if (!downloadUrl) return;
    window.location.href = downloadUrl;
  };
})();
