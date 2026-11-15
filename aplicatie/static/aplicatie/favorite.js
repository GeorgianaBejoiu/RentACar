
document.addEventListener('DOMContentLoaded', function () {

    // Selectăm toate butoanele pentru adăugarea sau eliminarea mașinilor din favorite.
    const butoaneFavorite = document.querySelectorAll('.favorite-btn');

    // Preluăm tokenul CSRF necesar pentru securizarea cererilor POST către Django.
    const csrfToken = document.querySelector(
        '#csrf-container [name=csrfmiddlewaretoken]'
    ).value;

    // Parcurgem toate butoanele de favorite pentru a le adăuga funcționalitatea de click.
    butoaneFavorite.forEach(function (buton) {

        //Trimitem o cerere POST către server, folosind URL-ul asociat butonului.
        buton.addEventListener('click', function () {

            fetch(buton.dataset.url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })

            //Verificăm dacă răspunsul serverului este valid și îl transformăm în JSON.
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('A apărut o eroare.');
                }
                return response.json();
            })

            // Prelucrăm datele primite de la server și actualizăm aspectul butonului.
            .then(function (data) {

                if (data.success) {
                    // Dacă mașina a fost adăugată la favorite, afișăm o inimă plină.
                    if (data.este_favorita) {
                        buton.textContent = '♥';
                        buton.classList.remove('btn-outline-danger');
                        buton.classList.add('btn-danger');
                        buton.setAttribute('aria-pressed', 'true');
                    } else {// Dacă mașina a fost eliminată, afișăm o inimă goală.
                        buton.textContent = '♡';
                        buton.classList.remove('btn-danger');
                        buton.classList.add('btn-outline-danger');
                        buton.setAttribute('aria-pressed', 'false');
                    }

                    // Dacă serverul indică o problemă, afișăm mesajul de eroare.
                } else {
                    alert(data.error || 'Nu s-a putut modifica lista de favorite.');
                }

            })

            // Gestionăm erorile apărute în timpul trimiterii sau prelucrării cererii.
            .catch(function (error) {
                console.error(error);
                alert('Nu am putut salva modificarea. Încearcă din nou.');
            });

        });

    });

});
