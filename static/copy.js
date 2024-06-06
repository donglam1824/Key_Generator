function copy(button) {
    const key = button.dataset.key; // Lấy giá trị key từ thuộc tính data-key

    navigator.clipboard.writeText(key) // Sao chép giá trị key vào clipboard
        .then(() => {
                alert('Key đã được sao chép!');
        })
        .catch(err => {
            alert('Lỗi khi sao chép key: ' + err);
        });
 }
