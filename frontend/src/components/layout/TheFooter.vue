<script setup lang="ts">
</script>

<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>Wiki Platform</h3>
        <p>A collaborative wiki platform for sharing knowledge and building communities.</p>
      </div>
      
      <div class="footer-section">
        <h4>Quick Links</h4>
        <ul>
          <li><RouterLink to="/">Home</RouterLink></li>
          <li><RouterLink to="/articles">Articles</RouterLink></li>
          <li><RouterLink to="/categories">Categories</RouterLink></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h4>Account</h4>
        <ul>
          <li><RouterLink to="/login">Login</RouterLink></li>
          <li><RouterLink to="/register">Register</RouterLink></li>
        </ul>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>&copy; 2026 Wiki Platform. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: var(--color-surface);
  color: var(--color-text);
  padding: 40px 20px 20px;
  margin-top: auto;
  border-top: 1px solid var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.1);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
}

.footer-section h3,
.footer-section h4 {
  margin-bottom: 16px;
  color: var(--color-primary);
  text-shadow: 0 0 5px var(--color-primary);
}

.footer-section p {
  color: var(--color-text-muted);
  line-height: 1.6;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section li {
  margin-bottom: 8px;
}

.footer-section a {
  color: var(--color-text-muted);
  text-decoration: none;
  transition: all 0.2s;
}

.footer-section a:hover {
  color: var(--color-primary);
  text-shadow: 0 0 5px var(--color-primary);
}

.footer-bottom {
  max-width: 1200px;
  margin: 40px auto 0;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
  text-align: center;
  color: var(--color-text-muted);
}
</style>
