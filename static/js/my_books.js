document.addEventListener('DOMContentLoaded', function() {
  // Обработчик удаления книги с подтверждением
  document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function() {
      const bookId = this.getAttribute('data-book-id');
      if (confirm('Вы уверены, что хотите удалить эту книгу из коллекции?')) {
        fetch(`/delete-book/${bookId}`, {
          method: 'GET'
        })
        .then(response => {
          if (response.ok) {
            // Удаляем карточку книги из DOM без перезагрузки страницы
            const card = this.closest('.col-md-4');
            card.style.opacity = '0.5';
            setTimeout(() => card.remove(), 300);
          } else {
            alert('Ошибка при удалении книги');
          }
        })
        .catch(error => {
          console.error('Ошибка:', error);
          alert('Произошла ошибка при удалении книги');
        });
      }
    });
  });

  // Фильтрация книг по статусу
  const statusFilter = document.getElementById('statusFilter');
  if (statusFilter) {
    statusFilter.addEventListener('change', function() {
      const selectedStatus = this.value;
      document.querySelectorAll('.card').forEach(card => {
        const statusBadge = card.querySelector('.badge');
        if (!selectedStatus || statusBadge.textContent.includes(selectedStatus)) {
          card.parentElement.style.display = 'block';
        } else {
          card.parentElement.style.display = 'none';
        }
      });
    });
  }

  // Поиск по названию/автору
  const searchInput = document.getElementById('searchBooks');
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      const searchTerm = this.value.toLowerCase();
      document.querySelectorAll('.card').forEach(card => {
        const title = card.querySelector('.card-title').textContent.toLowerCase();
        const author = card.querySelector('p').textContent.toLowerCase();

        if (title.includes(searchTerm) || author.includes(searchTerm)) {
          card.parentElement.style.display = 'block';
        } else {
          card.parentElement.style.display = 'none';
        }
      });
    });
  }
  // Обработчик клика по карточке книги для перехода на страницу просмотра
document.querySelectorAll('.card').forEach(card => {
  // Исключаем кнопки внутри карточки
  if (!card.querySelector('a.btn, button')) {
    card.style.cursor = 'pointer';
    card.addEventListener('click', function() {
      const bookId = this.querySelector('.delete-btn')?.getAttribute('data-book-id');
      if (bookId) {
        window.location.href = `/book/${bookId}`;
      }
    });
  }
});

// Остальной код JavaScript остаётся без изменений
document.querySelectorAll('.delete-btn').forEach(button => {
  button.addEventListener('click', function(e) {
    e.stopPropagation(); // Останавливаем всплытие события
    const bookId = this.getAttribute('data-book-id');
    if (confirm('Вы уверены, что хотите удалить эту книгу из коллекции?')) {
      fetch(`/delete-book/${bookId}`, {
        method: 'GET'
      })
      .then(response => {
        if (response.ok) {
          const card = this.closest('.col-md-4');
          card.style.opacity = '0.5';
          setTimeout(() => card.remove(), 300);
        } else {
          alert('Ошибка при удалении книги');
        }
      })
      .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при удалении книги');
      });
    }
  });
});

});
