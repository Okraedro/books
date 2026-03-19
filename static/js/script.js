document.addEventListener('DOMContentLoaded', function() {
  const applyFiltersBtn = document.getElementById('applyFilters');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortFilter = document.getElementById('sortFilter');
  const booksContainer = document.getElementById('booksContainer');
  const bookCards = document.querySelectorAll('.book-card');

  // Функция фильтрации
  function filterBooks() {
    const selectedCategory = categoryFilter.value;
    const sortBy = sortFilter.value;

    bookCards.forEach(card => {
      const cardCategory = card.getAttribute('data-category');
      const showByCategory = !selectedCategory || cardCategory === selectedCategory;

      if (showByCategory) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });

    // Простая сортировка на клиенте (для демонстрации)
    if (sortBy !== 'title') {
      Array.from(bookCards)
        .filter(card => card.style.display !== 'none')
        .sort((a, b) => {
          const aValue = a.getAttribute(`data-${sortBy}`);
          const bValue = b.getAttribute(`data-${sortBy}`);
          return sortBy === 'year' ? aValue - bValue : aValue.localeCompare(bValue);
        })
        .forEach(card => booksContainer.appendChild(card));
    }
  }

  applyFiltersBtn.addEventListener('click', filterBooks);

  // Обработчики для кнопок покупки/аренды
  document.querySelectorAll('.buy-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const bookId = this.getAttribute('data-book-id');
      alert(`Вы выбрали покупку книги с ID ${bookId}`);
      // Здесь будет AJAX‑запрос к API
    });
  });

  document.querySelectorAll('.rent-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const bookId = this.getAttribute('data-book-id');
      alert(`Вы выбрали аренду книги с ID ${bookId}. Выберите срок: 2 недели / 1 месяц / 3 месяца.`);
      // Здесь будет модальное окно выбора срока аренды
    });
  });
});

