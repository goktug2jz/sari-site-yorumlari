$(document).ready(function() {
    localStorage.setItem('username', "goktug2jz");
    const username =localStorage.getItem('username');
    $(".username").html(username);
    if (username === null || username.trim() === '') {
        $(".comment-section").html("Lütfen giriş yapın");
        
    }else{
        var classifiedId;
        chrome.tabs.executeScript({
            file: 'content.js'
        }, function(results) {
            if (chrome.runtime.lastError) {
                document.getElementById('content').textContent = 'Bir hata oluştu: ' + chrome.runtime.lastError.message;
            } else {
                document.getElementById('content').textContent = "İlan Numarası: "+results[0];
                classifiedId = results[0];
            }
        });
        if (classifiedId === null || classifiedId.trim() === '') {
            $(".comments").html("ilan no tespit edilemedi");
        }else{
            // FastAPI servisine GET isteği atın
            $.get(`http://127.0.0.1:8000/comments/${classifiedId}`, function(data) {
                // Data'yı işleyin ve yorumları ekleyin
                if (data.length > 0) {
                    let commentsHtml = "";
                    data.forEach(comment => {
                        const commentDate = new Date(comment.comment_date).toLocaleDateString(); // Tarih formatını değiştirin
                        commentsHtml += `
                            <div class="comment">
                                <strong>${comment.username}:</strong> ${comment.comment}
                                <span class="date">${commentDate}</span>
                            </div>
                        `;
                    });
                    $(".comments").html(commentsHtml);
                } else {
                    $(".comments").html("Yorum bulunamadı. İlk yorumu siz yazın!");
                }
            }).fail(function(jqXHR, textStatus, errorThrown) {
                console.error("Error details:", textStatus, errorThrown);
                $(".comments").html("Yorumları yüklerken bir hata oluştu.");
            });
        }

    }
    //localStorage.clear();

    
});
