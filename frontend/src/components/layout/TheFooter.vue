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
  background: #333;
  color: white;
  padding: 40px 20px 20px;
  margin-top: auto;
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
}

.footer-section h3 {
  color: #42b883;
}

.footer-section p {
  color: #aaa;
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
  color: #aaa;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-section a:hover {
  color: #42b883;
}

.footer-bottom {
  max-width: 1200px;
  margin: 40px auto 0;
  padding-top: 20px;
  border-top: 1px solid #444;
  text-align: center;
  color: #aaa;
}
</style>
