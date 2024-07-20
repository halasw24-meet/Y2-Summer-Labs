function changeBackgroundColor() {
    const form = document.getElementById('colorForm');
    const color = form.color.value;
    document.body.style.backgroundColor = color;
}