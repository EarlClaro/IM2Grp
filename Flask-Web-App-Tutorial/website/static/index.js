function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function updateNote(noteId, updatedContent) {
  fetch("/update-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId, updatedContent: updatedContent }),
  }).then((_res) => {
      // Reload the page after updating the note
      window.location.href = "/";
  });
}