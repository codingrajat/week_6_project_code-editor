const editor = ace.edit("editor");
editor.setTheme("ace/theme/dracula");
editor.session.setMode("ace/mode/python");
editor.setFontSize(16);

const languageSelect = document.getElementById("language");
languageSelect.addEventListener("change", () => {
  const lang = languageSelect.value;
  if (lang === "python") editor.session.setMode("ace/mode/python");
  if (lang === "cpp") editor.session.setMode("ace/mode/c_cpp");
});

document.getElementById("run-btn").addEventListener("click", async () => {
  const code = editor.getValue();
  const language = languageSelect.value;
  const outputElement = document.getElementById("output");
  outputElement.textContent = "Running...";

  try {
    const response = await fetch("http://127.0.0.1:5000/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, language }),
    });

    if (!response.ok) {
      outputElement.textContent = `Error: ${response.status}`;
      return;
    }

    const result = await response.json();
    outputElement.textContent = result.output || result.error || "No output";
  } catch (err) {
    outputElement.textContent = `Network error: ${err.message}`;
  }
});
