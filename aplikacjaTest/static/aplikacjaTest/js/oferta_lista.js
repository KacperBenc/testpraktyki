document.addEventListener('DOMContentLoaded', function () {
  // klik w cały wiersz – otwieramy modal
  document.querySelectorAll('tr.link-row').forEach(function (row) {
    row.addEventListener('click', function () {
      const id = row.getAttribute('data-oferta-id');
      const modalEl = document.getElementById('ofertaModal' + id);
      if (!modalEl) return;
      const modal = new bootstrap.Modal(modalEl);
      modal.show();
    });
  });

  // klik w przycisk w kolumnie Akcje – nie otwieramy modala
  document.querySelectorAll('.akcje-col button').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();   // nie wywołuj handlera z <tr>
    });
  });
});
