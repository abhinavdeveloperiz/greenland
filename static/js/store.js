// static/js/store.js
// Client-side cart, wishlist, and session state manager with real-time Django backend synchronization

function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta && meta.content && meta.content !== 'NOTPROVIDED') {
    return meta.content;
  }
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === 'csrftoken=') {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue || '';
}

document.addEventListener('alpine:init', () => {
  // Clean up any legacy sample cart items from previous versions
  try {
    localStorage.removeItem('greenland_cart_items');
    localStorage.removeItem('greenland_applied_coupon');
  } catch (e) {}

  Alpine.store('cart', {
    items: JSON.parse(localStorage.getItem('greenland_user_cart') || '[]'),
    appliedCoupon: JSON.parse(localStorage.getItem('greenland_user_coupon') || 'null'),
    deliveryFee: 40,

    init() {
      // Synchronize with Django backend database cart
      this.fetchBackendCart();
    },

    save() {
      try {
        localStorage.setItem('greenland_user_cart', JSON.stringify(this.items));
        localStorage.setItem('greenland_user_coupon', JSON.stringify(this.appliedCoupon));
      } catch (e) {}
    },

    fetchBackendCart() {
      fetch('/cart/data/', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && data.success && Array.isArray(data.items)) {
          this.items = data.items;
          this.save();
        }
      })
      .catch(err => {
        // Fallback gracefully to localStorage if offline
        console.warn('Backend cart sync unavailable, using local storage cache.');
      });
    },

    get totalCount() {
      return this.items.reduce((acc, item) => acc + (Number(item.quantity) || 0), 0);
    },

    get subtotal() {
      return this.items.reduce((acc, item) => acc + ((Number(item.price) || 0) * (Number(item.quantity) || 0)), 0);
    },

    get discount() {
      if (!this.appliedCoupon) return 0;
      if (this.appliedCoupon.type === 'percent') {
        return Math.round((this.subtotal * this.appliedCoupon.value) / 100);
      }
      return this.appliedCoupon.value;
    },

    get finalDeliveryFee() {
      if (this.subtotal >= 499 || this.items.length === 0) return 0;
      return this.deliveryFee;
    },

    get tax() {
      return Math.round(this.subtotal * 0.05); // 5% GST / commercial fee
    },

    get total() {
      if (this.items.length === 0) return 0;
      return Math.max(0, this.subtotal - this.discount + this.finalDeliveryFee + this.tax);
    },

    addItem(product, qty = 1) {
      const itemKey = product.variantId
        ? `${product.id}-v${product.variantId}`
        : (product.weight ? `${product.id}-${String(product.weight).replace(/\s+/g, '_')}` : String(product.id));
      const existing = this.items.find(i => String(i.id) === String(itemKey));
      const requestedQty = Number.isFinite(Number(qty)) ? Math.max(1, Math.floor(Number(qty))) : 1;
      const hasStockLimit = product.stock !== undefined && product.stock !== null;
      const stockLimit = hasStockLimit ? Number(product.stock) : null;

      if (hasStockLimit && (!Number.isFinite(stockLimit) || stockLimit <= 0)) {
        this.showToast(`${product.name} is currently out of stock.`);
        return;
      }

      const currentQty = existing ? Math.max(0, Number(existing.quantity) || 0) : 0;
      const cappedCurrentQty = hasStockLimit ? Math.min(currentQty, stockLimit) : currentQty;
      if (existing && hasStockLimit) {
        existing.quantity = cappedCurrentQty;
        existing.stock = stockLimit;
      }

      const addQty = hasStockLimit
        ? Math.min(requestedQty, Math.max(0, stockLimit - cappedCurrentQty))
        : requestedQty;

      if (addQty === 0) {
        if (existing && hasStockLimit) this.save();
        this.showToast(`Only ${stockLimit} ${product.weight || 'items'} available.`);
        return;
      }

      // Optimistic instant UI update
      if (existing) {
        existing.quantity = cappedCurrentQty + addQty;
        if (hasStockLimit) existing.stock = stockLimit;
      } else {
        this.items.push({
          id: itemKey,
          productId: String(product.id),
          variantId: product.variantId || null,
          name: product.name,
          price: Number(product.price),
          originalPrice: Number(product.originalPrice || product.price),
          weight: product.weight || '',
          image: product.image || (product.images && product.images[0]),
          ...(hasStockLimit ? { stock: stockLimit } : {}),
          quantity: addQty
        });
      }
      this.save();
      const wtLabel = product.weight ? ` (${product.weight})` : '';
      this.showToast(`Added ${product.name}${wtLabel} to your cart!`);

      // Backend API sync
      fetch('/cart/add/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
          product_id: product.id,
          variant_id: product.variantId || null,
          quantity: addQty
        })
      })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && data.success && Array.isArray(data.items)) {
          this.items = data.items;
          this.save();
        }
      })
      .catch(err => {
        console.warn('Backend cart add failed, retained local copy:', err);
      });
    },

    updateQty(id, qty) {
      const targetQty = Math.floor(Number(qty));
      if (targetQty <= 0) {
        this.removeItem(id);
        return;
      }

      const item = this.items.find(i => String(i.id) === String(id));
      if (item) {
        const stockLimit = Number(item.stock);
        item.quantity = Number.isFinite(stockLimit)
          ? Math.min(targetQty, stockLimit)
          : targetQty;

        if (item.quantity < targetQty) {
          this.showToast(`Only ${stockLimit} ${item.weight || 'items'} available.`);
        }
      }
      this.save();

      // Backend API sync
      fetch('/cart/update/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
          item_key: id,
          quantity: targetQty
        })
      })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && data.success && Array.isArray(data.items)) {
          this.items = data.items;
          this.save();
        }
      })
      .catch(err => console.warn('Backend cart update failed:', err));
    },

    removeItem(id) {
      this.items = this.items.filter(i => String(i.id) !== String(id));
      this.save();
      this.showToast('Item removed from cart.');

      // Backend API sync
      fetch('/cart/remove/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ item_key: id })
      })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && data.success && Array.isArray(data.items)) {
          this.items = data.items;
          this.save();
        }
      })
      .catch(err => console.warn('Backend cart remove failed:', err));
    },

    clear() {
      this.items = [];
      this.appliedCoupon = null;
      this.save();

      // Backend API sync
      fetch('/cart/clear/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .catch(err => console.warn('Backend cart clear failed:', err));
    },

    applyPromo(code) {
      const c = code.trim().toUpperCase();
      if (c === 'GREENLAND20') {
        this.appliedCoupon = { code: 'GREENLAND20', type: 'percent', value: 20, desc: '20% OFF' };
        this.save();
        this.showToast('Coupon GREENLAND20 applied successfully! (20% OFF)');
        return true;
      } else if (c === 'FLAT50') {
        this.appliedCoupon = { code: 'FLAT50', type: 'flat', value: 50, desc: '₹50 FLAT OFF' };
        this.save();
        this.showToast('Coupon FLAT50 applied successfully! (₹50 OFF)');
        return true;
      } else {
        alert('Invalid coupon code. Try GREENLAND20 or FLAT50');
        return false;
      }
    },

    removePromo() {
      this.appliedCoupon = null;
      this.save();
      this.showToast('Coupon removed.');
    },

    showToast(msg) {
      const toast = document.getElementById('global-toast');
      if (toast) {
        toast.innerText = msg;
        toast.classList.remove('hidden');
        toast.classList.add('flex');
        setTimeout(() => {
          toast.classList.add('hidden');
          toast.classList.remove('flex');
        }, 2800);
      }
    }
  });

  Alpine.store('wishlist', {
    items: JSON.parse(localStorage.getItem('greenland_wishlist_items') || '[]'),

    init() {
      // Synchronize with Django backend database wishlist
      this.fetchBackendWishlist();
    },

    fetchBackendWishlist() {
      fetch('/wishlist/data/', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && data.success && Array.isArray(data.items)) {
          this.items = data.items;
          localStorage.setItem('greenland_wishlist_items', JSON.stringify(this.items));
        }
      })
      .catch(err => {
        console.warn('Backend wishlist sync unavailable, using local storage cache.');
      });
    },

    get count() {
      return this.items.length;
    },

    has(id) {
      return this.items.some(i => String(i.id) === String(id));
    },

    toggle(product) {
      const inWishlist = this.has(product.id);
      if (inWishlist) {
        this.items = this.items.filter(i => String(i.id) !== String(product.id));
        Alpine.store('cart').showToast(`Removed ${product.name} from wishlist.`);
      } else {
        this.items.push({
          id: String(product.id),
          name: product.name,
          price: Number(product.price),
          originalPrice: Number(product.originalPrice || product.price),
          weight: product.weight || '',
          image: product.image || (product.images && product.images[0])
        });
        Alpine.store('cart').showToast(`Saved ${product.name} to wishlist!`);
      }
      localStorage.setItem('greenland_wishlist_items', JSON.stringify(this.items));

      // Backend API sync
      fetch('/wishlist/toggle/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ product_id: product.id })
      })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && data.success) {
          // If server confirmed, ensure count is up to date
          if (data.in_wishlist && !this.has(product.id)) {
            this.items.push(data.item);
          } else if (!data.in_wishlist && this.has(product.id)) {
            this.items = this.items.filter(i => String(i.id) !== String(product.id));
          }
          localStorage.setItem('greenland_wishlist_items', JSON.stringify(this.items));
        }
      })
      .catch(err => console.warn('Backend wishlist toggle failed:', err));
    }
  });

  Alpine.store('auth', {
    isLoggedIn: localStorage.getItem('greenland_logged_in') === 'true',
    user: JSON.parse(localStorage.getItem('greenland_user') || '{"name": "Aryan Sharma", "email": "aryan.sharma@example.com", "phone": "+91 98765 43210"}'),

    login(email, name) {
      this.isLoggedIn = true;
      if (email) this.user.email = email;
      if (name) this.user.name = name;
      localStorage.setItem('greenland_logged_in', 'true');
      localStorage.setItem('greenland_user', JSON.stringify(this.user));
      // Re-sync cart and wishlist upon login
      if (Alpine.store('cart')) Alpine.store('cart').fetchBackendCart();
      if (Alpine.store('wishlist')) Alpine.store('wishlist').fetchBackendWishlist();
    },

    logout() {
      this.isLoggedIn = false;
      localStorage.setItem('greenland_logged_in', 'false');
      window.location.href = '/login/';
    }
  });
});
