document.addEventListener('DOMContentLoaded', function() {
  // Обработчик добавления книги
  document.getElementById('addBookForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch('/api/admin/books', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        location.reload();
      } else {
        alert('Ошибка: ' + data.error);
      }
    })
    .catch(error => {
      console.error('Ошибка:', error);
      alert('Произошла ошибка при добавлении книги');
    });
  });

  // Обработчики для кнопок редактирования
  document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const bookId = this.getAttribute('data-book-id');
      // Заполняем форму данными книги
      fetch(`/api/books/${bookId}`)
        .then(response => response.json())
        .then(book => {
          document.getElementById('edit_book_id').value = book.id;
          document.getElementById('edit_title').value = book.title;
          document.getElementById('edit_author').value = book.author;
          document.getElementById('edit_year').value = book.year;
          document.getElementById('edit_category_id').value = book.category_id;
          document.getElementById('edit_price').value = book.price;
          document.getElementById('edit_rental_price').value = book.rental_price;
          document.getElementById('edit_is_available').checked = book.is_available;
          document.getElementById('edit_stock_quantity').value = book.stock_quantity;
        })
        .catch(error => {
          console.error('Ошибка загрузки данных книги:', error);
          alert('Не удалось загрузить данные книги для редактирования');
        });
    });
  });

  // Обработчик сохранения изменений книги
  document.getElementById('editBookForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const bookId = document.getElementById('edit_book_id').value;
    const formData = new FormData(this);

    fetch(`/api/admin/books/${bookId}`, {
      method: 'PUT',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        $('#editBookModal').modal('hide');
        location.reload();
      } else {
        alert('Ошибка: ' + data.error);
      }
    })
    .catch(error => {
      console.error('Ошибка:', error);
      alert('Произошла ошибка при сохранении изменений');
    });
  });

  // Обработчик удаления книги
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      if (confirm('Вы уверены, что хотите удалить эту книгу?')) {
        const bookId = this.getAttribute('data-book-id');
        fetch(`/api/admin/books/${bookId}`, {
          method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            location.reload();
          } else {
            alert('Ошибка: ' + data.error);
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
