document.getElementById("plagiarism-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const code1 = document.getElementById("text1").value;
  const code2 = document.getElementById("text2").value;

  const response = await fetch("http://127.0.0.1:5000/compare", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ code1, code2 })
  });

  const data = await response.json();

  if (data.error) {
    document.getElementById("result").innerText = data.error;
    return;
  }

  // Show similarity percent
  document.getElementById("similarity-score").innerText = `Similarity: ${data.similarity_percent}%`;

  // Highlight similarities and differences
  const highlighted1 = highlightDifferences(code1, code2);
  const highlighted2 = highlightDifferences(code2, code1);

  document.getElementById("highlighted-text1").innerHTML = highlighted1;
  document.getElementById("highlighted-text2").innerHTML = highlighted2;
});

// Function to highlight matching words
function highlightDifferences(textA, textB) {
  const wordsA = textA.split(/\s+/);
  const wordsBSet = new Set(textB.split(/\s+/));

  return wordsA
    .map(word => {
      if (wordsBSet.has(word)) {
        return `<span class="match">${word}</span>`;
      } else {
        return `<span class="different">${word}</span>`;
      }
    })
    .join(" ");
}
