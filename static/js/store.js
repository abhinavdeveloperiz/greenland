// static/js/store.js
// Client-side cart, wishlist, and session state manager for Greenland Foodstuff

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
      // Ensure cart starts completely empty unless user explicitly adds products
      try {
        localStorage.removeItem('greenland_cart_items');
      } catch (e) {}
    },

    save() {
      try {
        localStorage.setItem('greenland_user_cart', JSON.stringify(this.items));
        localStorage.setItem('greenland_user_coupon', JSON.stringify(this.appliedCoupon));
      } catch (e) {}
    },

    get totalCount() {
      return this.items.reduce((acc, item) => acc + item.quantity, 0);
    },

    get subtotal() {
      return this.items.reduce((acc, item) => acc + (item.price * item.quantity), 0);
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
      return Math.round(this.subtotal * 0.05); // 5% GST
    },

    get total() {
      if (this.items.length === 0) return 0;
      return Math.max(0, this.subtotal - this.discount + this.finalDeliveryFee + this.tax);
    },

    addItem(product, qty = 1) {
      const existing = this.items.find(i => i.id === product.id);
      if (existing) {
        existing.quantity += qty;
      } else {
        this.items.push({
          id: product.id,
          name: product.name,
          price: product.price,
          originalPrice: product.originalPrice || product.price,
          weight: product.weight,
          image: product.image || (product.images && product.images[0]),
          quantity: qty
        });
      }
      this.save();
      this.showToast(`Added ${product.name} to your cart!`);
    },

    updateQty(id, qty) {
      if (qty <= 0) {
        this.removeItem(id);
      } else {
        const item = this.items.find(i => i.id === id);
        if (item) item.quantity = qty;
        this.save();
      }
    },

    removeItem(id) {
      this.items = this.items.filter(i => i.id !== id);
      this.save();
      this.showToast('Item removed from cart.');
    },

    clear() {
      this.items = [];
      this.appliedCoupon = null;
      this.save();
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

    get count() {
      return this.items.length;
    },

    has(id) {
      return this.items.some(i => i.id === id);
    },

    toggle(product) {
      if (this.has(product.id)) {
        this.items = this.items.filter(i => i.id !== product.id);
        Alpine.store('cart').showToast(`Removed from wishlist.`);
      } else {
        this.items.push(product);
        Alpine.store('cart').showToast(`Saved ${product.name} to wishlist!`);
      }
      localStorage.setItem('greenland_wishlist_items', JSON.stringify(this.items));
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
    },

    logout() {
      this.isLoggedIn = false;
      localStorage.setItem('greenland_logged_in', 'false');
      window.location.href = '/login/';
    }
  });
});
