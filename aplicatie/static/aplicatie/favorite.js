
document.addEventListener('DOMContentLoaded', function () {

    const butoaneFavorite = document.querySelectorAll('.favorite-btn');

    const csrfToken = document.querySelector(
        '#csrf-container [name=csrfmiddlewaretoken]'
    ).value;

    butoaneFavorite.forEach(function (buton) {

        buton.addEventListener('click', function () {

            fetch(buton.dataset.url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })

            .then(function (response) {
                if (!response.ok) {
                    throw new Error('A apărut o eroare.');
                }
                return response.json();
            })

            .then(function (data) {

                if (data.success) {

                    if (data.este_favorita) {
                        buton.textContent = '♥';
                        buton.classList.remove('btn-outline-danger');
                        buton.classList.add('btn-danger');
                        buton.setAttribute('aria-pressed', 'true');
                    } else {
                        buton.textContent = '♡';
                        buton.classList.remove('btn-danger');
                        buton.classList.add('btn-outline-danger');
                        buton.setAttribute('aria-pressed', 'false');
                    }

                } else {
                    alert(data.error || 'Nu s-a putut modifica lista de favorite.');
                }

            })

            .catch(function (error) {
                console.error(error);
                alert('Nu am putut salva modificarea. Încearcă din nou.');
            });

        });

    });

});
