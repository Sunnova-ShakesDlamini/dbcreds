// Custom JavaScript for dbcreds documentation

// Add copy button to code blocks
document.addEventListener('DOMContentLoaded', function() {
  // Code copy functionality is handled by mkdocs-material
  
  // Add fast mode indicator if in example code
  const codeBlocks = document.querySelectorAll('pre code');
  codeBlocks.forEach(block => {
    if (block.textContent.includes('DBCREDS_FAST_MODE')) {
      const badge = document.createElement('span');
      badge.className = 'fast-mode';
      badge.textContent = '⚡ Fast Mode';
      block.parentElement.insertBefore(badge, block);
    }
  });
});
