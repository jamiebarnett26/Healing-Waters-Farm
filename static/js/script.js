
// Home-page button for adding new crops
document.getElementById('navigateButton').addEventListener('click', function() {
  window.location.href = 'selectFamily';
});

document.getElementById('homepageButton').addEventListener('click', function() {
  window.location.href = '/homepage';
});

// Redirect to login
document.getElementById('logoutButton').addEventListener('click', function() {
  window.location.href = '/logout';
});