document.addEventListener('DOMContentLoaded', function () {
  console.log('zgloszenia_lista.js loaded');
  const rows = document.querySelectorAll('tr.link-row');

  rows.forEach(row => {
    row.addEventListener('click', function (event) {
      // jeśli kliknięto w przycisk/formularz w wierszu, nie otwieraj modala
      if (event.target.closest('button') || event.target.closest('a') || event.target.closest('form')) {
        return;
      }
      const id = this.getAttribute('data-zgloszenie-id');
      if (!id) return;

      const modalEl = document.getElementById('zgloszenieModal' + id);
      if (!modalEl) return;

      const modal = new bootstrap.Modal(modalEl);
      modal.show();
    });
  });
});
