$(document).ready(function() {
    let offset = 10;  // Initial offset set to 10 to fetch the next set after the initial 10
    const limit = 10; // Fetch 10 blogs at a time
    const totalBlogs = parseInt(document.getElementById('totalBlogs').value, 10); // Total number of blogs

    $('#load-more').click(function() {
        $.ajax({
            url: loadMoreUrl, // This will be set in the HTML
            type: 'GET',
            data: {
                offset: offset,
                limit: limit
            },
            success: function(data) {
                if (data.length > 0) {
                    data.forEach(blog => {
                        $('#post-container').append(`
                            <div class="post-box ${blog.category.toLowerCase()}">
                                <a href="/post/${blog.id}">
                                    <img src="${blog.cover_path}" class="post-img">
                                    <h2 class="category"> ${blog.category} </h2>
                                    <h1 class="post-title"> ${blog.title} </h1>
                                    <span class="post-date"> ${blog.date} </span>
                                    <p class="post-decription"> ${blog.description.replace(/(<([^>]+)>)/gi, "")} </p>
                                    <div class="profile">
                                    <img src="${profileImageUrl}" alt="" class="profile-img">
                                    <span class="profile-name"> ${blog.author} </span>
                                </div>
                                </a>
                            </div>
                        `);
                    });
                    offset += limit; // Increase the offset by the limit
                    if (data.length < limit || offset >= totalBlogs) {
                        $('#load-more').hide(); // Hide the load more button if fewer than `limit` blogs are returned or all blogs are loaded
                    }
                } else {
                    $('#load-more').hide(); // Hide the load more button if no more blogs
                }
            }
        });
    });

    // Initially check if the number of loaded blogs is less than the total count to conditionally display the Load More button
    if (offset >= totalBlogs) {
        $('#load-more').hide();
    }
});
