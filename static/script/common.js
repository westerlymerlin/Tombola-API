function openModal(src) {
  const modal = document.getElementById("imageModal");
  const img = document.getElementById("modalImage");
  if (!modal || !img) return;

  modal.style.display = "block";
  img.src = src;
}

function closeModal() {
  const modal = document.getElementById("imageModal");
  if (!modal) return;

  modal.style.display = "none";
}