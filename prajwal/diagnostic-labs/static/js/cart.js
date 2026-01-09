// Cart management

// Add to cart
async function addToCart(itemType, itemId, itemName) {
    try {
        const response = await fetch('/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: itemType,
                id: itemId
            })
        });

        const data = await response.json();

        if (data.success) {
            showToast(`${itemName} added to cart!`, 'success');
            updateCartCount(data.cart_count);
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        showToast('Failed to add item to cart', 'error');
        console.error('Error:', error);
    }
}

// Remove from cart
async function removeFromCart(itemType, itemId) {
    try {
        const response = await fetch('/cart/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: itemType,
                id: itemId
            })
        });

        const data = await response.json();

        if (data.success) {
            showToast('Item removed from cart', 'success');
            updateCartCount(data.cart_count);
            // Reload page to update cart display
            window.location.reload();
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        showToast('Failed to remove item from cart', 'error');
        console.error('Error:', error);
    }
}

// Update cart count in header
function updateCartCount(count) {
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(element => {
        element.textContent = count;
        if (count > 0) {
            element.style.display = 'flex';
        } else {
            element.style.display = 'none';
        }
    });
}

// Initialize cart buttons
document.addEventListener('DOMContentLoaded', function () {
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('[data-add-to-cart]');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function () {
            const itemType = this.dataset.itemType;
            const itemId = parseInt(this.dataset.itemId);
            const itemName = this.dataset.itemName;
            addToCart(itemType, itemId, itemName);
        });
    });

    // Remove from cart buttons
    const removeButtons = document.querySelectorAll('[data-remove-from-cart]');
    removeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const itemType = this.dataset.itemType;
            const itemId = parseInt(this.dataset.itemId);
            removeFromCart(itemType, itemId);
        });
    });
});
