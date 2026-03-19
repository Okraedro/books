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
document.addEventListener('DOMContentLoaded', function() {
  const sortForm = document.getElementById('sortForm');
  if (sortForm) {
    sortForm.addEventListener('submit', function(e) {
      e.preventDefault();

      const sortBy = document.getElementById('sort_by').value;
      const order = document.getElementById('order').value;

      // AJAX‑запрос для получения отсортированных данных
      fetch(`/my-books?sort_by=${sortBy}&order=${order}`)
        .then(response => response.text())
        .then(html => {
          // Обновляем только область с книгами
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, 'text/html');
          const newBooksContainer = doc.querySelector('.row');
          document.querySelector('.row').innerHTML = newBooksContainer.innerHTML;

          // Переинициализируем обработчики удаления
          initializeDeleteButtons();
        })
        .catch(error => {
          console.error('Ошибка при сортировке:', error);
          alert('Произошла ошибка при сортировке книг');
        });
    });
  }

  // Функция для переинициализации кнопок удаления
  function initializeDeleteButtons() {
    document.querySelectorAll('.delete-btn').forEach(button => {
      button.addEventListener('click', function(e) {
        e.stopPropagation();
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
  }

  // Инициализируем кнопки удаления при загрузке
  initializeDeleteButtons();
});
document.addEventListener('DOMContentLoaded', function() {
  const sortForm = document.getElementById('sortForm');
  const booksContainer = document.querySelector('.row');
  const notification = document.createElement('div');
  notification.className = 'sort-notification';
  document.body.appendChild(notification);

  function showNotification(message) {
    notification.textContent = message;
    notification.classList.add('show');
    setTimeout(() => {
      notification.classList.remove('show');
    }, 2000);
  }

  if (sortForm) {
    sortForm.addEventListener('submit', function(e) {
      e.preventDefault();

      const sortBy = document.getElementById('sort_by').value;
      const order = document.getElementById('order').value;

      // Добавляем индикатор загрузки
      booksContainer.classList.add('loading');
      showNotification(`Сортировка по ${getSortLabel(sortBy)} ${order === 'asc' ? 'по возрастанию' : 'по убыванию'}`);

      fetch(`/my-books?sort_by=${sortBy}&order=${order}`)
        .then(response => response.text())
        .then(html => {
          // Обновляем только область с книгами
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, 'text/html');
          const newBooksContainer = doc.querySelector('.row');

          if (newBooksContainer) {
            booksContainer.innerHTML = newBooksContainer.innerHTML;
            // Переинициализируем обработчики удаления
            initializeDeleteButtons();
            // Обновляем обработчики просмотра
            initializeViewButtons();
          }
        })
        .catch(error => {
          console.error('Ошибка при сортировке:', error);
          alert('Произошла ошибка при сортировке книг');
        })
        .finally(() => {
          // Убираем индикатор загрузки
          booksContainer.classList.remove('loading');
        });
    });
  }

  // Функция для получения читаемого названия поля сортировки
  function getSortLabel(field) {
    const labels = {
      'date_added': 'дате добавления',
      'title': 'названию',
      'author': 'автору',
      'year_published': 'году издания',
      'genre': 'жанру'
    };
    return labels[field] || field;
  }

  // Функция для переинициализации кнопок удаления
  function initializeDeleteButtons() {
    document.querySelectorAll('.delete-btn').forEach(button => {
      button.addEventListener('click', function(e) {
        e.stopPropagation();
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
  }

  // Функция для переинициализации кнопок просмотра
  function initializeViewButtons() {
    document.querySelectorAll('.btn-outline-info').forEach(button => {
      button.addEventListener('click', function(e) {
        e.stopPropagation();
      });
    });
  }

  // Инициализируем кнопки удаления и просмотра при загрузке
  initializeDeleteButtons();
  initializeViewButtons();
});

});
