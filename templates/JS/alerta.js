document.addEventListener('DOMContentLoaded', () => {
    const alertContainer = document.getElementById('alert-container');
    if (alertContainer) {
        // Oculta automáticamente después de 5 segundos
        setTimeout(() => {
            alertContainer.querySelectorAll('.alert').forEach(alert => {
                let bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.close();
            });
        }, 5000);
    }
});
