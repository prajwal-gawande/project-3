// Booking form handling

document.addEventListener('DOMContentLoaded', function () {
    const bookingForm = document.getElementById('bookingForm');

    if (bookingForm) {
        // Time slot selection
        const timeSlots = document.querySelectorAll('.time-slot');
        const timeInput = document.getElementById('appointment_time');

        timeSlots.forEach(slot => {
            slot.addEventListener('click', function () {
                timeSlots.forEach(s => s.classList.remove('selected'));
                this.classList.add('selected');
                timeInput.value = this.dataset.time;
            });
        });

        // Form submission
        bookingForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            // Validate form
            if (!bookingForm.checkValidity()) {
                bookingForm.reportValidity();
                return;
            }

            // Check if time slot is selected
            if (!timeInput.value) {
                showToast('Please select a time slot', 'error');
                return;
            }

            // Disable submit button
            const submitBtn = bookingForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';

            try {
                const formData = new FormData(bookingForm);

                const response = await fetch('/booking/submit', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    showToast(data.message, 'success');
                    // Redirect to confirmation page
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1000);
                } else {
                    showToast(data.message, 'error');
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }
            } catch (error) {
                showToast('Failed to submit booking', 'error');
                console.error('Error:', error);
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        });
    }
});
