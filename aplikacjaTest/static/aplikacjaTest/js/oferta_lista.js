let currentOfertaId = null;
let currentDeleteUrl = null;
let previousModalId = null;
let deleteConfirmModalInstance = null;

document.addEventListener('DOMContentLoaded', function () {
    // Inicjalizacja modala potwierdzenia usunięcia
    const deleteConfirmModalEl = document.getElementById('deleteConfirmModal');
    deleteConfirmModalInstance = new bootstrap.Modal(deleteConfirmModalEl);

    // Kliknięcie w cały wiersz – otwiera modal szczegółów
    document.querySelectorAll('tr.link-row').forEach(function (row) {
        row.addEventListener('click', function () {
            const id = row.getAttribute('data-oferta-id');
            const modalEl = document.getElementById('ofertaModal' + id);
            if (!modalEl) return;
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        });
    });

    // Kliknięcie w przycisk w kolumnie Akcje – nie otwiera modala
    document.querySelectorAll('.akcje-col button, .akcje-col a').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.stopPropagation(); // nie wywołuj handlera z <tr>
        });
    });

    // Obsługa przycisku "Usuń" w każdym modalu szczegółów
    document.querySelectorAll('.usun-oferta-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            currentOfertaId = btn.getAttribute('data-oferta-id');
            currentDeleteUrl = btn.getAttribute('data-delete-url');
            previousModalId = 'ofertaModal' + currentOfertaId;

            // Ukryj modal szczegółów
            const detailModalEl = document.getElementById(previousModalId);
            const detailModalInstance = bootstrap.Modal.getInstance(detailModalEl);
            if (detailModalInstance) {
                detailModalInstance.hide();
            }

            // Wypełnij dane w modalu potwierdzenia
            const modalTitle = btn.closest('.modal-content').querySelector('.modal-title').textContent;
            document.getElementById('deleteOfertaNazwa').textContent = modalTitle;

            // Pokaż modal potwierdzenia usunięcia po zamknięciu poprzedniego
            detailModalEl.addEventListener('hidden.bs.modal', function showDeleteModal() {
                deleteConfirmModalInstance.show();
                detailModalEl.removeEventListener('hidden.bs.modal', showDeleteModal);
            }, { once: true });
        });
    });

    // Obsługa przycisku "Anuluj" w modalu potwierdzenia
    document.getElementById('anulujUsunBtn')?.addEventListener('click', function () {
        returnToDetailModal();
    });

    // Obsługa przycisku X w modalu potwierdzenia
    document.getElementById('closeDeleteModal')?.addEventListener('click', function () {
        returnToDetailModal();
    });

    // Obsługa przycisku "Usuń ofertę" w modalu potwierdzenia
    document.getElementById('potwierdzUsunBtn')?.addEventListener('click', function () {
        if (!currentOfertaId || !currentDeleteUrl) return;

        const deleteBtn = this;
        const originalText = deleteBtn.innerHTML;
        deleteBtn.disabled = true;
        deleteBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Usuwam...';

        // Pobierz CSRF token z cookie
        const csrftoken = getCookie('csrftoken');

        // Wyślij żądanie AJAX
        fetch(currentDeleteUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error('Błąd serwera (status: ' + response.status + ')');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                deleteConfirmModalInstance.hide();
                setTimeout(() => {
                    window.location.reload();
                }, 300);
            } else {
                throw new Error('Nie udało się usunąć oferty');
            }
        })
        .catch(error => {
            console.error('Błąd:', error);
            alert('Wystąpił błąd podczas usuwania oferty: ' + error.message);
            deleteBtn.disabled = false;
            deleteBtn.innerHTML = originalText;
        });
    });

    // Funkcja powrotu do modala szczegółów
    function returnToDetailModal() {
        // Ukryj modal potwierdzenia
        deleteConfirmModalInstance.hide();

        // Wróć do modala szczegółów po zamknięciu modala potwierdzenia
        deleteConfirmModalEl.addEventListener('hidden.bs.modal', function showDetailModal() {
            if (previousModalId) {
                const detailModalEl = document.getElementById(previousModalId);
                if (detailModalEl) {
                    const detailModal = new bootstrap.Modal(detailModalEl);
                    detailModal.show();
                }
            }
            // Usuń listener po wykonaniu
            deleteConfirmModalEl.removeEventListener('hidden.bs.modal', showDetailModal);
        }, { once: true });
    }
});

// Funkcja pomocnicza do pobierania cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
