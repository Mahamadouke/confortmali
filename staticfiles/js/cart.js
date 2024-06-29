document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    const cartCountElement = document.getElementById('cart-count');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const url = this.getAttribute('href');

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    swal({
                        title: "Succès!",
                        text: "Produit ajouté au panier.",
                        type: "success",
                        confirmButtonText: "OK"
                    });
                    cartCountElement.textContent = data.total_items;
                } else {
                    swal({
                        title: "Erreur!",
                        text: "Le produit n'a pas pu être ajouté au panier.",
                        type: "error",
                        confirmButtonText: "OK"
                    });
                }
            })
            .catch(error => {
                swal({
                    title: "Erreur!",
                    text: "Une erreur est survenue. Veuillez réessayer.",
                    type: "error",
                    confirmButtonText: "OK"
                });
            });
        });
    });

    document.querySelectorAll('.remove-from-cart-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const form = this.closest('form');
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    swal({
                        title: "Erreur!",
                        text: "Le produit n'a pas pu être retiré du panier.",
                        type: "error",
                        confirmButtonText: "OK"
                    });
                }
            })
            .catch(error => {
                swal({
                    title: "Erreur!",
                    text: "Une erreur est survenue. Veuillez réessayer.",
                    type: "error",
                    confirmButtonText: "OK"
                });
            });
        });
    });
});
