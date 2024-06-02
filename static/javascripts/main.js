function filterBlogs(category, button) {
  let posts = document.querySelectorAll('.post-box');
  let buttons = document.querySelectorAll('.filter-item');

  buttons.forEach(btn => {
      btn.classList.remove('active-filter');
  });

  button.classList.add('active-filter');

  posts.forEach(post => {
      if (category === 'all') {
          post.style.display = 'block';
      } else {
          if (post.classList.contains(category)) {
              post.style.display = 'block';
          } else {
              post.style.display = 'none';
          }
      }
  });
}

// Initially show all posts
filterBlogs('all', document.querySelector('.filter-item'));
